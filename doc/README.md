# Steam client configuration reference

This is an exhaustive catalogue of every configuration option in the **Steam Linux client**, public and
non-public, recovered by analysing the client itself. It is the groundwork for `nixos-steam`: knowing every
knob is the first step toward configuring Steam declaratively on NixOS.

* **Client build:** bootstrap manifest version `1791918634` (`steam_client_ubuntu12`), binaries dated
  2026-10-13, fetched from Valve's update CDN (`client-update.steamstatic.com`) on 2026-10-20.
* **Runtimes:** steamrt3c `3c.0.20260824` (pressure-vessel `0.20260824.0`) and scout `1.0.20260714`.
* **Scope:** the 64-bit client (`steamrt64/`, `ubuntu12_64/`), its shell scripts and runtimes, and the
  `steamui` web frontend. Steam's own binaries were analysed. Bundled third-party libraries
  (FFmpeg, CEF/Chromium internals, SDL internals, OpenSSL) were not, except where Steam configures them.

## Where to look

| I want to… | Read |
|---|---|
| See every setting in the Settings UI, plus the hidden ones, with its storage key and default | [settings/client-settings.md](settings/client-settings.md) (270 settings) |
| Pass flags to `steam` | [binaries/command-line.md](binaries/command-line.md) (255 switches), [launcher/bootstrapper.md](launcher/bootstrapper.md), [launcher/steam-sh.md](launcher/steam-sh.md) |
| Set console variables (`steam://open/console`, `+convar`, `steam_dev.cfg`) | [binaries/convars.md](binaries/convars.md) (464), [binaries/console-commands.md](binaries/console-commands.md) (133), [launcher/steam-dev-cfg-convars.md](launcher/steam-dev-cfg-convars.md) |
| Use environment variables | [binaries/environment.md](binaries/environment.md) (174 read, 103 set for games), [launcher/steam-sh.md](launcher/steam-sh.md), [launcher/steam-runtime.md](launcher/steam-runtime.md) |
| Edit files on disk (`registry.vdf`, `config.vdf`, `localconfig.vdf`, `steam.cfg`, magic files…) | [launcher/on-disk-config-files.md](launcher/on-disk-config-files.md), [launcher/steam-cfg-and-magic-files.md](launcher/steam-cfg-and-magic-files.md) |
| Find developer / Valve-internal UI, `steam://` handlers, URL config params | [steamui/hidden-dev-options.md](steamui/hidden-dev-options.md), [steamui/url-params-and-protocols.md](steamui/url-params-and-protocols.md), [steamui/injected-config.md](steamui/injected-config.md) |
| Look up per-app properties (launch options, compat tool…) and the `SteamClient.*` API | [steamui/steamclient-api-config.md](steamui/steamclient-api-config.md) |
| Look up browser storage keys | [steamui/storage-keys.md](steamui/storage-keys.md) |
| Look up SDL hints and gamescope X11 properties | [binaries/sdl-hints.md](binaries/sdl-hints.md), [binaries/x11-atoms.md](binaries/x11-atoms.md) |
| Look up shader pre-caching (Fossilize) filters and other shipped config files | [launcher/fossilize-filters.md](launcher/fossilize-filters.md) |
| Read the raw protobuf schemas (settings, per-app, Remote Play, etc.) | [protobuf/](protobuf/) (117 `.proto` files recovered from the binaries) |

## Layout

```
doc/
├── settings/   CMsgClientSettings: the canonical settings schema, decoded from its protobuf custom options
├── binaries/   options recovered by disassembling Steam's ELF binaries (CLI, convars, commands, env, hints, atoms)
├── launcher/   steam.sh, bootstrapper, steam-runtime/pressure-vessel, steam.cfg, magic files, on-disk VDFs
├── steamui/    the React UI (steamui/*.js): JS-side settings, hidden dev pages, storage, URL params, SteamClient API
├── protobuf/   every embedded .proto descriptor, as text
└── _tools/     the scripts that produced binaries/, settings/ and protobuf/ (re-run them on a new build)
```

## Method

1. **Client settings.** `steamui.so` embeds the serialized protobuf descriptor
   `steammessages_clientsettings.proto`. Its fields carry custom options (`setting_store`, `setting_name`,
   `setting_default_*`, `setting_pre_login`, `setting_clamp_*`, `setting_description`, `setting_profile_mode`),
   which give the exact store and key each setting is persisted under, plus its default. This source is
   authoritative.
2. **Binaries.** Steam's 64-bit ELF files keep their dynamic imports but are otherwise stripped. A small
   capstone-based disassembler ([_tools/callargs.py](_tools/callargs.py)) records the constant arguments at
   every call site. Registrations are then recognised by callee:
   * `SteamStdLib::CCommandLineParam(name, help)`: switches Valve documents with help text;
   * `Plat_CommandLineParamExists/Value`, virtual `ICommandLine` calls, and argv `strcmp` loops: undocumented switches;
   * the internal ConVar/ConCommand constructors, identified by their `(this, name, default, flags, help)`
     call shape: convars, defaults, flags and help text;
   * `getenv`/`setenv`/`secure_getenv`, plus hand-verified internal accessors: environment variables.
     This includes the setter that builds the environment for game processes.
3. **Scripts, runtimes and data files** (`steam.sh`, steam-runtime/pressure-vessel, `*.vdf`, `*.json`) were
   read directly.
4. **Usage-based descriptions.** Most internal options ship without help text, so a second pass
   ([_tools/usage.py](_tools/usage.py)) collects how each option is *used*. It finds function bounds from
   `.eh_frame_hdr` and gathers the strings referenced near each read site: log messages, related options,
   paths and URLs. For a ConVar it looks at every function that touches the ConVar object, not only where the
   ConVar is registered. Client settings were matched to their UI labels and the JS code that reads them.
   Descriptions were written from that evidence. Each carries a confidence tag: *(high)*, *(medium)* or *(low)*.
   *Low* means the description rests mostly on the option's name. Valve's own help text is always kept in its own column.
5. **steamui.** The minified bundles (`sp.js`, `library.js`, …) were searched for settings access,
   developer-page gating, storage keys, query-parameter handling, `steam://` handlers and `SteamClient.*` calls.
   English labels were joined in from the localization files.

## Caveats

* **Descriptions.** The "Valve help text" and "Valve description" columns are Valve's own strings from the binary.
  "What it does" columns and text marked *inferred* are our interpretation of how the code uses the option.
  Check the confidence tag before relying on one. A *(low)* description is an educated guess from the name.
* **Static analysis limits.** Names built at runtime or read from server-delivered config cannot be seen. The
  `@`-prefixed convars can also be overridden server-side, so the defaults listed are compile-time defaults.
* **Build-specific.** Valve ships client updates often, and options appear and disappear. Re-run
  [_tools/](_tools/) against a newer manifest to refresh the tables.
* **32-bit.** `ubuntu12_32/` holds 32-bit builds of the same components, kept for legacy games. It was spot-checked
  but not disassembled.
* Some options are Valve-internal or debug-only, and changing them can break the client, your account
  session, or a Steam Deck/SteamOS install. This is reference material, not a recommendation.

Steam, the Steam logo and all related names are trademarks of Valve Corporation. This project is not affiliated
with Valve. No Valve binaries or source files are redistributed here. The tables contain only identifiers, short
strings and default values needed to document configuration.
