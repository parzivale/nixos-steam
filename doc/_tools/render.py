#!/usr/bin/env python3
"""Render records.json (from aggregate.py) into Markdown reference pages under out/doc/binaries/."""
import collections, json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out/doc/binaries'
JUNK = {'Unknown', 'Steam3Master', '-inf',
        # not settings: VGUI panel messages, D-Bus names and Vulkan layer ids caught by the ConVar-shape heuristic
        'com.steampowered.Atomupd1', 'org.freedesktop.DBus', 'CursorMoved', 'ItemsChecked', 'KeyCodeTyped', 'MouseDoublePressed',
        'MousePressed', 'OnCursorMoved', 'OnScreenSizeChanged', 'WrapPanelItemVisibility', 'ClickPanel',
        'VK_LAYER_VALVE_steam_fossilize_32', 'VK_LAYER_VALVE_steam_fossilize_64', 'VK_LAYER_VALVE_steam_overlay_32', 'VK_LAYER_VALVE_steam_overlay_64'}
recs = [r for r in json.load(open('records.json')) if r['name'] not in JUNK]


DESC = {}
for _p in ('desc/convars.json', 'desc/commands-and-switches.json', 'desc/env-hints-atoms.json'):
    if os.path.exists(_p):
        DESC.update(json.load(open(_p)))


def what(kind, name):
    d = DESC.get(f'{kind}:{name}')
    if not d:
        return ''
    tag = '' if d.get('basis') == 'valve-help' and d.get('confidence') == 'high' else f" *({d.get('confidence', '?')})*"
    return esc(d['what']) + tag


def esc(x):
    if x is None:
        return ''
    return str(x).replace('|', '\\|').replace('\n', '\\n').replace('\t', '\\t')


def code(x):
    return f'`{esc(x)}`' if x not in (None, '') else ''


def short(b):
    return b.split('/', 1)[1]


def group(kind):
    g = collections.OrderedDict()
    for r in sorted((r for r in recs if r['kind'] == kind), key=lambda r: r['name'].lstrip('@-').lower()):
        e = g.setdefault(r['name'], dict(name=r['name'], values=[], helps=[], flags=set(), binaries=set(), access=set()))
        if r.get('value') not in (None, '') and r['value'] not in e['values']:
            e['values'].append(r['value'])
        if r.get('help') and r['help'] not in e['helps']:
            e['helps'].append(r['help'])
        if r.get('flags') is not None:
            e['flags'].add(r['flags'])
        e['binaries'].add(short(r['binary']))
        if r.get('access'):
            e['access'].add(r['access'])
    return g


def bins(e):
    return ', '.join(sorted(e['binaries']))


HEADER = ('> **What it does** is written from how the option is used in the code (strings and log messages near each\n'
          '> read site, related options, Valve help). The confidence tag *(high/medium/low)* follows each inferred description.\n'
          '> Untagged descriptions restate Valve\'s own help text.\n>\n'
          '> Generated from the Steam Linux client, bootstrap manifest version **{ver}**, by static analysis of the\n'
          '> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.\n\n')
VER = open('manifest.vdf').read().split('"version"')[1].split('"')[1]


def write(name, title, intro, body):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w') as w:
        w.write(f'# {title}\n\n' + HEADER.format(ver=VER) + intro + '\n\n' + body)


# ---- command line
g = group('cli')
urls = {k: v for k, v in g.items() if not k.startswith(('-', '+'))}
g = {k: v for k, v in g.items() if k.startswith(('-', '+'))}
rows = ['| Switch | What it does | Valve help text | How it is read | Binaries |', '|---|---|---|---|---|']
for e in g.values():
    rows.append(f'| {code(e["name"])} | {what("cli", e["name"])} | {esc(" / ".join(e["helps"]))} | {esc("; ".join(sorted(e["access"])))} | {bins(e)} |')
documented = sum(1 for e in g.values() if e['helps'])
write('command-line.md', 'Command-line switches',
      f'Every command-line switch the client binaries test for: **{len(g)}** switches, **{documented}** of which carry a\n'
      'help string that Valve registered through `SteamStdLib::CCommandLineParam(name, help)`.\n\n'
      'You pass these to the `steam` launcher (e.g. `steam -dev -console`). `steam.sh` and the bootstrapper forward\n'
      'unrecognised arguments to the client. Read-method legend:\n\n'
      '* **registered (CCommandLineParam)**: declared with help text. These are the switches Valve formally documents internally.\n'
      '* **exists / value**: `Plat_CommandLineParamExists` / `Plat_CommandLineParamValue` (tier0). `value` switches take an argument (`-switch <value>`).\n'
      '* **internal parser**: a private argv parser, e.g. in the `steam` bootstrapper.\n'
      '* **checked (virtual ICommandLine call, inferred)**: a `"-switch"` literal passed to a virtual `ICommandLine` method (`FindParm`/`ParmValue`). The method is inferred from the call shape.\n'
      '* **compared against argv (inferred)**: a literal compared with `strcmp`-style functions, typically in argv loops.\n'
      + (f'\nThe analysis also found these protocol URLs used as launch arguments: {", ".join(code(k) for k in urls)}.\n' if urls else ''),
      '\n'.join(rows) + '\n')

# ---- convars / concommands
for kind, fname, title, intro in [
    ('convar', 'convars.md', 'Console variables (ConVars)',
     'Every ConVar registered in the client binaries, recovered from the arguments of the static ConVar\n'
     'constructors. You can set these in the Steam console (`steam://open/console`, or run with `-console`/`-dev`)\n'
     'as `name value`, or on the command line as `+name value`.\n\n'
     '**Name prefixes (Valve naming convention):** `b` = bool, `n` = int, `fl`/`f` = float, `s` = string.\n'
     'A leading `@` marks a client-config convar. Steam can override these from the server-side client\n'
     'configuration it downloads at login (inferred from usage). Many are internal tuning knobs that never\n'
     'appear in any UI. **Flags** is the raw flags bitmask passed to the constructor.'),
    ('concommand', 'console-commands.md', 'Console commands (ConCommands)',
     'Every console command registered in the client binaries (name and help text). Run them in the Steam\n'
     'console (`steam://open/console`).'),
]:
    g = group(kind)
    if kind == 'convar':
        rows = ['| Name | Default | What it does | Valve help text | Flags | Binaries |', '|---|---|---|---|---|---|']
        for e in g.values():
            fl = ', '.join(hex(f) for f in sorted(e['flags']))
            rows.append(f'| {code(e["name"])} | {" / ".join(code(v) for v in e["values"])} | {what(kind, e["name"])} | {esc(" / ".join(e["helps"]))} | {fl} | {bins(e)} |')
    else:
        rows = ['| Command | What it does | Valve help text | Binaries |', '|---|---|---|---|']
        for e in g.values():
            rows.append(f'| {code(e["name"])} | {what(kind, e["name"])} | {esc(" / ".join(e["helps"]))} | {bins(e)} |')
    write(fname, title, intro + f'\n\nTotal: **{len(g)}**.', '\n'.join(rows) + '\n')

# ---- environment
g = group('env')
rows = ['| Variable | What it does | Access | Value seen at call site | Binaries |', '|---|---|---|---|---|']
for e in g.values():
    rows.append(f'| {code(e["name"])} | {what("env", e["name"])} | {esc("; ".join(sorted(e["access"])))} | {" / ".join(code(v) for v in e["values"])} | {bins(e)} |')
body = '\n'.join(rows) + '\n'
ge = group('game-env')
rows = ['| Variable | What it does | Value written (if constant) |', '|---|---|---|']
for e in ge.values():
    rows.append(f'| {code(e["name"])} | {what("game-env", e["name"])} | {" / ".join(code(v) for v in e["values"])} |')
body += ('\n## Environment Steam sets for launched games\n\n'
         'Steam builds a launch environment for every game process (`steamclient.so`). The table lists every variable\n'
         'name passed to that setter. An empty value means the client computes it at runtime (paths, app IDs and so on).\n'
         'Games, Proton, pressure-vessel and the overlay read these. On NixOS they matter for FHS/steam-run wrappers.\n\n'
         + '\n'.join(rows) + '\n')
write('environment.md', 'Environment variables',
      f'**{len(g)}** environment variables that the client binaries read or set (`getenv`, `secure_getenv`,\n'
      '`setenv`, the `boolean_env` helper in `steam-launch-wrapper`, the SDR/SteamNetworkingSockets env accessor),\n'
      f'plus **{len(ge)}** variables injected into game processes. Valve ships no descriptions for env vars, so most\n'
      'have none. The names are usually self-explanatory, and many are also handled in the shell scripts\n'
      '(see [../launcher/](../launcher/)).', body)

# ---- SDL hints / X11 atoms
g = group('sdl-hint')
rows = ['| Hint | What it does | Access | Value set | Binaries |', '|---|---|---|---|---|']
for e in g.values():
    rows.append(f'| {code(e["name"])} | {what("sdl-hint", e["name"])} | {esc("; ".join(sorted(e["access"])))} | {" / ".join(code(v) for v in e["values"])} | {bins(e)} |')
write('sdl-hints.md', 'SDL hints',
      f'**{len(g)}** SDL3 hints that Steam sets or reads internally (`SDL_SetHint` and wrappers). Every SDL hint can\n'
      'also be overridden with an environment variable of the same name, which makes them user-configurable.',
      '\n'.join(rows) + '\n')
g = group('x11-atom')
rows = ['| Atom / property | What it does | Binaries |', '|---|---|---|']
for e in g.values():
    rows.append(f'| {code(e["name"])} | {what("x11-atom", e["name"])} | {bins(e)} |')
write('x11-atoms.md', 'X11 atoms and gamescope properties',
      f'**{len(g)}** `STEAM_*`/`GAMESCOPE_*` X11 atoms that the client interns or sets. These are how Steam talks to\n'
      'gamescope (Steam Deck / SteamOS game mode) and to the window manager: frame limits, VRR, HDR, blur,\n'
      'ReShade effects and so on. Values are set at runtime.',
      '\n'.join(rows) + '\n')
print('ok')
