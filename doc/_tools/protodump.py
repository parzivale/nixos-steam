#!/usr/bin/env python3
"""Extract serialized FileDescriptorProtos embedded in a binary and write them as .proto text."""
import os, re, sys
from google.protobuf import descriptor_pb2

VALID_FIELDS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}


def varint(b, i):
    r = s = 0
    while True:
        if i >= len(b):
            raise ValueError
        c = b[i]; i += 1
        r |= (c & 0x7F) << s; s += 7
        if not c & 0x80:
            return r, i
        if s > 63:
            raise ValueError


def scan_end(b, i):
    """Walk wire-format fields from i while they look like FileDescriptorProto fields."""
    last_ok = i
    while i < len(b):
        try:
            key, j = varint(b, i)
        except ValueError:
            break
        fn, wt = key >> 3, key & 7
        if fn not in VALID_FIELDS:
            break
        if wt == 2:
            try:
                ln, j = varint(b, j)
            except ValueError:
                break
            if j + ln > len(b):
                break
            j += ln
        elif wt == 0:
            try:
                _, j = varint(b, j)
            except ValueError:
                break
        else:
            break
        i = j
        last_ok = i
    return last_ok


def extract(path):
    b = open(path, 'rb').read()
    found = {}
    for m in re.finditer(rb'\x0a([\x01-\x7f])([A-Za-z0-9_./]+\.proto)', b):
        ln = m.group(1)[0]
        if ln != len(m.group(2)):
            continue
        start = m.start()
        end = scan_end(b, start)
        fd = descriptor_pb2.FileDescriptorProto()
        try:
            fd.ParseFromString(b[start:end])
        except Exception:
            continue
        if not (fd.message_type or fd.enum_type or fd.service or fd.extension):
            continue
        prev = found.get(fd.name)
        if prev is None or len(prev.SerializeToString()) < end - start:
            found[fd.name] = fd
    return found


LABEL = {1: 'optional', 2: 'required', 3: 'repeated'}
TYPE = {1: 'double', 2: 'float', 3: 'int64', 4: 'uint64', 5: 'int32', 6: 'fixed64', 7: 'fixed32', 8: 'bool',
        9: 'string', 12: 'bytes', 13: 'uint32', 15: 'sfixed32', 16: 'sfixed64', 17: 'sint32', 18: 'sint64'}


def opts_str(opts):
    parts = []
    try:
        from google.protobuf.unknown_fields import UnknownFieldSet
        for u in UnknownFieldSet(opts):
            v = u.data
            if isinstance(v, bytes):
                try:
                    v = '"' + v.decode() + '"'
                except UnicodeDecodeError:
                    v = repr(v)
            parts.append(f'({u.field_number}) = {v}')
    except Exception:
        pass
    for fd, v in opts.ListFields():
        name = f'({fd.full_name})' if fd.is_extension else fd.name
        if isinstance(v, str):
            v = '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'
        elif isinstance(v, bool):
            v = 'true' if v else 'false'
        elif hasattr(v, 'ListFields'):
            v = '{ ' + str(v).replace('\n', ' ') + '}'
        parts.append(f'{name} = {v}')
    return ' [' + ', '.join(parts) + ']' if parts else ''


def fmt_field(f, ind):
    t = TYPE.get(f.type) or f.type_name
    d = f' [default = {f.default_value}]' if f.HasField('default_value') else ''
    o = opts_str(f.options)
    if d and o:
        o = ', ' + o.strip()[1:]
        return f'{ind}{LABEL[f.label]} {t} {f.name} = {f.number} [default = {f.default_value}{o};\n'
    return f'{ind}{LABEL[f.label]} {t} {f.name} = {f.number}{d}{o};\n'


def fmt_enum(e, ind):
    s = f'{ind}enum {e.name} {{\n'
    for v in e.value:
        s += f'{ind}\t{v.name} = {v.number}{opts_str(v.options)};\n'
    return s + f'{ind}}}\n'


def fmt_msg(m, ind=''):
    s = f'{ind}message {m.name} {{\n'
    for e in m.enum_type:
        s += fmt_enum(e, ind + '\t')
    for n in m.nested_type:
        s += fmt_msg(n, ind + '\t')
    for f in m.field:
        s += fmt_field(f, ind + '\t')
    for x in m.extension:
        s += f'{ind}\textend {x.extendee} {{ ' + fmt_field(x, '').strip() + ' }\n'
    return s + f'{ind}}}\n'


def fmt_file(fd):
    s = f'// {fd.name}\n'
    s += f'syntax = "{fd.syntax or "proto2"}";\n'
    if fd.package:
        s += f'package {fd.package};\n'
    for d in fd.dependency:
        s += f'import "{d}";\n'
    s += '\n'
    for x in fd.extension:
        s += f'extend {x.extendee} {{\n' + fmt_field(x, '\t') + '}\n'
    for e in fd.enum_type:
        s += fmt_enum(e, '') + '\n'
    for m in fd.message_type:
        s += fmt_msg(m) + '\n'
    for sv in fd.service:
        s += f'service {sv.name}{opts_str(sv.options)} {{\n'
        for me in sv.method:
            s += f'\trpc {me.name} ({me.input_type}) returns ({me.output_type}){opts_str(me.options)};\n'
        s += '}\n'
    return s


def main():
    outdir = sys.argv[1]
    found = {}
    for p in sys.argv[2:]:
        for k, v in extract(p).items():
            if k not in found or len(v.SerializeToString()) > len(found[k].SerializeToString()):
                found[k] = v
    # build a pool so custom options (extensions) are decoded
    from google.protobuf import descriptor_pool, message_factory
    pool = descriptor_pool.DescriptorPool()
    added = set()

    def add(name):
        if name in added:
            return
        if name not in found:
            if name == 'google/protobuf/descriptor.proto':
                pool.AddSerializedFile(descriptor_pb2.DESCRIPTOR.serialized_pb)
                added.add(name)
            return
        for d in found[name].dependency:
            add(d)
        try:
            pool.Add(found[name])
        except Exception as e:
            print('pool add failed', name, e, file=sys.stderr)
        added.add(name)

    for n in found:
        add(n)
    os.makedirs(outdir, exist_ok=True)
    for name, fd in sorted(found.items()):
        # re-parse options with extensions known
        try:
            fdesc = pool.FindFileByName(name)
            cls = message_factory.GetMessageClass(pool.FindMessageTypeByName('google.protobuf.FileDescriptorProto'))
            fdp = cls()
            fdp.ParseFromString(fd.SerializeToString())
            text = fmt_file(fdp)
        except Exception as e:
            text = fmt_file(fd)
        p = os.path.join(outdir, name)
        os.makedirs(os.path.dirname(p) or outdir, exist_ok=True)
        open(p, 'w').write(text)
    print(len(found), 'descriptors')


if __name__ == '__main__':
    main()
