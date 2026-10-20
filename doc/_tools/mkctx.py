#!/usr/bin/env python3
"""Build per-category usage-context files (ctx/*.txt) for writing usage-based descriptions."""
import collections, glob, json, os

JUNK = {'Unknown', 'Steam3Master', '-inf'}
recs = [r for r in json.load(open('records.json')) if r['name'] not in JUNK]
usage = {}
for p in glob.glob('usage/*.json'):
    b = os.path.basename(p)[:-5].replace('__', '/')
    try:
        d = json.load(open(p))
    except Exception:
        continue
    for k, v in d.items():
        usage.setdefault(k, []).extend((b, x) for x in v)

items = collections.OrderedDict()
for r in sorted(recs, key=lambda r: (r['kind'], r['name'].lstrip('@-').lower())):
    k = f"{r['kind']}:{r['name']}"
    e = items.setdefault(k, dict(kind=r['kind'], name=r['name'], help=[], values=[], binaries=set(), access=set()))
    if r.get('help') and r['help'] not in e['help']:
        e['help'].append(r['help'])
    if r.get('value') not in (None, '') and r['value'] not in e['values']:
        e['values'].append(r['value'])
    e['binaries'].add(r['binary'].split('/', 1)[1])
    if r.get('access'):
        e['access'].add(r['access'])

CATS = {
    'convars': ['convar'],
    'commands-and-switches': ['concommand', 'cli'],
    'env-hints-atoms': ['env', 'game-env', 'sdl-hint', 'x11-atom'],
}
os.makedirs('ctx', exist_ok=True)
for cat, kinds in CATS.items():
    with open(f'ctx/{cat}.txt', 'w') as w:
        n = 0
        for k, e in items.items():
            if e['kind'] not in kinds:
                continue
            n += 1
            w.write(f"### {k}\n")
            if e['help']:
                w.write(f"valve_help: {' / '.join(e['help'])}\n")
            if e['values']:
                w.write(f"value/default: {e['values']}\n")
            w.write(f"binaries: {', '.join(sorted(e['binaries']))}; access: {'; '.join(sorted(e['access']))}\n")
            seen = []
            for b, u in usage.get(k, [])[:8]:
                for s in u['strings']:
                    s = s.replace('\n', '\\n')[:160]
                    if s not in seen and s != e['name']:
                        seen.append(s)
            if seen:
                w.write('usage_strings: ' + ' | '.join(seen[:45]) + '\n')
            w.write('\n')
    print(cat, n, os.path.getsize(f'ctx/{cat}.txt'))
