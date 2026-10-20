#!/usr/bin/env python3
"""Merge declarative settings into Steam's text KeyValues (VDF) config files.

steam-config-apply <config.json>

config.json:
  {
    "steamRoot": null | "/path",           # default: ~/.steam/steam -> ~/.local/share/Steam
    "userIds": null | ["12345678", ...],   # default: every userdata/<id> directory
    "settings": [ {"store": "install|local|roaming|registry", "key": "a\\b/c", "value": "<string>"} ],
    "steamCfg": {"BootStrapperInhibitAll": "enable", ...}   # written to <root>/steam.cfg (empty -> removed)
  }

Rules:
* Does nothing while Steam is running (pid in ~/.steam/steam.pid alive): Steam rewrites these files on exit.
* Keys are matched case-insensitively (KeyValues semantics); existing key spelling is kept.
* Files are written atomically; the first time a file is modified a `.nixos-steam.bak` copy is kept.
* Missing files are created (e.g. registry.vdf before first run); missing userdata dirs are skipped.
"""
import json, os, sys, tempfile

ROOTS = {'install': 'InstallConfigStore', 'local': 'UserLocalConfigStore', 'roaming': 'UserRoamingConfigStore', 'registry': 'Registry'}
MANAGED_MARK = '# managed by nixos-steam (programs.steam.client.steamCfg)\n'


# ---------------------------------------------------------------- KeyValues text format
def tokenize(s):
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in ' \t\r\n':
            i += 1
        elif s.startswith('//', i):
            j = s.find('\n', i)
            i = n if j < 0 else j + 1
        elif c in '{}':
            yield c
            i += 1
        elif c == '"':
            i += 1
            out = []
            while i < n and s[i] != '"':
                if s[i] == '\\' and i + 1 < n:
                    out.append({'n': '\n', 't': '\t', '\\': '\\', '"': '"'}.get(s[i + 1], '\\' + s[i + 1]))
                    i += 2
                else:
                    out.append(s[i])
                    i += 1
            i += 1
            yield ('s', ''.join(out))
        elif c == '[':  # conditional like [$WIN32]: ignore
            j = s.find(']', i)
            i = n if j < 0 else j + 1
        else:
            j = i
            while j < n and s[j] not in ' \t\r\n{}"':
                j += 1
            yield ('s', s[i:j])
            i = j


def parse(s):
    """Parse into nested lists of [key, value] pairs (value: str or list), preserving order and duplicates."""
    toks = list(tokenize(s))
    pos = 0

    def block():
        nonlocal pos
        items = []
        while pos < len(toks):
            t = toks[pos]
            if t == '}':
                pos += 1
                return items
            if t == '{':  # stray brace
                pos += 1
                continue
            key = t[1]
            pos += 1
            if pos >= len(toks):
                break
            v = toks[pos]
            if v == '{':
                pos += 1
                items.append([key, block()])
            elif v == '}':
                items.append([key, ''])
            else:
                pos += 1
                items.append([key, v[1]])
        return items

    return block()


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')


def dump(items, depth=0):
    out = []
    ind = '\t' * depth
    for k, v in items:
        if isinstance(v, list):
            out.append(f'{ind}"{esc(k)}"\n{ind}{{\n{dump(v, depth + 1)}{ind}}}\n')
        else:
            out.append(f'{ind}"{esc(k)}"\t\t"{esc(v)}"\n')
    return ''.join(out)


def set_path(items, path, value):
    for i, comp in enumerate(path):
        last = i == len(path) - 1
        hit = next((kv for kv in items if kv[0].lower() == comp.lower()), None)
        if last:
            if hit is None:
                items.append([comp, value])
            elif hit[1] != value:
                hit[1] = value
            else:
                return False
            return True
        if hit is None or not isinstance(hit[1], list):
            if hit is None:
                hit = [comp, []]
                items.append(hit)
            else:
                hit[1] = []
        items = hit[1]
    return False


# ---------------------------------------------------------------- files
def steam_running(home):
    try:
        pid = int(open(os.path.join(home, '.steam', 'steam.pid')).read().strip())
        os.kill(pid, 0)
        return os.path.exists(f'/proc/{pid}') and 'steam' in open(f'/proc/{pid}/comm').read()
    except (OSError, ValueError):
        return False


def write_atomic(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not os.path.exists(path + '.nixos-steam.bak'):
        with open(path, 'rb') as a, open(path + '.nixos-steam.bak', 'wb') as b:
            b.write(a.read())
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='.nixos-steam.')
    with os.fdopen(fd, 'w') as w:
        w.write(text)
    os.replace(tmp, path)


def apply_file(path, root_key, entries, prefix=()):
    try:
        items = parse(open(path, encoding='utf-8', errors='replace').read())
    except FileNotFoundError:
        items = []
    root = next((kv for kv in items if kv[0].lower() == root_key.lower() and isinstance(kv[1], list)), None)
    if root is None:
        root = [root_key, []]
        items.append(root)
    changed = False
    for key, value in entries:
        path_ = list(prefix) + [p for p in key.replace('/', '\\').split('\\') if p]
        changed |= set_path(root[1], path_, value)
    if changed:
        write_atomic(path, dump(items))
    return changed


def registry_path(key):
    """setting_name for the registry store: 'HKEY_CURRENT_USER\\Software\\Valve\\Steam\\X' -> HKCU/Software/Valve/Steam/X."""
    parts = [p for p in key.replace('/', '\\').split('\\') if p]
    hive = {'HKEY_CURRENT_USER': 'HKCU', 'HKEY_LOCAL_MACHINE': 'HKLM', 'HKCU': 'HKCU', 'HKLM': 'HKLM'}.get(parts[0].upper(), None)
    return '\\'.join([hive] + parts[1:]) if hive else '\\'.join(['HKCU'] + parts)


# ---------------------------------------------------------------- binary KeyValues (shortcuts.vdf)
def bkv_parse(b, i=0):
    """Parse a binary KeyValues map starting at i; returns (items, i) with items = [[key, value]]."""
    items = []
    while i < len(b):
        t = b[i]; i += 1
        if t == 0x08:
            return items, i
        e = b.index(b'\0', i); key = b[i:e].decode('utf-8', 'replace'); i = e + 1
        if t == 0x00:
            v, i = bkv_parse(b, i)
        elif t == 0x01:
            e = b.index(b'\0', i); v = b[i:e].decode('utf-8', 'replace'); i = e + 1
        elif t == 0x02:
            v = ('i32', int.from_bytes(b[i:i + 4], 'little', signed=True)); i += 4
        elif t == 0x07:
            v = ('u64', int.from_bytes(b[i:i + 8], 'little')); i += 8
        elif t == 0x03:
            v = ('f32', b[i:i + 4]); i += 4
        else:
            raise ValueError(f'unsupported binary KV type {t:#x}')
        items.append([key, v])
    return items, i


def bkv_dump(items):
    out = bytearray()
    for k, v in items:
        kb = k.encode() + b'\0'
        if isinstance(v, list):
            out += b'\x00' + kb + bkv_dump(v)
        elif isinstance(v, str):
            out += b'\x01' + kb + v.encode() + b'\0'
        elif v[0] == 'i32':
            out += b'\x02' + kb + (v[1] & 0xFFFFFFFF).to_bytes(4, 'little')
        elif v[0] == 'u64':
            out += b'\x07' + kb + v[1].to_bytes(8, 'little')
        elif v[0] == 'f32':
            out += b'\x03' + kb + v[1]
    return bytes(out + b'\x08')


def shortcut_appid(exe, name):
    import zlib
    return (zlib.crc32((exe + name).encode()) & 0xFFFFFFFF) | 0x80000000


def apply_shortcuts(path, wanted):
    """Upsert managed non-Steam shortcuts (matched by their generated appid); other shortcuts are kept."""
    try:
        items, _ = bkv_parse(open(path, 'rb').read())
    except FileNotFoundError:
        items = []
    root = next((kv for kv in items if kv[0].lower() == 'shortcuts' and isinstance(kv[1], list)), None)
    if root is None:
        root = ['shortcuts', []]
        items = [root]
    entries = [v for _, v in root[1] if isinstance(v, list)]

    def appid_of(e):
        for k, v in e:
            if k.lower() == 'appid' and isinstance(v, tuple):
                return v[1] & 0xFFFFFFFF
        return None

    for w in wanted:
        exe = '"' + w['exe'] + '"'
        aid = shortcut_appid(exe, w['appName'])
        new = [
            ['appid', ('i32', aid)], ['AppName', w['appName']], ['Exe', exe],
            ['StartDir', '"' + (w.get('startDir') or os.path.dirname(w['exe'])) + '"'],
            ['icon', w.get('icon') or ''], ['ShortcutPath', ''], ['LaunchOptions', w.get('launchOptions') or ''],
            ['IsHidden', ('i32', int(bool(w.get('hidden'))))], ['AllowDesktopConfig', ('i32', int(w.get('allowDesktopConfig', True)))],
            ['AllowOverlay', ('i32', int(w.get('allowOverlay', True)))], ['OpenVR', ('i32', int(bool(w.get('openVR'))))],
            ['Devkit', ('i32', 0)], ['DevkitGameID', ''], ['DevkitOverrideAppID', ('i32', 0)],
            ['LastPlayTime', ('i32', 0)], ['FlatpakAppID', ''],
            ['tags', [[str(n), t] for n, t in enumerate(w.get('tags') or [])]],
        ]
        old = next((e for e in entries if appid_of(e) == aid), None)
        if old is not None:
            keep = {k.lower(): v for k, v in old if k.lower() in ('lastplaytime',)}
            for kv in new:
                if kv[0].lower() in keep:
                    kv[1] = keep[kv[0].lower()]
            old[:] = new
        else:
            entries.append(new)
    root[1] = [[str(n), e] for n, e in enumerate(entries)]
    data = bkv_dump(items)
    try:
        if open(path, 'rb').read() == data:
            return False
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not os.path.exists(path + '.nixos-steam.bak'):
        with open(path, 'rb') as a, open(path + '.nixos-steam.bak', 'wb') as b_:
            b_.write(a.read())
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='.nixos-steam.')
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
    os.replace(tmp, path)
    return True


# ---------------------------------------------------------------- libraries / manifests
def library_paths(root):
    paths = [root]
    p = os.path.join(root, 'steamapps', 'libraryfolders.vdf')
    try:
        items = parse(open(p, encoding='utf-8', errors='replace').read())
    except FileNotFoundError:
        return paths
    for k, v in items:
        if k.lower() == 'libraryfolders' and isinstance(v, list):
            for _, f in v:
                if isinstance(f, list):
                    for fk, fv in f:
                        if fk.lower() == 'path' and isinstance(fv, str) and fv not in paths:
                            paths.append(fv)
    return paths


def apply_library_folders(root, wanted):
    """Ensure each wanted library folder is registered (existing folders and their bookkeeping are kept)."""
    import random
    p = os.path.join(root, 'steamapps', 'libraryfolders.vdf')
    try:
        items = parse(open(p, encoding='utf-8', errors='replace').read())
    except FileNotFoundError:
        items = []
    top = next((kv for kv in items if kv[0].lower() == 'libraryfolders' and isinstance(kv[1], list)), None)
    if top is None:
        top = ['libraryfolders', []]
        items.append(top)
    folders = [v for _, v in top[1] if isinstance(v, list)]

    def path_of(f):
        return next((v for k, v in f if k.lower() == 'path'), None)

    if not any(os.path.realpath(path_of(f) or '') == os.path.realpath(root) for f in folders):
        folders.insert(0, [['path', root], ['label', ''], ['contentid', str(random.getrandbits(63))], ['totalsize', '0'], ['apps', []]])
    changed = False
    for w in wanted:
        hit = next((f for f in folders if os.path.realpath(path_of(f) or '') == os.path.realpath(w['path'])), None)
        if hit is None:
            hit = [['path', w['path']], ['label', w.get('label') or ''], ['contentid', str(random.getrandbits(63))],
                   ['totalsize', '0'], ['apps', []]]
            folders.append(hit)
            changed = True
        elif w.get('label') is not None:
            changed |= set_path(hit, ['label'], w['label'])
        lib_vdf = os.path.join(w['path'], 'libraryfolder.vdf')
        if not os.path.exists(lib_vdf):
            cid = next(v for k, v in hit if k.lower() == 'contentid')
            write_atomic(lib_vdf, dump([['libraryfolder', [['contentid', cid], ['label', w.get('label') or '']]]]))
            changed = True
        os.makedirs(os.path.join(w['path'], 'steamapps'), exist_ok=True)
    top[1] = [[str(n), f] for n, f in enumerate(folders)]
    if changed:
        write_atomic(p, dump(items))
    return changed


# ---------------------------------------------------------------- managed plain files
STATE = '.nixos-steam-managed.json'


def apply_files(root, files):
    """files: {relative path: content or null}. Files created earlier but no longer configured are removed."""
    state_path = os.path.join(root, STATE)
    try:
        managed = set(json.load(open(state_path)))
    except (FileNotFoundError, ValueError):
        managed = set()
    log = []
    for rel, content in files.items():
        p = os.path.join(root, rel)
        if content is None:
            continue
        if not os.path.exists(p) or open(p, encoding='utf-8', errors='replace').read() != content:
            if os.path.exists(p) and rel not in managed:
                print(f'steam-config-apply: not overwriting unmanaged {rel}', file=sys.stderr)
                continue
            write_atomic(p, content)
            log.append(rel)
        managed.add(rel)
    for rel in sorted(managed - {k for k, v in files.items() if v is not None}):
        p = os.path.join(root, rel)
        if os.path.exists(p):
            os.remove(p)
            log.append(rel + ' (removed)')
        managed.discard(rel)
    if managed or os.path.exists(state_path):
        write_atomic(state_path, json.dumps(sorted(managed)))
    return log


def main():
    cfg = json.load(open(sys.argv[1]))
    home = os.environ['HOME']
    if steam_running(home):
        print('steam-config-apply: Steam is running, not touching config files', file=sys.stderr)
        return
    root = cfg.get('steamRoot')
    if not root:
        link = os.path.join(home, '.steam', 'steam')
        root = os.path.realpath(link) if os.path.exists(link) else os.path.join(home, '.local', 'share', 'Steam')

    by_store = {}
    for s in cfg.get('settings', []):
        by_store.setdefault(s['store'], []).append((s['key'], s['value']))

    log = []
    if by_store.get('install'):
        if apply_file(os.path.join(root, 'config', 'config.vdf'), ROOTS['install'], by_store['install']):
            log.append('config/config.vdf')
    if by_store.get('registry'):
        if apply_file(os.path.join(home, '.steam', 'registry.vdf'), ROOTS['registry'],
                      [(registry_path(k), v) for k, v in by_store['registry']]):
            log.append('~/.steam/registry.vdf')

    if cfg.get('libraryFolders'):
        if apply_library_folders(root, cfg['libraryFolders']):
            log.append('steamapps/libraryfolders.vdf')

    # per-app manifests: store "appmanifest:<appid>", only for installed apps (in any library)
    manifests = {k.split(':', 1)[1]: v for k, v in by_store.items() if k.startswith('appmanifest:')}
    if manifests:
        libs = library_paths(root)
        for appid, entries in manifests.items():
            for lib in libs:
                mp = os.path.join(lib, 'steamapps', f'appmanifest_{appid}.acf')
                if os.path.exists(mp) and apply_file(mp, 'AppState', entries):
                    log.append(mp)

    udir = os.path.join(root, 'userdata')
    ids = cfg.get('userIds') or ([d for d in os.listdir(udir) if d.isdigit() and d != '0'] if os.path.isdir(udir) else [])
    for uid in ids:
        if not os.path.isdir(os.path.join(udir, uid)):
            continue
        if by_store.get('local') and apply_file(os.path.join(udir, uid, 'config', 'localconfig.vdf'), ROOTS['local'], by_store['local']):
            log.append(f'userdata/{uid}/config/localconfig.vdf')
        if by_store.get('roaming') and apply_file(os.path.join(udir, uid, '7', 'remote', 'sharedconfig.vdf'), ROOTS['roaming'], by_store['roaming']):
            log.append(f'userdata/{uid}/7/remote/sharedconfig.vdf')
        if cfg.get('shortcuts') and apply_shortcuts(os.path.join(udir, uid, 'config', 'shortcuts.vdf'), cfg['shortcuts']):
            log.append(f'userdata/{uid}/config/shortcuts.vdf')
        for rel, src in (cfg.get('userFiles') or {}).items():
            dst = os.path.join(udir, uid, rel)
            data = open(src, 'rb').read()
            try:
                if open(dst, 'rb').read() == data:
                    continue
            except FileNotFoundError:
                pass
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dst), prefix='.nixos-steam.')
            with os.fdopen(fd, 'wb') as f:
                f.write(data)
            os.replace(tmp, dst)
            log.append(f'userdata/{uid}/{rel}')

    scfg = cfg.get('steamCfg')
    if scfg is not None:
        path = os.path.join(root, 'steam.cfg')
        managed = os.path.exists(path) and open(path).read().startswith(MANAGED_MARK)
        if scfg:
            text = MANAGED_MARK + ''.join(f'{k}={v}\n' for k, v in sorted(scfg.items()))
            if not os.path.exists(path) or open(path).read() != text:
                write_atomic(path, text)
                log.append('steam.cfg')
        elif managed:
            os.remove(path)
            log.append('steam.cfg (removed)')

    log += apply_files(root, cfg.get('files') or {})
    if log:
        print('steam-config-apply: updated ' + ', '.join(log), file=sys.stderr)


if __name__ == '__main__':
    main()
