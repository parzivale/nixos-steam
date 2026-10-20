#!/usr/bin/env python3
"""Render CMsgClientSettings (with its custom field options) as a Markdown reference."""
import struct, sys
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from protodump import extract

STORE = {0: 'Invalid', 1: 'ConfigStore/Install (config/config.vdf)', 2: 'ConfigStore/UserRoaming (userdata/<id>/7/remote/sharedconfig.vdf)',
         3: 'ConfigStore/UserLocal (userdata/<id>/config/localconfig.vdf)', 4: 'Registry (registry.vdf)', 5: 'CustomFunc (computed in code)'}
STORE_SHORT = {0: 'invalid', 1: 'Install', 2: 'UserRoaming', 3: 'UserLocal', 4: 'Registry', 5: 'CustomFunc'}
PROFILE = {0: '', 1: 'per-game', 2: 'per-game+display', 3: 'per-display'}
TYPE = {1: 'double', 2: 'float', 3: 'int64', 4: 'uint64', 5: 'int32', 6: 'fixed64', 7: 'fixed32', 8: 'bool',
        9: 'string', 12: 'bytes', 13: 'uint32', 14: 'enum', 11: 'message'}


def fmt_float(v):
    # options are stored as float32; print the shortest repr that round-trips
    for p in range(1, 10):
        s = f'{v:.{p}g}'
        if struct.unpack('<f', struct.pack('<f', float(s)))[0] == struct.unpack('<f', struct.pack('<f', v))[0]:
            return s
    return repr(v)


def esc(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def main(binary, out):
    found = extract(binary)
    pool = descriptor_pool.DescriptorPool()
    pool.AddSerializedFile(descriptor_pb2.DESCRIPTOR.serialized_pb)
    done = {'google/protobuf/descriptor.proto'}

    def add(n):
        if n in done or n not in found:
            return
        for d in found[n].dependency:
            add(d)
        pool.Add(found[n]); done.add(n)

    add('steammessages_clientsettings.proto')
    msg = pool.FindMessageTypeByName('CMsgClientSettings')
    fo_cls = message_factory.GetMessageClass(pool.FindMessageTypeByName('google.protobuf.FieldOptions'))
    ext = {e: pool.FindExtensionByName(e) for e in [
        'setting_store', 'setting_name', 'setting_pre_login', 'setting_default_bool', 'setting_default_int',
        'setting_default_uint', 'setting_default_float', 'setting_default_string', 'setting_readonly',
        'setting_description', 'setting_profile_mode', 'setting_clamp_min', 'setting_clamp_max']}
    rows = []
    for f in msg.fields:
        o = fo_cls(); o.ParseFromString(f.GetOptions().SerializeToString())

        def g(k):
            return o.Extensions[ext[k]] if o.HasExtension(ext[k]) else None
        default = None
        for k in ('setting_default_bool', 'setting_default_int', 'setting_default_uint', 'setting_default_float', 'setting_default_string'):
            v = g(k)
            if v is not None:
                default = ('true' if v else 'false') if isinstance(v, bool) else fmt_float(v) if isinstance(v, float) else repr(v) if isinstance(v, str) else v
        if default is None and f.has_default_value:
            default = f.default_value
        t = f.message_type.name if f.message_type else f.enum_type.name if f.enum_type else TYPE.get(f.type, f.type)
        if f.is_repeated:
            t = 'repeated ' + t
        flags = []
        if g('setting_pre_login'): flags.append('pre-login')
        if g('setting_readonly'): flags.append('read-only')
        pm = g('setting_profile_mode')
        if pm: flags.append(PROFILE.get(pm, pm))
        cmin, cmax = g('setting_clamp_min'), g('setting_clamp_max')
        if cmin is not None or cmax is not None: flags.append(f'clamp [{cmin if cmin is not None else ""}..{cmax if cmax is not None else ""}]')
        rows.append((f.number, f.name, t, STORE_SHORT.get(g('setting_store'), ''), g('setting_name') or '', default, flags, g('setting_description') or ''))

    import json, os
    sdesc = json.load(open('desc/settings.json')) if os.path.exists('desc/settings.json') else {}

    def what(name):
        d = sdesc.get(name)
        if not d:
            return '', ''
        tag = '' if d.get('confidence') == 'high' else f" *({d.get('confidence', '?')})*"
        return esc(d['what']) + tag, esc(d.get('ui', ''))

    with open(out, 'w') as w:
        w.write('# Client settings (`CMsgClientSettings`)\n\n')
        w.write('This is the canonical list of user-facing *and* hidden client settings. It was recovered from the protobuf\n'
                'descriptor `steammessages_clientsettings.proto`, which is embedded in `steamclient.so`/`steamui.so`.\n'
                'The settings UI (`SteamClient.Settings`) reads and writes these fields, and each field carries custom\n'
                'options that say where the value is persisted and what its default is.\n\n')
        w.write(f'Total settings: **{len(rows)}**\n\n')
        w.write('## Storage backends (`EClientSettingStore`)\n\n| Store | Where it lives |\n|---|---|\n')
        for k in (1, 2, 3, 4, 5):
            w.write(f'| {STORE_SHORT[k]} | {STORE[k]} |\n')
        w.write('\nKey paths use `\\` as the KeyValues path separator; e.g. `system\\EnableGameOverlay` in the UserLocal\n'
                'store is `UserLocalConfigStore/system/EnableGameOverlay` in `localconfig.vdf`. Registry-store names are\n'
                'keys under `Registry/HKCU/Software/Valve/Steam` in `~/.steam/registry.vdf`. `CustomFunc` settings have no\n'
                'single backing key; the client computes them or forwards them to subsystems such as the voice, ping and\n'
                'screenshot managers.\n\n')
        w.write('Flags: `pre-login` = available before a user signs in; `read-only` = cannot be set; `per-game`/`per-display` = stored per profile; `clamp` = value range enforced by the client.\n\n')
        w.write('## All settings\n\n**What it does** and **Where in the UI** come from how the Steam UI and client use each field\n'
                '(localized labels, the code that reads it). Descriptions tagged *(medium)* or *(low)* are inferences.\n'
                '**Valve description** is the descriptor\'s own `setting_description`.\n\n'
                '| # | Field | What it does | Where in the UI | Type | Store | Key | Default | Flags | Valve description |\n'
                '|---|---|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            num, name, t, store, key, d, flags, desc = r
            wd, ui = what(name)
            w.write(f'| {num} | `{name}` | {wd} | {ui} | {esc(t)} | {store} | {"`" + esc(key) + "`" if key else ""} | {"`" + esc(d) + "`" if d is not None else ""} | {", ".join(flags)} | {esc(desc)} |\n')
        # enums referenced
        enums = sorted({f.enum_type.full_name for f in msg.fields if f.enum_type})
        if enums:
            w.write('\n## Enum types used by settings\n\n')
            for en in enums:
                e = pool.FindEnumTypeByName(en)
                w.write(f'### `{en}`\n\n| Value | Name |\n|---|---|\n')
                for v in e.values:
                    w.write(f'| {v.number} | `{v.name}` |\n')
                w.write('\n')
    print(len(rows), 'settings')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
