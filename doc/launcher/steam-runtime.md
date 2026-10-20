# Steam Runtime scripts (steamrt3c / pressure-vessel and legacy scout)

Steam Linux client, manifest `1791918634`.

## Method and sources

The runtime payloads are not in the main client zips. I downloaded two packages from `client-update.steamstatic.com`, as listed in `manifest.vdf`:

* `runtime_steamrt_ubuntu12.zip.e9edd732…` (127.6 MB). It contains:
  * `steamrt64/pv-run.sh`
  * `steamrt64/pv-runtime/steam-runtime-steamrt.sh`
  * an unpacked `steamrt64/pv-runtime/steam-runtime-steamrt/`
  * versions: depot `3c.0.20260824.257593`, pressure-vessel `0.20260824.0`
* `runtime_scout_ubuntu12.zip.96f38007…` (63.5 MB). It contains `ubuntu12_32/steam-runtime.tar.xz` plus `.checksum` (scout `1.0.20260714.251828`), which I unpacked.

I read every shell script in these packages. For the ELF tools (`pressure-vessel-wrap`, `srt-logger`, `steam-runtime-*`, `srt-client-container`, and others) I enumerated environment variable names with `strings`. Where I describe what those variables do, the source is the upstream steam-runtime-tools / pressure-vessel documentation (pressure-vessel-wrap(1), srt-logger(1)), and these entries are marked **(upstream doc)**. Anything else marked **(inferred)** is my interpretation.

The tables below list every script that ships with these runtimes.

### steamrt3c (SteamRT 3 "sniper"-based, used by the 64-bit client)

| Script | Purpose |
|---|---|
| `steamrt64/pv-run.sh` | Developer wrapper: runs a command inside the steamrt3c container through `srt-client-container`. |
| `steamrt64/pv-runtime/steam-runtime-steamrt.sh` | Unpacks `steam-runtime-steamrt.tar.xz` when its version changes, prints the entry point, and can optionally exec a command. |
| `…/steam-runtime-steamrt/_v2-entry-point` | Standard SLR entry point, used for the webhelper and for games. |
| `…/steam-runtime-steamrt/run` | Generated file. Sets the `PRESSURE_VESSEL_*` runtime selection and execs `pressure-vessel-unruntime`. |
| `…/pressure-vessel/bin/pressure-vessel-unruntime` | Strips the scout LDLP environment, then execs `pressure-vessel-wrap`. |
| `…/pressure-vessel/bin/steam-runtime-launch-options` | Wrapper for the developer/debug launch-options GUI, `launch-options.py`. |
| `…/pressure-vessel/libexec/steam-runtime-tools-0/logger-0.bash` | Meant to be sourced. Redirects the calling shell's stdout and stderr to `srt-logger`. |
| `…/libexec/steam-runtime-tools-0/launch-options.py` | GTK launch-options dialog (2290 lines). |

### Scout (Steam Runtime 1, LD_LIBRARY_PATH runtime, used by the legacy ubuntu12_32 client)

| Script | Purpose |
|---|---|
| `run.sh` | Builds `LD_LIBRARY_PATH` (host paths first, then pinned libs, then runtime libs) and execs a command. |
| `setup.sh` | Pins host libraries that are newer than the runtime's copies, using `pinned_libs_{32,64}`. |
| `scripts/switch-runtime.sh` | Switches from scout to another runtime. |
| `scripts/check-*.sh`, `scripts/fix-*.sh` | Build/QA consistency checks. Not used at runtime. |
| `{amd64,i386}/usr/bin/steam-runtime-dialog` | zenity-compatible dialog shim. |
| `{amd64,i386}/usr/bin/steam-runtime-launch-options` | Same role as the steamrt3c wrapper. |

---

## 1. steamrt3c environment variables (shell scripts)

| Variable | Script | R/W | Default | Effect |
|---|---|---|---|---|
| `STEAM_LINUX_RUNTIME_VERBOSE` | `_v2-entry-point`, `pv-run.sh` | R | unset/0 | `1`: verbose output from the entry point. Also exports `PRESSURE_VESSEL_VERBOSE=1`. In pv-run.sh it enables `verbose` messages. |
| `STEAM_LINUX_RUNTIME_LOG` | `_v2-entry-point` | R | unset | `1`: sends output to a log file (`--log-to-file`) and adds timestamps. The file is `$log_dir/slr-app<APPID>-t<YYYYmmddTHHMMSS>.log` (`slr-non-steam-game-…` when there is no app ID), with `slr-latest.log` as a symlink to it. Also exports `PRESSURE_VESSEL_LOG_INFO=1` and `PRESSURE_VESSEL_LOG_WITH_TIMESTAMP=1`. |
| `STEAM_LINUX_RUNTIME_KEEP_LOGS` | `_v2-entry-point` | R | unset | `1`: don't delete older `slr-<app>-*.log` files for the same app. |
| `SRT_LOG_ROTATION` | `_v2-entry-point`, `srt-logger` | R | unset | `0`: same effect as `KEEP_LOGS`. In srt-logger it disables log rotation. |
| `STEAM_LINUX_RUNTIME_LOG_DIR` | `_v2-entry-point` | R | `$PRESSURE_VESSEL_VARIABLE_DIR`, otherwise `<runtime>/var` | Directory for the SLR log files. |
| `PRESSURE_VESSEL_VARIABLE_DIR` | `_v2-entry-point`, `run` | R | `<runtime>/var` | Where mutable copies of the runtime and logs are kept. Passed as `--variable-dir`. |
| `STEAM_COMPAT_APP_ID` / `SteamAppId` | `_v2-entry-point`, `steam-runtime-launch-options` | R | — | App ID used in log names. launch-options uses it to wrap the GUI with `reaper SteamLaunch AppId=<id>`. |
| `LD_PRELOAD` | `_v2-entry-point`, `pressure-vessel-unruntime` | R/W | — | Captured, unset, and passed as `--ld-preloads=…` and `--env-if-host=LD_PRELOAD=…`. Overlay preloads get special handling inside pressure-vessel. |
| `LD_AUDIT` | `pressure-vessel-unruntime` | R/W | — | Same pattern, passed as `--ld-audits`. |
| `LD_LIBRARY_PATH` | `_v2-entry-point`, `unruntime` | R/W | — | Entries under `$STEAM_RUNTIME` (scout) are removed. What remains becomes `PRESSURE_VESSEL_APP_LD_LIBRARY_PATH`, i.e. the game's own `LD_LIBRARY_PATH=… %command%` additions. Then unset. |
| `PRESSURE_VESSEL_APP_LD_LIBRARY_PATH` | `_v2-entry-point` (W), `unruntime` (R) | R/W | — | Library path the game should see inside the container. |
| `STEAM_RUNTIME` | all | R/W | — | If it is an absolute path (scout in use), the scout environment is undone: `PATH` is reset to the system default or `SYSTEM_PATH`, and `LD_LIBRARY_PATH` is restored from `SYSTEM_LD_LIBRARY_PATH`. The variable is then unset. |
| `SYSTEM_PATH`, `SYSTEM_LD_LIBRARY_PATH`, `STEAM_RUNTIME_LIBRARY_PATH`, `SYSTEM_ZENITY` | `unruntime`, `steam-runtime-steamrt.sh`, launch-options | R | — | Host values saved by steam.sh. They are forwarded with `--env-if-host=…`, so a command run with `--host` gets them back. |
| `STEAM_ZENITY` | `steam-runtime-steamrt.sh`, launch-options | R/W | — | Progress-dialog binary used while unpacking. Unset if it points inside the scout runtime. If `~/.steam/root/steam-dialog` is executable, that is preferred. |
| `STEAM_COMPAT_MACHINE_ARCHITECTURE` | `_v2-entry-point` | R | — | Together with `STEAM_COMPAT_EMULATOR` and `STEAM_COMPAT_GRAPHICS_PROVIDER` (both must be existing files), selects `pressure-vessel-arm64` or `pressure-vessel-amd64` and re-execs through `<arch>-exec`. This is the FEX/ARM emulation path. Values: `aarch64-linux-gnu`, `x86_64-linux-gnu`. |
| `STEAM_COMPAT_EMULATOR`, `STEAM_COMPAT_GRAPHICS_PROVIDER` | `_v2-entry-point`, `pressure-vessel-wrap` | R | — | See above. They are also read directly by pressure-vessel. |
| `PRESSURE_VESSEL_PREFIX` | `_v2-entry-point`, `run`, launch-options.py | R/W | `<runtime>/pressure-vessel` | Alternative pressure-vessel installation. |
| `PRESSURE_VESSEL_BATCH` | `_v2-entry-point`, steamwebhelper.sh | W | — | Set to `1` for `--verb=run` (not the main game process). In batch mode only stderr goes to the log file. |
| `PRESSURE_VESSEL_ARCHITECTURES` | `run` | W | `x86_64-linux-gnu:i386-linux-gnu` | Multiarch tuples that get graphics drivers. |
| `PRESSURE_VESSEL_COPY_RUNTIME` | `run` | W | `1` | Makes a mutable copy of the runtime under the variable dir. |
| `PRESSURE_VESSEL_RUNTIME` | `run` | W | `steamrt3c_platform_3c.0.20260824.257593` | Runtime directory name. |
| `PRESSURE_VESSEL_RUNTIME_ARCHIVE` | `run` | W (unset) | — | Always unset: the runtime is a directory, not an archive. |
| `PRESSURE_VESSEL_RUNTIME_BASE` | `run` | W | `<runtime dir>` | Base for the relative `PRESSURE_VESSEL_RUNTIME`. |
| `STEAM_RUNTIME_STEAMRT` | `pv-run.sh`, steamwebhelper.sh, steam.sh, bootstrapper | R | `steamrt64/pv-runtime/steam-runtime-steamrt` | Use a custom unpacked runtime directory and skip unpacking. |
| `STEAM_RUNTIME_STEAMRT_SDK_ROOT` | `pv-run.sh` | R | `steamrt64/pv-sdk` | For `--sdk`: the SDK sysroot is built with `ninja -C "$SDK_ROOT"`, then run with `--devel --runtime=$SDK_ROOT/files`. **Developer-only; the SDK is not shipped.** |
| `DEBUGINFOD_URLS` | `pv-run.sh` | W (unset) | — | Always unset. |
| `SHELL` | `pv-run.sh` | W | `/bin/bash` | |
| `PATH` | `pv-run.sh` | W | prepends `<runtime>/bin` | Lets `srt-client-container --alongside-steam` find the `steam-runtime-*` tools. |
| `SRT_LOGGER` | `logger-0.bash` | R | `<same dir>/srt-logger` | Path to the srt-logger executable. |
| `SRT_LOGGER_PID`, `SRT_LOGGER_READY` | `logger-0.bash` | W (eval) | — | Printed by `srt-logger --sh-syntax`. `SRT_LOGGER_READY=1` means the redirect succeeded. |
| `PRESSURE_VESSEL_SHELL`, `PRESSURE_VESSEL_TERMINAL`, `PRESSURE_VESSEL_WRAP_GUI`, `PRESSURE_VESSEL_GRAPHICS_PROVIDER`, `PRESSURE_VESSEL_IMPORT_VULKAN_LAYERS`, `PRESSURE_VESSEL_REMOVE_GAME_OVERLAY`, `PRESSURE_VESSEL_SHARE_HOME`, `PRESSURE_VESSEL_SHARE_PID`, `STEAM_COMPAT_LAUNCHER_SERVICE`, `STEAM_COMPAT_LIBRARY_PATHS`, `STEAM_COMPAT_RUNTIME_SDL2`, `STEAM_COMPAT_RUNTIME_SDL3`, `STEAM_RUNTIME_SCOUT` | `launch-options.py` | R/W | — | Values the launch-options GUI reads, offers as choices, and writes into the command line it generates. |

### Command-line options

| Script | Option | Meaning |
|---|---|---|
| `pv-run.sh` | `-v`, `--verbose` | Verbose output. |
| | `-i`, `--interactive` | Passes `--devel` to pressure-vessel. |
| | `--sdk` | Use the SDK sysroot (see above). |
| | `-h`, `--help` | Print usage. |
| | `-- CMD…` | Command to run. |
| `steam-runtime-steamrt.sh` | `--runtime=NAME` | Default `steam-runtime-steamrt-amd64`. Must be a single path component that doesn't start with `.`. |
| | `--unpack-dir=DIR` | Unpack `DIR/NAME.tar.xz` into `DIR/NAME`, comparing `DIR/NAME.VERSIONS.txt` (or `.version.txt`) with `DIR/NAME/VERSIONS.txt`. CRLF endings are tolerated ("transferring these files through the Steam bootstrap converts LF to CRLF"). |
| | `--try-runtime=DIR` | Use an existing runtime if its `VERSIONS.txt` matches. |
| | `--validate` | Run `pressure-vessel/bin/pv-verify --quiet` after unpacking. |
| | `--help` | Print usage. |
| | `[--] CMD…` | Exec `_v2-entry-point -- CMD`. Without a command, prints the entry point path. |
| | exit codes | 64 = usage error, 70 = unpack or verify failure. |
| `_v2-entry-point` | `--verb=%verb%` | `waitforexitandrun` (the default) marks the main process. `run` sets `PRESSURE_VESSEL_BATCH=1`. Anything else is a non-main process. |
| | `--suite=SUITE` | Execs `run-in-SUITE` instead of `run`. |
| | `--log-to-file`, `--keep-logs`, `--use-timestamp`, `--verbose` | Same effect as the env vars above. |
| | `--deploy=DIR` | Ignored (kept for compatibility). |
| | `--help` | Print usage. |
| | exit code | 125 = usage error or missing command. |
| `logger-0.bash` (sourced) | anything | Forwarded to `srt-logger`. steam.sh uses `--log-directory`, `--filename=console-linux.txt`, `--parse-level-prefix`, `-t steam`. steamwebhelper.sh uses `--filename=webhelper-linux.txt`, `--identifier=steamwebhelper`, `--terminal-level=debug`, `--journal-level=info`. Other srt-logger options seen in strings: `--default-level`, `--file-level`, `--journal-fd`, `--log-fd`, `--terminal-fd`, `--no-timestamps`, `--rotate=N`, `--sh-syntax`, `--mkfifo`, `--background`. |

Files and checks:

* `/run/pressure-vessel` existing means "Cannot be run inside a pressure-vessel container" (pv-run.sh).
* `<runtime>/var` must not be a symlink; if it is, it gets removed.
* `~/.steam/root/steam-dialog` is the preferred progress or error dialog.
* `~/.steam/root/{steamrt64,ubuntu12_32}/{reaper,steam-launch-wrapper}` are used by `steam-runtime-launch-options` to run the GUI "like a game".

---

## 2. pressure-vessel and steam-runtime-tools binaries: environment variables

The names were extracted with `strings` from the ELF tools in `steam-runtime-steamrt/pressure-vessel/{bin,libexec}`. The "Seen in" column records which binaries contain each name.

### `PRESSURE_VESSEL_*`

| Variable | Seen in | Meaning (upstream doc unless stated) |
|---|---|---|
| `PRESSURE_VESSEL_ARCHITECTURES` | wrap, pv-adverb | Colon-separated multiarch tuples to set up. |
| `PRESSURE_VESSEL_BATCH` | wrap | `1` = `--batch`: no interactive shell, terminal, or launch-options GUI. |
| `PRESSURE_VESSEL_BWRAP` | wrap, pv-adverb, check-requirements, system-info | Path to an alternative `bwrap` executable. |
| `PRESSURE_VESSEL_COPY_RUNTIME` | wrap | `1` = make a temporary mutable copy of the runtime in the variable dir. |
| `PRESSURE_VESSEL_COPY_RUNTIME_INTO` | wrap | Older, deprecated form that takes a directory. |
| `PRESSURE_VESSEL_DETERMINISTIC` | wrap | Sort directory listings so output is reproducible (debugging). |
| `PRESSURE_VESSEL_DEVEL` | wrap | `--devel`: unsupported developer mode. |
| `PRESSURE_VESSEL_EMULATOR` | wrap | Emulator (FEX) integration, paired with `STEAM_COMPAT_EMULATOR`. |
| `PRESSURE_VESSEL_FDO_APP_ID` | wrap | App ID used when running as a Flatpak sub-sandbox. |
| `PRESSURE_VESSEL_FILESYSTEMS_RO` / `_RW` | wrap | Colon-separated host paths to share read-only or read-write. |
| `PRESSURE_VESSEL_GC_RUNTIMES` | wrap | Garbage-collect old runtime copies. Default on. |
| `PRESSURE_VESSEL_GENERATE_LOCALES` | wrap | Generate missing locales. Default on. |
| `PRESSURE_VESSEL_GRAPHICS_PROVIDER` | wrap, launch-options.py | Sysroot to take graphics drivers from (`/`, `/run/host`, …). Empty means no host graphics. |
| `PRESSURE_VESSEL_GRAPHICS_PROVIDER_` | wrap | Prefix of a longer name. **(inferred)** Per-architecture variants or a string-building prefix. |
| `PRESSURE_VESSEL_HOME` | wrap | Legacy: location of the fake per-game home. |
| `PRESSURE_VESSEL_HOST_GRAPHICS` | wrap | Legacy boolean: `0` disables host graphics. |
| `PRESSURE_VESSEL_IMPORT_CA_CERTS` | wrap | Import host CA certificates. steamwebhelper.sh sets it when the Valve-internal CA file exists. |
| `PRESSURE_VESSEL_IMPORT_OPENXR_1_LAYERS` / `_RUNTIMES` | wrap | Import host OpenXR 1 API layers and runtimes. |
| `PRESSURE_VESSEL_IMPORT_VULKAN_LAYERS` | wrap, launch-options.py | Import host Vulkan layers. Default on. |
| `PRESSURE_VESSEL_LOG_INFO` | all tools | Log at info level. |
| `PRESSURE_VESSEL_LOG_WITH_TIMESTAMP` | all tools | Prefix log lines with timestamps. |
| `PRESSURE_VESSEL_REMOVE_GAME_OVERLAY` | wrap, launch-options.py | Remove the Steam overlay from `LD_PRELOAD`. |
| `PRESSURE_VESSEL_RUNTIME`, `PRESSURE_VESSEL_RUNTIME_BASE` | wrap | Runtime selection (set by `run`). |
| `PRESSURE_VESSEL_SHARE_HOME` | wrap | `1` = real home, `0` = per-app fake home. |
| `PRESSURE_VESSEL_SHARE_PID` | wrap | Share the PID namespace. Default on. |
| `PRESSURE_VESSEL_SHELL` | wrap, launch-options.py | `none`, `after`, `fail` or `instead`: open an interactive shell at that point. |
| `PRESSURE_VESSEL_SINGLE_THREAD` | wrap | Avoid parallelism (debugging). |
| `PRESSURE_VESSEL_SYSTEMD_SCOPE` | wrap, steam-launch-wrapper | Put the game in its own systemd scope. |
| `PRESSURE_VESSEL_TERMINAL` | wrap, launch-options.py | `none`, `auto`, `tty` or `xterm`. Where an interactive shell goes. |
| `PRESSURE_VESSEL_TEST_STANDARDIZE_PLATFORM` | pv-adverb | Test-suite only. |
| `PRESSURE_VESSEL_VARIABLE_DIR` | wrap | See above. |
| `PRESSURE_VESSEL_VERBOSE` | wrap, pv-adverb, launch-client, launcher-service | Verbose logging. |
| `PRESSURE_VESSEL_WORKAROUNDS` | wrap, pv-verify | Comma-separated workaround flags. The enum names in the binary are `PV_WORKAROUND_FLAGS_BWRAP_SETUID`, `_BWRAP_NO_PERMS` and `_LIMIT_SHARED_DIRS` (presumably `bwrap-setuid`, `bwrap-no-perms`, `limit-shared-dirs`) **(inferred spelling)**. |
| `PRESSURE_VESSEL_WRAP_GUI` | launch-options.py | Set when the launch-options GUI is in use. |

### `SRT_*` (steam-runtime-tools)

| Variable | Seen in | Meaning |
|---|---|---|
| `SRT_LOG` | all tools | Comma-separated debug-log flags. **(upstream doc)** |
| `SRT_LOG_TO_JOURNAL` | all tools | Send diagnostics to the systemd Journal. |
| `SRT_LOG_LEVEL_PREFIX` | all tools | Emit `<N>` syslog-level prefixes. srt-logger's `--parse-level-prefix` understands these. |
| `SRT_LOG_DIR`, `SRT_LOG_ROTATION`, `SRT_LOG_TERMINAL`, `SRT_LOGGER_TIMESTAMPS`, `SRT_LOGGER_USE_JOURNAL` | srt-logger | Log directory, rotation (`0` = off), terminal to mirror output to, timestamps, and Journal use. |
| `SRT_LOGGER_PID`, `SRT_LOGGER_READY` | srt-logger (output) | Shell-syntax status written for `logger-0.bash`. |
| `SRT_RECURSIVE_EXEC_GUARD` | most tools | Internal guard against re-exec loops. |
| `SRT_LAUNCHER_SERVICE`, `SRT_LAUNCHER_SERVICE_ALONGSIDE_STEAM`, `SRT_LAUNCHER_SERVICE_HINT`, `SRT_LAUNCHER_SERVICE_STOP_ON_EXIT`, `SRT_LAUNCHER_SERVICE_STOP_ON_NAME_LOSS` | launcher-service, launch-client, srt-client-container | Control the in-container launcher D-Bus service, which is used by `steam-runtime-launch-client --alongside-steam` (the bootstrapper string `steam-runtime-launch-client --alongside-steam -- `). |
| `SRT_HELPERS_PATH`, `SRT_BIN_PATH`, `SRT_DATA_PATH` | system-info, check-requirements, wrap | Override where helper executables and data live. Test/dev only. |
| `SRT_CHECK_VDPAU_CRASH` | check-vdpau | Test hook. |
| `SRT_TEST_PARSE_JSON`, `SRT_TEST_SYSROOT`, `SRT_TEST_ELF_CLASS_FROM_PATH` | system-info | Test hooks. |

### `STEAM_*` read by pressure-vessel tools

These are inputs that the Steam client sets for compatibility tools. See also `compatmanager` in [on-disk-config-files.md](on-disk-config-files.md).

| Variable | Seen in | Meaning |
|---|---|---|
| `STEAM_COMPAT_APP_ID` | all | App ID of the game. |
| `STEAM_COMPAT_APP_LIBRARY_PATH(S)` | wrap | Deprecated predecessor of `STEAM_COMPAT_LIBRARY_PATHS`. |
| `STEAM_COMPAT_CLIENT_INSTALL_PATH` | wrap, system-info | Steam install root. |
| `STEAM_COMPAT_DATA_PATH` | wrap | Per-app compatdata directory (Proton prefix). |
| `STEAM_COMPAT_FLAGS` | wrap, system-info | Comma-separated flags. Strings show `search-cwd` and `search-cwd-first`. |
| `STEAM_COMPAT_FOR_STEAM_CLIENT` | wrap | **(inferred)** Marks a container started for Steam's own components, e.g. the webhelper (cf. `srt-client-container --for-steam-client`). |
| `STEAM_COMPAT_INSTALL_PATH` | wrap | Game install directory. |
| `STEAM_COMPAT_LAUNCHER_SERVICE` | wrap, launcher-interface-0, launch-options.py | Name of the compat tool that should start an in-container launcher service. The client config key `CompatTool_LauncherService` and the value `auto` also appear in steamclient. |
| `STEAM_COMPAT_LIBRARY_PATHS` | wrap | Colon-separated Steam library folders to share. |
| `STEAM_COMPAT_MOUNTS`, `STEAM_COMPAT_MOUNT_PATHS` | wrap | Extra paths to share. `MOUNT_PATHS` is the older spelling. |
| `STEAM_COMPAT_RUNTIME_SDL2`, `STEAM_COMPAT_RUNTIME_SDL3` | wrap, system-info, launch-options.py | Override a game's bundled SDL with the runtime's copy. **(inferred from name)** |
| `STEAM_COMPAT_SHADER_PATH` | wrap | Per-app shader cache directory. |
| `STEAM_COMPAT_TOOL_PATH(S)` | wrap, launcher-service | Compat tool install directories. |
| `STEAM_COMPAT_TRACING` | wrap, system-info | `1` enables tracing in compat tools. |
| `STEAM_EXTRA_COMPAT_TOOLS_PATHS` | wrap, steamclient | Extra `compatibilitytools.d` search directories, colon-separated. |
| `STEAM_RUNTIME_PREFER_HOST_LIBRARIES` | wrap, system-info | Deprecated, no effect. |
| `STEAM_RUNTIME_SCOUT` | wrap | Scout runtime location, for scout-on-SLR. |
| `STEAM_ZENITY` | several | Dialog program. |
| `STEAM_CLIENT_LOG_FOLDER` | srt-logger | Default log directory name (`logs`). |
| `FLATPAK_ID` | wrap, pv-verify, launch-client | Flatpak detection. |

---

## 3. Scout runtime (`ubuntu12_32/steam-runtime`, legacy client path)

### run.sh

| Variable | R/W | Default | Effect |
|---|---|---|---|
| `STEAM_RUNTIME` | W | dir of `run.sh` | Exported. |
| `SYSTEM_PATH`, `SYSTEM_LD_LIBRARY_PATH` | R/W | current `PATH`/`LD_LIBRARY_PATH` | Set only if not already set. |
| `SYSTEM_ZENITY`, `STEAM_ZENITY` | R/W | `command -v zenity`, otherwise `zenity` | Same logic as in steam.sh. |
| `PATH` | W | prepends `$STEAM_RUNTIME/{amd64\|i386}/bin`, `…/usr/bin`, `$STEAM_RUNTIME/usr/bin` | Skips entries that are already present. |
| `STEAM_RUNTIME_PREFER_HOST_LIBRARIES` | R | — | `0` logs "deprecated, no longer has an effect". |
| `DEBUGGER` | R | — | If it is `valgrind*`, `callgrind*`, `helgrind*`, `drd*` or `memcheck*`, defaults `STEAM_RUNTIME_USE_LIBCURL_SHIM=1`. |
| `STEAM_RUNTIME_USE_LIBCURL_SHIM` | R | empty | `1` prepends `libcurl_compat_32:libcurl_compat_64`. `0`/empty does nothing. Any other value logs a warning. **Undocumented switch.** |
| `STEAM_COMPAT_INSTALL_PATH` + `STEAM_COMPAT_FLAGS` | R | — | `search-cwd-first` prepends the install path to `LD_LIBRARY_PATH`. `search-cwd` appends it. |
| `LD_LIBRARY_PATH` | R/W | — | Final order: `pinned_libs_32`, `pinned_libs_64`, the existing `LD_LIBRARY_PATH`, the host ldconfig paths (from `steam-runtime-identify-library-abi --ldconfig-paths`, falling back to `/sbin/ldconfig -XNv`), then the runtime `lib/{i386,x86_64}-linux-gnu`, `usr/lib/…`, `lib` and `usr/lib`. |

| Argument | Meaning |
|---|---|
| `--print-steam-runtime-library-paths` (as `$1`) | Print the computed path and exit. steam.sh uses this. |
| anything else | `exec "$@"` with the runtime `LD_LIBRARY_PATH`. |

### setup.sh

| Option | Meaning |
|---|---|
| `--force` | Always re-pin libraries: rebuild `pinned_libs_{32,64}`, using a zenity progress dialog titled "Steam setup". |
| `--print-bin-path` | Print `$top/<arch>/bin:$top/<arch>/usr/bin:$top/usr/bin`. |
| `--print-lib-paths` | Accepted in the case statement but not in the getopt spec, so it is effectively unusable. |
| `--help` | Print usage. |
| (none) | `check_pins`: re-pin only if `pinned_libs_*/done` is missing or a pinned host library has changed. |

| Variable | Effect |
|---|---|
| `STEAM_RUNTIME_VERBOSE` | Non-empty enables `debug` output. |
| `STEAM_ZENITY` | Unset becomes `command -v zenity`. A non-executable value becomes empty, meaning no progress dialog. |

Pinning rules, from the code:

* The runtime copy is forced (always pinned, regardless of version) for:
  * `libcurl.so.4` and `libcurl-gnutls.so.4`, plus `.so.3` compatibility symlinks
  * 32-bit `libgtk-x11-2.0.so.0`
  * 32-bit `libdbusmenu-glib.so.4` and `libdbusmenu-gtk.so.4`
* For every other library, the host copy is pinned when its version is newer than the runtime's.

Marker files written:

* `pinned_libs_{32,64}/done` (pinning complete)
* `has_pins` (at least one host library was pinned)
* `system_<soname>` (records the host symlink and target)

### steam-runtime-dialog (zenity shim)

| Variable | Effect |
|---|---|
| `STEAM_RUNTIME_DIALOG_UI` | External dialog program to use if it passes `--check-features`. |
| `STEAM_RUNTIME_DIALOG__FORCE_XTERM` | Non-empty forces the xterm fallback. **Undocumented, double underscore.** |
| `STEAM_RUNTIME_VERBOSE` | Debug output. |
| `XDG_CURRENT_DESKTOP`, `STEAM_ZENITY`, `STEAM_RUNTIME`, `STEAM_RUNTIME_SCOUT`, `SYSTEM_PATH`, `SYSTEM_LD_LIBRARY_PATH`, `SYSTEM_LD_PRELOAD` | Environment restoration and selection. |

Supported zenity-style options:

* Dialog types: `--error`, `--info`, `--warning`, `--progress`
* Modifiers: `--title`, `--text`, `--width`, `--height`, `--auto-close`, `--no-cancel`, `--no-wrap`, `--percentage`, `--pulsate`
* Other: `--check-features`, `--verbose`/`-v`, `--help`

### scripts/switch-runtime.sh

It undoes the scout environment: `STEAM_RUNTIME`, `STEAM_ZENITY`, `SYSTEM_PATH`, `SYSTEM_LD_LIBRARY_PATH`. Then it runs a command in another runtime, using `--runtime=…`, `--unpack-dir=…` and `--help`.
