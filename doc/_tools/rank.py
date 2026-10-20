#!/usr/bin/env python3
"""Rank call targets in a calls/*.jsonl by how much their arguments look like config registrations."""
import collections, json, re, sys

IDENT = re.compile(r'^@?[A-Za-z_][A-Za-z0-9_.]{2,}$')
ENV = re.compile(r'^[A-Z][A-Z0-9_]{2,}$')
OPT = re.compile(r'^[-+][A-Za-z][A-Za-z0-9_\-.]*$')

path = sys.argv[1]
stats = collections.defaultdict(lambda: collections.Counter())
samples = collections.defaultdict(list)
for line in open(path):
    c = json.loads(line)
    t = c['target_name'] or (hex(c['target']) if c['target'] else 'indirect')
    a = c['args']
    s = {k: v.get('s') for k, v in a.items() if 's' in v}
    st = stats[t]
    st['calls'] += 1
    if s.get('a1') and IDENT.match(s['a1']) and any(v and ' ' in v for k, v in s.items() if k in ('a2', 'a3', 'a4', 'a5')):
        st['name+help'] += 1
    if any(v and ENV.match(v) for v in s.values()):
        st['env'] += 1
    if any(v and OPT.match(v) for v in s.values()):
        st['opt'] += 1
    if len(samples[t]) < 3 and s:
        samples[t].append(s)

for key in ('name+help', 'env', 'opt'):
    print(f'== top by {key}')
    for t, st in sorted(stats.items(), key=lambda kv: -kv[1][key])[:12]:
        if st[key] < 3:
            break
        print(f'{st[key]:5d}/{st["calls"]:<6d} {t:28s} {json.dumps(samples[t][:2])[:220]}')
