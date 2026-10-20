#!/usr/bin/env python3
"""Recover string/immediate arguments passed at every call site in an x86-64 ELF.

Linear-sweeps executable sections with capstone, tracks per-basic-block register
state for the SysV argument registers (rdi rsi rdx rcx r8 r9) and emits one JSON
line per call: {"site", "target", "target_name", "args": {reg: value}}.
A value is {"s": "<c-string>"} for rip-relative leas pointing at printable
strings, {"i": n} for immediates, {"p": addr} for other rip-relative addresses.
"""
import json, mmap, sys, struct
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

ARGREGS = {
    'rdi': 'a0', 'edi': 'a0', 'rsi': 'a1', 'esi': 'a1', 'rdx': 'a2', 'edx': 'a2',
    'rcx': 'a3', 'ecx': 'a3', 'r8': 'a4', 'r8d': 'a4', 'r9': 'a5', 'r9d': 'a5',
    'xmm0': 'f0', 'xmm1': 'f1', 'xmm2': 'f2',
}


def load(path):
    f = open(path, 'rb')
    elf = ELFFile(f)
    segs = [(s['p_vaddr'], s['p_filesz'], s['p_offset']) for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']
    data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    def read(addr, n):
        for va, sz, off in segs:
            if va <= addr < va + sz:
                return data[off + (addr - va): off + (addr - va) + n]
        return None

    # symbol names for PLT targets and defined functions
    names = {}
    for secname in ('.symtab', '.dynsym'):
        sec = elf.get_section_by_name(secname)
        if not sec:
            continue
        for s in sec.iter_symbols():
            if s['st_value'] and s['st_info']['type'] == 'STT_FUNC':
                names.setdefault(s['st_value'], s.name)
    # PLT: map plt stub address -> imported symbol via .rela.plt / GOT
    dynsym = elf.get_section_by_name('.dynsym')
    got2sym = {}
    for sec in elf.iter_sections():
        if isinstance(sec, RelocationSection) and sec.name in ('.rela.plt', '.rela.dyn'):
            for r in sec.iter_relocations():
                if r['r_info_sym']:
                    got2sym[r['r_offset']] = dynsym.get_symbol(r['r_info_sym']).name
    # absolute pointers stored in data (RELATIVE relocs) for string pointer tables
    relative = {}
    for sec in elf.iter_sections():
        if isinstance(sec, RelocationSection) and sec.name == '.rela.dyn':
            for r in sec.iter_relocations():
                if r['r_info_type'] == 8:  # R_X86_64_RELATIVE
                    relative[r['r_offset']] = r['r_addend']
    return elf, read, names, got2sym, relative


def cstr(read, addr, maxlen=4096):
    b = read(addr, maxlen)
    if not b:
        return None
    end = b.find(b'\0')
    if end <= 0:
        return None
    s = b[:end]
    try:
        t = s.decode('utf-8')
    except UnicodeDecodeError:
        return None
    if not all(c.isprintable() or c in '\n\t\r' for c in t):
        return None
    return t


def chunked_disasm(md, code, base, chunk=64 * 1024):
    """capstone's disasm() decodes its whole input in C before yielding, so feed it
    small windows to keep memory bounded. Each window resumes after the last
    instruction that ended safely before the window edge."""
    off = 0
    n = len(code)
    while off < n:
        end = min(off + chunk, n)
        nxt = off
        for ins in md.disasm(code[off:end], base + off):
            ins_end = ins.address - base + ins.size
            if end < n and ins_end > end - 16:
                break
            nxt = ins_end
            yield ins
        if nxt == off:  # nothing decodable; skip a byte
            nxt = off + 1
        off = nxt


def main(path):
    elf, read, names, got2sym, relative = load(path)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    md.skipdata = True
    # resolve plt stubs: jmp [rip+X] where X is a GOT slot
    plt_names = {}
    for secname in ('.plt', '.plt.sec', '.plt.got'):
        sec = elf.get_section_by_name(secname)
        if not sec:
            continue
        for ins in md.disasm(sec.data(), sec['sh_addr']):
            if ins.mnemonic in ('jmp', 'bnd jmp') and ins.operands and ins.operands[0].type == X86_OP_MEM and ins.operands[0].mem.base == X86_REG_RIP:
                slot = ins.address + ins.size + ins.operands[0].mem.disp
                if slot in got2sym:
                    # stub start: align down to 16 (.plt.sec stubs are 16 bytes)
                    plt_names[ins.address & ~0xF] = got2sym[slot]
    text = elf.get_section_by_name('.text')
    out = sys.stdout
    # Track every GP/xmm register (canonical 64-bit names). Callee-saved registers survive
    # calls, which matters because compilers hoist e.g. lea r14,"0" and reuse it per ConVar.
    regs = {}
    for ins in chunked_disasm(md, text.data(), text['sh_addr']):
        if ins.id == 0:
            regs = {}
            continue
        m = ins.mnemonic
        if m in ('ret', 'jmp', 'ud2', 'hlt') or m.startswith('int3'):
            regs = {}
            continue
        ops = ins.operands
        if m == 'call':
            tgt = None
            tname = None
            if ops and ops[0].type == X86_OP_IMM:
                tgt = ops[0].imm
                tname = plt_names.get(tgt) or names.get(tgt)
            elif ops and ops[0].type == X86_OP_MEM and ops[0].mem.base == X86_REG_RIP:
                slot = ins.address + ins.size + ops[0].mem.disp
                tname = got2sym.get(slot)
            args = {ARGNAME[r]: regs[r] for r in ARGNAME if r in regs}
            if args:
                out.write(json.dumps({'site': ins.address, 'target': tgt, 'target_name': tname, 'args': args}) + '\n')
            for r in CALLER_SAVED:
                regs.pop(r, None)
            continue
        val = None
        dst = None
        if len(ops) == 2 and ops[0].type == X86_OP_REG:
            dst = canon(ins.reg_name(ops[0].reg))
            src = ops[1]
            if m == 'lea' and src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
                addr = ins.address + ins.size + src.mem.disp
                s = cstr(read, addr)
                val = {'s': s} if s is not None else {'p': addr}
            elif m in ('mov', 'movabs') and src.type == X86_OP_IMM:
                val = {'i': src.imm}
                if src.imm > 0x10000:
                    s = cstr(read, src.imm)
                    if s is not None:
                        val = {'s': s}
            elif m in ('mov', 'movaps', 'movapd', 'movq', 'movd') and src.type == X86_OP_REG:
                s_ = canon(ins.reg_name(src.reg))
                if s_ in regs:
                    val = regs[s_]
            elif m in ('movss', 'movsd') and src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
                addr = ins.address + ins.size + src.mem.disp
                b = read(addr, 8)
                if b:
                    val = {'f': struct.unpack('<f', b[:4])[0] if m == 'movss' else struct.unpack('<d', b)[0]}
            elif m in ('xor', 'pxor', 'xorps') and src.type == X86_OP_REG and src.reg == ops[0].reg:
                val = {'i': 0}
            elif m == 'mov' and src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
                slot = ins.address + ins.size + src.mem.disp
                if slot in relative:
                    s = cstr(read, relative[slot])
                    val = {'s': s} if s is not None else {'p': relative[slot]}
        # invalidate anything this instruction writes
        try:
            _, written = ins.regs_access()
        except Exception:
            written = ()
        for r in written:
            regs.pop(canon(ins.reg_name(r)), None)
        if dst is not None and val is not None:
            regs[dst] = val


CANON = {}
for _q, _d, _w, _b in [('rax', 'eax', 'ax', 'al'), ('rbx', 'ebx', 'bx', 'bl'), ('rcx', 'ecx', 'cx', 'cl'), ('rdx', 'edx', 'dx', 'dl'),
                       ('rsi', 'esi', 'si', 'sil'), ('rdi', 'edi', 'di', 'dil'), ('rbp', 'ebp', 'bp', 'bpl'), ('rsp', 'esp', 'sp', 'spl')]:
    for _n in (_q, _d, _w, _b):
        CANON[_n] = _q
for _i in range(8, 16):
    for _n in (f'r{_i}', f'r{_i}d', f'r{_i}w', f'r{_i}b'):
        CANON[_n] = f'r{_i}'


def canon(name):
    return CANON.get(name, name)


ARGNAME = {'rdi': 'a0', 'rsi': 'a1', 'rdx': 'a2', 'rcx': 'a3', 'r8': 'a4', 'r9': 'a5', 'xmm0': 'f0', 'xmm1': 'f1', 'xmm2': 'f2'}
CALLER_SAVED = ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11'] + [f'xmm{i}' for i in range(16)]


if __name__ == '__main__':
    main(sys.argv[1])
