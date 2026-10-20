#!/usr/bin/env python3
"""Collect usage context for config records: the strings referenced by the code that uses each option.

usage.py <elf> <binary-key> <records.json> <calls.jsonl>  -> JSON on stdout

* Function boundaries come from .eh_frame_hdr (every FDE's initial location).
* For call-site records (env vars, switches, hints...): strings referenced near the call site
  (closest by address) within the containing function.
* For ConVars: the ConVar object address is the constructor's `this` (a0). Every function that
  references [obj, obj+0x80) (other than the registering initializer) is a *reader*; we collect the
  strings those readers reference near each access.
Disassembly is detail-free (operand text parsing) and chunked, to keep memory low.
"""
import bisect, json, mmap, re, struct, sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

RIP = re.compile(r'\[rip ([+-]) (0x[0-9a-f]+)\]')
IMM = re.compile(r'(?:^|, )(0x[0-9a-f]{5,8})$')
NEAR = 14          # strings kept around each access
OBJ_SPAN = 0x80    # bytes of a ConVar object that count as "touching" it


def eh_frame_starts(elf, read):
    sec = elf.get_section_by_name('.eh_frame_hdr')
    base = sec['sh_addr']
    d = sec.data()
    ver, ptr_enc, cnt_enc, tbl_enc = d[0], d[1], d[2], d[3]
    assert ver == 1 and tbl_enc == 0x3b, (ver, tbl_enc)
    off = 4 + 4  # eh_frame_ptr (sdata4)
    count = struct.unpack_from('<I', d, off)[0]
    off += 4
    starts = []
    for i in range(count):
        loc, _ = struct.unpack_from('<ii', d, off + i * 8)
        starts.append(base + loc)
    starts.sort()
    return starts


def main(path, binkey, recpath, callspath):
    f = open(path, 'rb')
    elf = ELFFile(f)
    data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    segs = [(s['p_vaddr'], s['p_filesz'], s['p_offset']) for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']

    def read(addr, n):
        for va, sz, off in segs:
            if va <= addr < va + sz:
                return data[off + (addr - va): off + (addr - va) + n]
        return None

    def cstr(addr):
        b = read(addr, 400)
        if not b:
            return None
        e = b.find(b'\0')
        if e < 3:
            return None
        try:
            t = b[:e].decode()
        except UnicodeDecodeError:
            return None
        return t if all(c.isprintable() or c in '\n\t' for c in t) else None

    starts = eh_frame_starts(elf, read)

    def func_of(a):
        i = bisect.bisect_right(starts, a) - 1
        return starts[i] if i >= 0 else None

    recs = [r for r in json.load(open(recpath)) if r['binary'] == binkey]
    a0_by_site = {}
    for line in open(callspath):
        c = json.loads(line)
        a0 = c['args'].get('a0')
        if a0 and 'p' in a0:
            a0_by_site[c['site']] = a0['p']

    site_items = {}   # call site -> [record keys]
    obj_items = {}    # convar object -> [record keys]
    init_funcs = set()
    for r in recs:
        key = f"{r['kind']}:{r['name']}"
        if r['kind'] == 'convar' and r['site'] in a0_by_site:
            obj_items.setdefault(a0_by_site[r['site']], []).append(key)
            init_funcs.add(func_of(r['site']))
        else:
            site_items.setdefault(r['site'], []).append(key)
    objs = sorted(obj_items)
    site_funcs = {func_of(s) for s in site_items}

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    text = elf.get_section_by_name('.text')
    code = text.data()
    base = text['sh_addr']
    out = {}

    # per-function buffers, flushed when we cross into the next function
    cur_func = None
    strs = []      # (insn_addr, string)
    hits = []      # (insn_addr, key)

    def flush():
        if not hits:
            return
        sa = [a for a, _ in strs]
        for at, key in hits:
            i = bisect.bisect_left(sa, at)
            lo, hi = max(0, i - NEAR // 2), min(len(strs), i + NEAR // 2)
            near = []
            for _, s in strs[lo:hi]:
                if s not in near:
                    near.append(s)
            ent = out.setdefault(key, [])
            if len(ent) < 6:
                ent.append({'func': hex(cur_func), 'at': hex(at), 'strings': near})

    off = 0
    n = len(code)
    while off < n:
        end = min(off + 65536, n)
        nxt = off
        for addr, size, mn, ops in md.disasm_lite(code[off:end], base + off):
            ie = addr - base + size
            if end < n and ie > end - 16:
                break
            nxt = ie
            fs = func_of(addr)
            if fs != cur_func:
                flush()
                cur_func, strs, hits = fs, [], []
            want_func = cur_func in site_funcs or objs
            if not want_func:
                continue
            if mn == 'call' and addr in site_items:
                for k in site_items[addr]:
                    hits.append((addr, k))
            m = RIP.search(ops)
            tgt = None
            if m:
                disp = int(m.group(2), 16)
                tgt = addr + size + (disp if m.group(1) == '+' else -disp)
            else:
                m2 = IMM.search(ops)
                if m2:
                    tgt = int(m2.group(1), 16)
            if tgt is None:
                continue
            if mn in ('lea', 'mov'):
                s = cstr(tgt)
                if s is not None:
                    strs.append((addr, s))
            if cur_func not in init_funcs:
                j = bisect.bisect_right(objs, tgt) - 1
                if j >= 0 and tgt - objs[j] < OBJ_SPAN:
                    for k in obj_items[objs[j]]:
                        hits.append((addr, k))
        off = nxt if nxt > off else off + 1
    flush()
    json.dump(out, sys.stdout)


if __name__ == '__main__':
    main(*sys.argv[1:5])
