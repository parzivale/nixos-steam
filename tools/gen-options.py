#!/usr/bin/env python3
"""Generate data/*.json (consumed by modules/client.nix) from the extraction pipeline in doc/_tools.

Usage (from the extraction work dir that holds records.json and the unpacked client under root/):
  gen-options.py <repo-dir>

Inputs:
  records.json                         call-site records (aggregate.py)
  root/steamrt64/steamui.so            for the CMsgClientSettings descriptor (via protodump.extract)
  <repo>/doc/_tools/descriptions/*.json usage-based descriptions
Outputs:
  <repo>/data/settings.json  <repo>/data/switches.json  <repo>/data/convars.json  <repo>/data/environment.json
"""
import json, os, re, struct, sys

repo = sys.argv[1]
sys.path.insert(0, os.path.join(repo, 'doc', '_tools'))
from protodump import extract  # noqa: E402
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory  # noqa: E402

D = os.path.join(repo, 'doc', '_tools', 'descriptions')
desc = {}
for f in ('convars', 'commands-and-switches', 'env-hints-atoms'):
    desc.update(json.load(open(os.path.join(D, f + '.json'))))
sdesc = json.load(open(os.path.join(D, 'settings.json')))

JUNK = {'Unknown', 'Steam3Master', '-inf', 'com.steampowered.Atomupd1', 'org.freedesktop.DBus', 'CursorMoved',
        'ItemsChecked', 'KeyCodeTyped', 'MouseDoublePressed', 'MousePressed', 'OnCursorMoved', 'OnScreenSizeChanged',
        'WrapPanelItemVisibility', 'ClickPanel', 'VK_LAYER_VALVE_steam_fossilize_32', 'VK_LAYER_VALVE_steam_fossilize_64',
        'VK_LAYER_VALVE_steam_overlay_32', 'VK_LAYER_VALVE_steam_overlay_64'}
recs = [r for r in json.load(open('records.json')) if r['name'] not in JUNK]


def d(kind, name):
    x = desc.get(f'{kind}:{name}') or {}
    return x.get('what', ''), x.get('confidence', '')


def f32(v):
    for p in range(1, 10):
        s = f'{v:.{p}g}'
        if struct.unpack('<f', struct.pack('<f', float(s)))[0] == struct.unpack('<f', struct.pack('<f', v))[0]:
            return float(s)
    return v


def write(name, obj):
    os.makedirs(os.path.join(repo, 'data'), exist_ok=True)
    with open(os.path.join(repo, 'data', name), 'w') as w:
        json.dump(obj, w, indent=1, sort_keys=True)
        w.write('\n')
    print(name, len(obj))


# ---------------------------------------------------------------- settings
found = extract('root/steamrt64/steamui.so')
pool = descriptor_pool.DescriptorPool()
pool.AddSerializedFile(descriptor_pb2.DESCRIPTOR.serialized_pb)
done = {'google/protobuf/descriptor.proto'}


def add(n):
    if n in done or n not in found:
        return
    for dep in found[n].dependency:
        add(dep)
    pool.Add(found[n]); done.add(n)


add('steammessages_clientsettings.proto')
msg = pool.FindMessageTypeByName('CMsgClientSettings')
fo_cls = message_factory.GetMessageClass(pool.FindMessageTypeByName('google.protobuf.FieldOptions'))
ext = {e: pool.FindExtensionByName(e) for e in [
    'setting_store', 'setting_name', 'setting_pre_login', 'setting_default_bool', 'setting_default_int',
    'setting_default_uint', 'setting_default_float', 'setting_default_string', 'setting_readonly',
    'setting_description', 'setting_profile_mode', 'setting_clamp_min', 'setting_clamp_max']}
STORE = {1: 'install', 2: 'roaming', 3: 'local', 4: 'registry'}
settings = {}
skipped = []
for f in msg.fields:
    o = fo_cls(); o.ParseFromString(f.GetOptions().SerializeToString())
    g = lambda k: o.Extensions[ext[k]] if o.HasExtension(ext[k]) else None  # noqa: E731
    store = g('setting_store')
    if store not in STORE or not g('setting_name') or g('setting_readonly') or f.is_repeated:
        skipped.append(f.name)
        continue
    if f.message_type:
        typ = 'hotkey' if f.message_type.name == 'CMsgHotkey' else None
    elif f.enum_type:
        typ = 'enum'
    else:
        typ = {8: 'bool', 5: 'int', 13: 'int', 3: 'int', 4: 'int', 17: 'int', 18: 'int', 2: 'float', 1: 'float', 9: 'string'}.get(f.type)
    if typ is None:
        skipped.append(f.name)
        continue
    default = None
    for k in ('setting_default_bool', 'setting_default_int', 'setting_default_uint', 'setting_default_float', 'setting_default_string'):
        v = g(k)
        if v is not None:
            default = f32(v) if isinstance(v, float) else v
    e = sdesc.get(f.name, {})
    settings[f.name] = dict(
        number=f.number, type=typ, store=STORE[store], key=g('setting_name'), default=default,
        enum={v.name: v.number for v in f.enum_type.values} if f.enum_type else None,
        preLogin=bool(g('setting_pre_login')), perProfile=bool(g('setting_profile_mode')),
        clampMin=g('setting_clamp_min'), clampMax=g('setting_clamp_max'),
        what=e.get('what', ''), ui=e.get('ui', ''), confidence=e.get('confidence', ''),
        valveDescription=g('setting_description') or '')
write('settings.json', settings)
print('  skipped (computed/read-only/no key):', len(skipped))

# ---------------------------------------------------------------- switches
# one-shot actions / per-invocation arguments: valid, but rarely what you want on every launch
SESSION = {'-applaunch', '-gameid', '-gameidlaunch', '-install', '-uninstall', '-login', '-quicklogin', '-rememberpassword',
           '-shutdown', '-exitsteam', '-clearbeta', '-setbeta', '-clientbeta', '-download', '-forcesteamupdate',
           '-forcepackagedownload', '-installupdate', '-pipewire-fresh-start', '-flushconfig', '-accesscode', '-ifrunning',
           '-verifyfiles', '-force-oobe-stage1', '-force-oobe-stage2', '-singleapp', '-forcecontrollerappid'}
# arguments Steam passes to its own helper processes
INTERNAL_SW = {'-pid', '-steampid', '-steamid', '-query', '-query-arg', '-out-file', '-child-update-ui-socket',
               '-child-update-ui', '-master_ipc_name_override', '-srt-logger-opened', '-buildid', '-init_universe'}
# Valve test hooks
TEST_SW = {'-simulatedownloaderrors', '-simulatefatalerror', '-batterytestmode', '-failsystemcheck', '-testupdater',
           '-testoobe', '-testoobestage2', '-testoobeupdater', '-testlongoobeupdater', '-teststoragedata', '-testssa',
           '-testled', '-pretendeol', '-pretendeol32', '-hometest', '-net_fake_state'}
switches = {}
for r in recs:
    if r['kind'] != 'cli' or not r['name'].startswith('-'):
        continue
    e = switches.setdefault(r['name'], dict(arg=False, help='', access=set()))
    if r.get('help'):
        e['help'] = e['help'] or r['help']
    e['access'].add(r.get('access', ''))
for name, e in switches.items():
    what, conf = d('cli', name)
    # a switch takes a value when tier0 reads it with ParamValue, the name ends in '=', or the
    # description documents an argument as `-name <value>`
    e['arg'] = ('value' in e['access'] or name.endswith('=')
                or bool(re.search(re.escape(name) + r'[ =]<', what)))
    e['access'] = sorted(a for a in e['access'] if a)
    e['what'], e['confidence'] = what, conf
    e['kind'] = ('session' if name in SESSION else 'internal' if name in INTERNAL_SW else 'test' if name in TEST_SW else 'persistent')
write('switches.json', switches)

# ---------------------------------------------------------------- convars
convars = {}
for r in recs:
    if r['kind'] != 'convar':
        continue
    e = convars.setdefault(r['name'], dict(default=None, help='', binaries=set()))
    if e['default'] is None and r.get('value') not in (None, ''):
        e['default'] = str(r['value'])
    if r.get('help'):
        e['help'] = e['help'] or r['help']
    e['binaries'].add(r['binary'].split('/', 1)[1])
for name, e in convars.items():
    e['binaries'] = sorted(e['binaries'])
    e['what'], e['confidence'] = d('convar', name)
    n = name.lstrip('@')
    e['type'] = ('bool' if re.match(r'^b[A-Z]', n) else 'int' if re.match(r'^(n|u|c)[A-Z]', n)
                 else 'float' if re.match(r'^(fl|f)[A-Z]', n) else 'string' if re.match(r'^s[A-Z]', n) else 'any')
write('convars.json', convars)

# ---------------------------------------------------------------- environment (+ SDL hints)
env = {}
for r in recs:
    if r['kind'] not in ('env', 'sdl-hint'):
        continue
    e = env.setdefault(r['name'], dict(kind=r['kind'], access=set(), binaries=set()))
    e['access'].add(r.get('access', ''))
    e['binaries'].add(r['binary'].split('/', 1)[1])
for name, e in env.items():
    e['access'] = sorted(a for a in e['access'] if a)
    e['binaries'] = sorted(e['binaries'])
    e['what'], e['confidence'] = d(e['kind'], name)
# variables documented from the launcher/runtime scripts (research/runtime-environment.json)
RT = 'research/runtime-environment.json'
runtime = json.load(open(RT)) if os.path.exists(RT) else {}
for name, r in runtime.items():
    if r['target'] in ('steam', 'both') and name not in env:
        env[name] = dict(kind='runtime', access=['read by ' + r['source']], binaries=[], what=r['what'],
                         confidence=r['confidence'], type=r['type'], values=r.get('values'))
write('environment.json', env)

# ---------------------------------------------------------------- environment Steam builds for games
genv = {}
for r in recs:
    if r['kind'] != 'game-env':
        continue
    e = genv.setdefault(r['name'], dict(values=[]))
    if r.get('value') not in (None, '') and str(r['value']) not in e['values']:
        e['values'].append(str(r['value']))
for name, e in genv.items():
    e['what'], e['confidence'] = d('game-env', name)
for name, r in runtime.items():
    if r['target'] in ('game', 'both') and name not in genv:
        genv[name] = dict(values=[], what=r['what'], confidence=r['confidence'], type=r['type'], enum=r.get('values'),
                          source=r['source'])
write('game-environment.json', genv)
