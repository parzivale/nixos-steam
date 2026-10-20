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
    hive = {'HKEY_CURRENT_USER': 'HKCU', 'HKEY_LOCAL_MACHINE': 'HKLM'}.get(parts[0].upper(), None)
    return '\\'.join([hive] + parts[1:]) if hive else '\\'.join(['HKCU'] + parts)


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
    udir = os.path.join(root, 'userdata')
    ids = cfg.get('userIds') or ([d for d in os.listdir(udir) if d.isdigit() and d != '0'] if os.path.isdir(udir) else [])
    for uid in ids:
        if not os.path.isdir(os.path.join(udir, uid)):
            continue
        if by_store.get('local') and apply_file(os.path.join(udir, uid, 'config', 'localconfig.vdf'), ROOTS['local'], by_store['local']):
            log.append(f'userdata/{uid}/config/localconfig.vdf')
        if by_store.get('roaming') and apply_file(os.path.join(udir, uid, '7', 'remote', 'sharedconfig.vdf'), ROOTS['roaming'], by_store['roaming']):
            log.append(f'userdata/{uid}/7/remote/sharedconfig.vdf')

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
    if log:
        print('steam-config-apply: updated ' + ', '.join(log), file=sys.stderr)


if __name__ == '__main__':
    main()
