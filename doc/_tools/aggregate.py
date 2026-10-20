#!/usr/bin/env python3
"""Classify recovered call sites into config records (convars, commands, CLI switches, env vars).

Reads calls/*.jsonl (from callargs.py) and writes records.json: a list of
{kind, name, value, flags, help, binary, via} entries. Classification is by
call target:
  * known imports (getenv, CCommandLineParam, Plat_CommandLineParam*, SDL hints ...)
  * internal functions whose call sites overwhelmingly carry a registration-shaped
    argument pattern (identifier name in a1 + help text in a4 => ConVar/ConCommand;
    "-switch" literal => command-line parser; ENV_NAME literal => env accessor).
"""
import collections, glob, json, os, re, sys

IDENT = re.compile(r'^@?[A-Za-z_][A-Za-z0-9_.]{1,}$')
ENV = re.compile(r'^[A-Z_][A-Z0-9_]{2,}$')
OPT = re.compile(r'^[-+][A-Za-z][A-Za-z0-9_\-.]+$')

ENV_IMPORTS = {
    'getenv': 'read', 'secure_getenv': 'read', '__secure_getenv': 'read', 'setenv': 'set', 'unsetenv': 'unset',
    'boolean_env': 'read (bool)', 'g_getenv': 'read', 'g_setenv': 'set', 'SDL_getenv': 'read', 'SDL_GetEnvironmentVariable': 'read',
    'SDL_setenv_unsafe': 'set', 'SDL_SetEnvironmentVariable': 'set', 'SDL_getenv_unsafe': 'read',
}
HINT_IMPORTS = {'SDL_SetHint': 'set', 'SDL_SetHintWithPriority': 'set', 'SDL_GetHint': 'read', 'SDL_GetHintBoolean': 'read'}
CLI_IMPORTS = {'Plat_CommandLineParamExists': 'exists', 'Plat_CommandLineParamValue': 'value'}
CCLP = '_ZN11SteamStdLib17CCommandLineParamC1EPKcS2_'
# targets that look env-ish by shape but are not config (tag/atom/crypto tables)
CMP_FUNCS = {'strcmp', 'strcasecmp', 'V_stricmp', 'V_strcmp', 'V_stricmp_fast', 'strncmp', 'V_strnicmp', 'V_strncmp', 'V_stricmp_prefix', 'V_strcmp_prefix'}
NOT_ENV_NAMES = {'XInternAtom', 'V_strnicmp', 'V_stricmp', 'strcmp', 'strcasecmp', 'memcmp', 'fprintf', 'printf', 'strncmp',
                 '__assert_fail', 'g_return_if_fail_warning', 'snprintf', 'V_snprintf', 'sprintf'}


# internal functions (binary, target) verified by hand to be env/hint/property accessors
WHITELIST = {
    ('steamrt64/steamclient.so', '0x24ff380'): ('game-env', 'set in environment of launched games'),
    ('steamrt64/steamclient.so', '0x22782c0'): ('env', 'read (SteamNetworkingSockets/SDR)'),
    ('steamrt64/steamui.so', '0x1b5bac0'): ('x11-atom', 'gamescope X11 property'),
    ('steamrt64/steamwebhelper', '0x7c64d0'): ('sdl-hint', 'set (wrapper)'),
    ('steamrt64/steamui.so', '0x1e30a20'): ('sdl-hint', 'set (wrapper)'),
    ('steamrt64/chromehtml.so', '0x1d0060'): ('env', 'set (CEF crash reporter)'),
}


def s(a, k):
    v = a.get(k)
    return v.get('s') if v else None


def val(a, k):
    v = a.get(k)
    if not v:
        return None
    if 's' in v:
        return v['s']
    if 'i' in v:
        return v['i']
    if 'f' in v:
        return v['f']
    return None


def classify(path):
    binary = os.path.basename(path)[:-len('.jsonl')].replace('__', '/')
    calls = [json.loads(l) for l in open(path)]
    by_target = collections.defaultdict(list)
    for c in calls:
        t = c['target_name'] or (c['target'] and hex(c['target'])) or 'indirect'
        by_target[t].append(c)

    recs = []
    for t, cs in by_target.items():
        n = len(cs)
        if t in ENV_IMPORTS or t in HINT_IMPORTS:
            kind = 'env' if t in ENV_IMPORTS else 'sdl-hint'
            for c in cs:
                a = c['args']
                name = s(a, 'a0')
                if name:
                    recs.append(dict(kind=kind, name=name, value=val(a, 'a1') if 'set' in (ENV_IMPORTS.get(t) or HINT_IMPORTS.get(t)) else val(a, 'a2') if t == 'boolean_env' else None,
                                     access=ENV_IMPORTS.get(t) or HINT_IMPORTS.get(t), binary=binary, via=t, site=c['site']))
            continue
        if t == CCLP:
            for c in cs:
                a = c['args']
                if s(a, 'a1'):
                    recs.append(dict(kind='cli', name=s(a, 'a1'), help=s(a, 'a2'), access='registered (CCommandLineParam)', binary=binary, via='CCommandLineParam', site=c['site']))
            continue
        if t in CLI_IMPORTS:
            for c in cs:
                a = c['args']
                if s(a, 'a0'):
                    recs.append(dict(kind='cli', name=s(a, 'a0'), access=CLI_IMPORTS[t], binary=binary, via=t, site=c['site']))
            continue
        if t == 'indirect':
            # virtual ICommandLine::FindParm/ParmValue/CheckParm(this, "-x", ...)
            for c in cs:
                a = c['args']
                x = s(a, 'a1')
                if x and OPT.match(x) and not any(k for k in a if k not in ('a0', 'a1', 'a2', 'a3') or (k in ('a2', 'a3') and s(a, k) and ' ' in s(a, k))):
                    recs.append(dict(kind='cli', name=x, access='checked (virtual ICommandLine call, inferred)', value=val(a, 'a2'), binary=binary, via='indirect', site=c['site']))
            continue
        if (binary, t) in WHITELIST:
            kind, access = WHITELIST[(binary, t)]
            for c in cs:
                a = c['args']
                for k in ('a0', 'a1'):
                    x = s(a, k)
                    if x and (ENV.match(x) or re.match(r'^[A-Za-z_][A-Za-z0-9_]{2,}$', x)):
                        recs.append(dict(kind=kind, name=x, value=val(a, 'a2' if k == 'a1' else 'a1'), access=access, binary=binary, via=t, site=c['site']))
                        break
            continue
        if t == 'XInternAtom':
            for c in cs:
                x = s(c['args'], 'a1')
                if x and re.match(r'^(STEAM|GAMESCOPE)_', x):
                    recs.append(dict(kind='x11-atom', name=x, access='X11 atom', binary=binary, via=t, site=c['site']))
            continue
        if t in CMP_FUNCS:
            for c in cs:
                for k in ('a0', 'a1'):
                    x = s(c['args'], k)
                    if x and OPT.match(x) and len(x) > 3:
                        recs.append(dict(kind='cli', name=x, access='compared against argv (' + t + ', inferred)', binary=binary, via=t, site=c['site']))
            continue
        if t in NOT_ENV_NAMES or n < 2:
            continue
        # ConVar / ConCommand registration: a1 identifier; a4 help (at least sometimes)
        ident = sum(1 for c in cs if s(c['args'], 'a1') and IDENT.match(s(c['args'], 'a1')))
        helps = sum(1 for c in cs if s(c['args'], 'a4'))
        if n >= 3 and ident / n >= 0.9 and helps / n >= 0.3 and not any(s(c['args'], 'a1', ).startswith('CMsg') for c in cs if s(c['args'], 'a1')):
            cmd = sum(1 for c in cs if 'p' in (c['args'].get('a2') or {})) / n > 0.5
            for c in cs:
                a = c['args']
                if not s(a, 'a1'):
                    continue
                flags = val(a, 'a3')
                recs.append(dict(kind='concommand' if cmd else 'convar', name=s(a, 'a1'), value=None if cmd else val(a, 'a2'),
                                 flags=flags if isinstance(flags, int) else None, help=s(a, 'a4') or (s(a, 'a3') if cmd else None),
                                 binary=binary, via=t, site=c['site']))
            continue
        # help-less ConVar ctor variant: (this=&global, name, default, flags)
        shaped = sum(1 for c in cs if 'p' in (c['args'].get('a0') or {}) and s(c['args'], 'a1') and IDENT.match(s(c['args'], 'a1'))
                     and 'i' in (c['args'].get('a3') or {}))
        named = sum(1 for c in cs if s(c['args'], 'a1') and s(c['args'], 'a1').startswith('@'))
        if n >= 3 and shaped / n >= 0.8 and named >= 1:
            for c in cs:
                a = c['args']
                if s(a, 'a1'):
                    recs.append(dict(kind='convar', name=s(a, 'a1'), value=val(a, 'a2'), flags=val(a, 'a3'), help=None, binary=binary, via=t, site=c['site']))
            continue
        # internal command-line parsers: '-switch' literal in a0 or a1 for (almost) every call
        opt = sum(1 for c in cs if any(s(c['args'], k) and OPT.match(s(c['args'], k)) for k in ('a0', 'a1')))
        if opt / n >= 0.75 and opt >= 2:
            for c in cs:
                a = c['args']
                for k in ('a0', 'a1'):
                    x = s(a, k)
                    if x and OPT.match(x):
                        h = s(a, 'a2') if k == 'a1' else s(a, 'a1')
                        recs.append(dict(kind='cli', name=x, help=h if h and ' ' in h else None, value=None if h and ' ' in h else val(a, 'a2' if k == 'a1' else 'a1'),
                                         access='internal parser', binary=binary, via=t, site=c['site']))
                        break
            continue
        # internal env accessors: ENV_NAME literal in a0/a1 for (almost) every call
        envc = sum(1 for c in cs if any(s(c['args'], k) and ENV.match(s(c['args'], k)) for k in ('a0', 'a1')))
        if False and envc / n >= 0.8 and envc >= 3:
            for c in cs:
                a = c['args']
                for k in ('a0', 'a1'):
                    x = s(a, k)
                    if x and ENV.match(x):
                        recs.append(dict(kind='env?', name=x, value=val(a, 'a2' if k == 'a1' else 'a1'), access='internal accessor (inferred)',
                                         binary=binary, via=t, site=c['site']))
                        break
    return recs


def main():
    recs = []
    for p in sorted(glob.glob('calls/*.jsonl')):
        recs += classify(p)
    json.dump(recs, open('records.json', 'w'), indent=0)
    cnt = collections.Counter(r['kind'] for r in recs)
    print(cnt)
    uniq = collections.Counter((r['kind'], r['name']) for r in recs)
    print('unique', collections.Counter(k for k, _ in uniq))
    vias = collections.Counter((r['binary'], r['via'], r['kind']) for r in recs if r['kind'] == 'env?')
    for (b, v, k), c in vias.most_common():
        ex = [r['name'] for r in recs if r['binary'] == b and r['via'] == v][:6]
        print(f'{c:4d} {b} {v} {ex}')


if __name__ == '__main__':
    main()
