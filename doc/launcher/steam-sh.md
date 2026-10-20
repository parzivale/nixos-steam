# steam.sh and the other top-level launcher scripts

Steam Linux client, manifest version `1791918634` (`ubuntu12` platform manifest).

## Method and sources

I read every shell script shipped in the client packages line by line. Behaviour stated without a marker comes straight from the code. Anything marked **(inferred)** is my interpretation. Paths are relative to the Steam install root (`~/.local/share/Steam` or `~/.steam/debian-installation`; the scripts call it `$STEAMROOT`).

| Script | Package | Lines | Role |
|---|---|---|---|
| `steam.sh` | `bins_ubuntu12` | 1006 | Main entry point that `/usr/bin/steam` execs. It either hands off to the SteamRT3 bootstrapper `steamrt64/steam` or runs the legacy `ubuntu12_32/steam` client inside the scout LD_LIBRARY_PATH runtime. |
| `steam_msg.sh` | `bins_ubuntu12` | 76 | Shows an error or warning dialog through zenity, with xterm and then stderr as fallbacks. The bootstrapper calls it (`%s/steam_msg.sh` appears in `steamrt64/steam`). |
| `ubuntu12_32/legacy-run-stub.sh` | `bins_ubuntu12` | 12 | Gets symlinked as `ubuntu12_32/steam-runtime/run.sh` when the steamrt64 client is in use. |
| `ubuntu12_32/legacy-setup-stub.sh` | `bins_ubuntu12` | 5 | Gets symlinked as `ubuntu12_32/steam-runtime/setup.sh`. It always fails. |
| `ubuntu12_64/steamwebhelper.sh` | `webkit_ubuntu12` | 109 | Launches the CEF `steamwebhelper` inside the steamrt3c pressure-vessel container. Legacy/scout client path. |
| `ubuntu12_64/steamwebhelper_sniper_wrap.sh` | `webkit_ubuntu12` | 14 | Runs inside the container. Sets `LD_LIBRARY_PATH=.` and execs `./steamwebhelper`. |
| `steamrt64/steamwebhelper.sh` | `webkit_steamrt_ubuntu12` | 8 | Plain `cd` + `exec ./steamwebhelper "$@"`. The steamrt64 client already runs inside the container. |

The runtime scripts (`steamrt64/pv-run.sh`, `steam-runtime-steamrt.sh`, `_v2-entry-point`, scout `run.sh`/`setup.sh`, and others) are covered in [steam-runtime.md](steam-runtime.md). The native bootstrapper `steamrt64/steam` is covered in [bootstrapper.md](bootstrapper.md).

---

## 1. How steam.sh runs (overview)

1. Sets `STEAMROOT` to the directory containing the script and `STEAMEXE` to `basename $0 .sh`, so normally `steam`.
2. If `STEAM_FORCE_CLIENT` is set, creates or deletes the opt-in flag `$STEAMROOT/.steam-enable-steamrt64-client`.
3. **SteamRT3 path.** If `.steam-enable-steamrt64-client` exists and `steamrt64/steam` is executable, it does the following and exits. Nothing below this step runs.
   * `unset STEAM_RUNTIME STEAM_RUNTIME_LIBRARY_PATH`
   * Calls `create_legacy_entry_points`, which rebuilds `ubuntu12_32/steam-runtime/` as a shim tree:
     * `amd64/usr/bin/*` are symlinks into `steamrt64/pv-runtime/steam-runtime-steamrt/bin/*`.
     * `usr/libexec/steam-runtime-tools-0/{logger-0.bash,srt-logger}`.
     * `run.sh` points to `../legacy-run-stub.sh` and `setup.sh` to `../legacy-setup-stub.sh`.
     * The previous tree is moved to `steam-runtime.old`.
   * Runs `steamrt64/steam "$@"`. Exit code **42** means restart: `exec "$0" "$@"`.
4. **Legacy path** (ubuntu12_32 client in the scout LDLP runtime):
   * If `STEAMEXE=steamcmd`, exec `steamcmd.sh`.
   * Save `SYSTEM_PATH`, `SYSTEM_LD_LIBRARY_PATH` and `SYSTEM_ZENITY`, then pick `STEAM_ZENITY`.
   * Handle `--reset`. On first launch, create the `~/.steam/*` symlinks.
   * Unpack and verify the scout runtime (`ubuntu12_32/steam-runtime.tar.xz` plus its `.checksum`), then run its `setup.sh` (library pinning).
   * Export `STEAM_RUNTIME`, `PATH` and `STEAM_RUNTIME_LIBRARY_PATH`/`LD_LIBRARY_PATH`.
   * Fix the SDL Wayland-only driver values.
   * Handle `--run`.
   * Open the srt-logger to `logs/console-linux.txt` and prepend `-srt-logger-opened` to the arguments.
   * Unpack `steamrt64/steam-runtime-steamrt.tar.xz` if present. If that fails, `-verifyfiles` is appended **(see the note in section 3)**.
   * Prepend `ubuntu12_32:ubuntu12_32/panorama` to `LD_LIBRARY_PATH`.
   * Check for missing 32-bit libraries with `ldd` on `steamui.so`, unless `-steamos` was passed.
   * Run `steam-runtime-check-requirements`. Exit status 71 is fatal.
   * Touch `~/.steam/starting`.
   * Launch `ubuntu12_32/steam`, optionally under a debugger.
   * Restore `PATH`/`LD_LIBRARY_PATH`. Exit code 42 triggers a re-exec.

---

## 2. Environment variables used by steam.sh

"R" means the script reads the variable (input), "W" means it sets or exports it (output).

| Variable | R/W | Default | Effect |
|---|---|---|---|
| `STEAM_DEBUG` | R | unset | If non-empty, runs `set -x` and traces the whole script. |
| `STEAMEXE` | R/W | `basename $0 .sh` (`steam`) | Name of the client binary under `ubuntu12_32/`. If it is `steamcmd`, the script execs `steamcmd.sh` instead. |
| `STEAM_FORCE_CLIENT` | R | unset | `ubuntu12_32`, `scout` or `ldlp` delete `$STEAMROOT/.steam-enable-steamrt64-client` (forcing the legacy 32-bit client). `steamrt64`, `steamrt3c` or `steamrt` touch it (forcing the 64-bit SteamRT3 client). Any other value logs "Unknown value". The setting persists because it changes the flag file. |
| `STEAM_RUNTIME_STEAMRT` | R | `$STEAMROOT/steamrt64/pv-runtime/steam-runtime-steamrt` | Developer override for the steamrt3c runtime directory. Used as the symlink target in `create_legacy_entry_points`. In the legacy path, if set, the script skips unpacking `steamrt64/steam-runtime-steamrt.tar.xz` and logs "Using custom runtime ... (this is unsupported)". |
| `STEAM_RUNTIME` | R/W | `""`, then becomes the scout path | **SteamRT3 path:** unset before `steamrt64/steam` runs, because some distros set it wrongly (steam-for-linux#13597). **Legacy path** input values: `""` means auto (enabled); `1` means enabled; `0` disables the LDLP runtime ("unsupported"; the archive is still unpacked for srt-logger); `debug` is deprecated (only logs); an absolute path is deprecated and gets copied into `STEAM_RUNTIME_SCOUT`. Output: exported as `$STEAM_RUNTIME_SCOUT` unless it is `0`. |
| `STEAM_RUNTIME_SCOUT` | R/W | `$STEAMROOT/ubuntu12_32/steam-runtime` | Path to the unpacked scout runtime. A relative value is resolved with `realpath` and falls back to the default if the directory is missing. |
| `STEAM_RUNTIME_LIBRARY_PATH` | W | output of `run.sh --print-steam-runtime-library-paths` | Exported, and also copied into `LD_LIBRARY_PATH`. Unset on the SteamRT3 path. |
| `STEAM_RUNTIME_RUN_SCRIPT` | W | — | Set to `$STEAM_RUNTIME_SCOUT/run.sh` just before `--run` execs. Not exported. |
| `STEAM_RUNTIME_LOGGER` | R | unset | `0` disables logging to `logs/console-linux.txt`. The comment says it interferes with vscode's gdb wrapping. The bootstrapper also reads this variable; see bootstrapper.md. |
| `STEAM_CLIENT_LOG_FOLDER` | R | `logs` | Log directory name under the Steam data dir (`~/.steam/steam/<folder>`). Holds `console-linux.txt`. |
| `DEBUGGER` | R | unset | If set, the script launches the client under a debugger, disables srt-logger, and then **unsets** `DEBUGGER` so recursive Steam launches aren't debugged. Special values: `gdb`/`cgdb` (first word, `basename`), `valgrind`, `callgrind`, `strace`, `lldb-mi`, `gdbserver`. Any other value is treated as a generic command prefix with the warning "Using default/fallback debugger launch". See section 4. |
| `DEBUGGER_ARGS` | R | `""` | Extra arguments passed to the debugger. |
| `STEAM_VALGRIND` | R | `""` | Extra arguments passed to valgrind when `DEBUGGER=valgrind`. |
| `STEAM_DEBUGGER` | W (internal) | `$DEBUGGER` | Internal copy of `DEBUGGER`. |
| `STEAMSCRIPT` | R/W (not exported) | `/usr/bin/steam`, or `/usr/bin/steambeta` for the Beta universe | Only given a default on first launch. The distro wrapper `/usr/bin/steam` normally exports it, along with `STEAMSCRIPT_VERSION`; steam-runtime-system-info reports it as missing (`SRT_STEAM_ISSUES_STEAMSCRIPT_NOT_IN_ENVIRONMENT`). |
| `STEAMOS` | R/W | `""` | Set to 1 when `-steamos` or `-steamos3` is in argv; can also be preset. When non-empty, the `ldd` missing-32-bit-library check is skipped. |
| `HOME` | R | — | `STEAMCONFIG=${HOME%/}/.steam`. |
| `USER` | R | — | Used in the temp names `/tmp/steam_startup_messages_$USER.txt` and `$USER.steam.gdb.XXXX`. |
| `XDG_CURRENT_DESKTOP` | R | `other` | If it equals `gamescope`, `show_message` only logs and never runs zenity or xterm, because they would block. |
| `PATH` | R/W | — | Saved as `SYSTEM_PATH`. The runtime `--print-bin-path` entries are prepended. Restored before a restart. |
| `LD_LIBRARY_PATH` | R/W | — | Saved as `SYSTEM_LD_LIBRARY_PATH`. Set to `STEAM_RUNTIME_LIBRARY_PATH`, then prefixed with `$STEAMROOT/ubuntu12_32:$STEAMROOT/ubuntu12_32/panorama`. Under gdb/cgdb it moves into the gdb args file and is unset in the environment. |
| `LD_PRELOAD` | R/W | — | Under gdb/cgdb it moves into the args file (`set env LD_PRELOAD=...`) and is unset. `ldd` checks always run with `LD_PRELOAD=` cleared. |
| `SYSTEM_PATH` | W | `$PATH` | Exported so child processes can restore the host PATH. pressure-vessel-unruntime and steam-runtime-steamrt.sh use it. |
| `SYSTEM_LD_LIBRARY_PATH` | W | `$LD_LIBRARY_PATH` | Same idea, for the host library path. |
| `SYSTEM_ZENITY` | W | `$(which zenity)` | Path to the host zenity, if there is one. |
| `STEAM_ZENITY` | W | `$SYSTEM_ZENITY`, otherwise the literal `zenity` (the runtime's copy) | Dialog binary used by `show_message` and for the unpack progress bars. |
| `TEXTDOMAIN` / `TEXTDOMAINDIR` | W | `steam` / `/usr/share/locale` | Gettext domain for the `$"..."` localized strings in the script. |
| `SDL_VIDEO_DRIVER` | R/W | — | If it is exactly `wayland`, it is rewritten to `wayland,x11` with a warning (SDL3 builds may lack Wayland, so this allows fallback). |
| `SDL_VIDEODRIVER` | R/W | — | The same rewrite, for SDL2. |
| `SDL_VIDEO_X11_DGAMOUSE` | W | `0` | Always exported as 0. Disables SDL 1.2 DGA mouse because the overlay can't support it. |
| `DONT_BREAK_ON_ASSERT`, `G_SLICE`, `G_DEBUG` | W | `1`, `always-malloc`, `gc-friendly` | Set only for the `DEBUGGER=valgrind` launch. `DONT_BREAK_ON_ASSERT` is also a string in the bootstrapper. |
| `TAR_CHECKPOINT` | (tar) | — | Used by the extraction progress pipeline (`--checkpoint-action=exec=echo $TAR_CHECKPOINT`). |

Variables that `logger-0.bash` / `srt-logger` read when steam.sh sources it (`SRT_LOGGER`, `SRT_LOG_*` and others) are listed in steam-runtime.md.

### steam_msg.sh

| Variable | R/W | Effect |
|---|---|---|
| `XDG_CURRENT_DESKTOP` | R | Under `gamescope`, prints `FIXME: ... not functional under gamescope` and exits without showing a dialog. |
| `STEAM_ZENITY` | R/W | Expected to be already set by steam.sh. If it isn't, it gets the same `SYSTEM_ZENITY`/`zenity` treatment as in steam.sh. |
| `SYSTEM_ZENITY` | R/W | Detected with `which zenity` when missing. The script then restores the host `LD_LIBRARY_PATH` (`SYSTEM_LD_LIBRARY_PATH`) before running zenity. **Bug:** the `[ -n ${SYSTEM_ZENITY-} ]` test is unquoted, so it is always true. |
| `SYSTEM_LD_LIBRARY_PATH` | R | Becomes `LD_LIBRARY_PATH` for the zenity call. |

| Argument | Meaning |
|---|---|
| `--title "TITLE"` | Optional, and must come first. Passed through as zenity `--title=`. |
| `--error` / `--warning` | Required dialog style. Anything else prints `invalid command parameters` and exits 1. |
| remaining args | Message text. |

If zenity isn't available, the fallback is `xterm -bg "#383635" -fg "#d1cfcd"` with a "Press enter" prompt, and then plain stderr.

### ubuntu12_64/steamwebhelper.sh (legacy/scout client path)

| Variable | R/W | Default | Effect |
|---|---|---|---|
| `STEAM_RUNTIME_SCOUT` | R | `$HOME/.steam/root/ubuntu12_32/steam-runtime` | Where it sources `usr/libexec/steam-runtime-tools-0/logger-0.bash` from. The log file is `webhelper-linux.txt` with identifier `steamwebhelper` and journal level `info`. |
| `STEAMWEBHELPER_USE_TERMINAL` | R | unset | If non-empty, passes `--terminal-level=debug` to srt-logger so webhelper output also goes to the terminal. **Undocumented switch.** |
| `STEAM_RUNTIME_STEAMRT` | R | `realpath ../steamrt64/pv-runtime/steam-runtime-steamrt` | Location of the runtime. The entry point is `$STEAM_RUNTIME_STEAMRT/_v2-entry-point`. If it isn't executable, the script runs `../steamrt64/pv-run.sh -- true` to unpack it, and if it is still missing it shows `steam_msg.sh --error` and exits 1. |
| `PRESSURE_VESSEL_BATCH` | W | `1` | Disables interactive pressure-vessel features (`--shell`, `--terminal`, the launch-options GUI). |
| `PRESSURE_VESSEL_SHARE_HOME` | W | `1` | The webhelper always shares the real `$HOME`, even when games get a private home. |
| `PRESSURE_VESSEL_IMPORT_CA_CERTS` | W | `1` only when `/etc/ca-certificates/trust-source/anchors/constraind-valve-ca.cer` exists | Valve-internal: imports host CA certificates into the container, for testing against dev stores. **Hidden internal switch** triggered by that file's presence. |
| `STEAM_COMPAT_FLAGS` | W | `search-cwd,search-cwd-first` | Asks the runtime to put the working directory on the library search path. A FIXME notes this only works for LDLP runtimes. |
| `STEAM_COMPAT_INSTALL_PATH` | W | `ubuntu12_64` dir | Used together with `STEAM_COMPAT_FLAGS`. |

CEF sandbox auto-detection: unless `--no-sandbox` is already in argv, the script adds `--no-sandbox` when any of these hold:

* `/proc/sys/kernel/unprivileged_userns_clone` is `0`
* `/proc/sys/user/max_user_namespaces` is `0`
* `/.flatpak-info` exists (running under Flatpak)

A `can_sandbox=without-seccomp` branch would add `--disable-seccomp-filter-sandbox`, but nothing currently sets that value (dead code).

`steamwebhelper_sniper_wrap.sh` prepends `.` to `LD_LIBRARY_PATH`. It then writes `<6>exec ./steamwebhelper ...` and `<remaining-lines-assume-level=7>` to stdout. These are srt-logger level-prefix directives that demote all further output to debug level, so it reaches the log file and journal but not the terminal.

### legacy-run-stub.sh / legacy-setup-stub.sh

* `run.sh` stub: warns `Running $1 on the host, not in the legacy runtime`, recommends `steamapps/common/LegacySteamRuntime/{setup,run}.sh`, prepends `steam-runtime/amd64/usr/bin` (the steamrt3c tools) to `PATH`, and execs its arguments on the host.
* `setup.sh` stub: prints `ERROR: This is not a complete version of the legacy Steam Runtime` and exits 1.
* Effect: third-party scripts that call `~/.steam/root/ubuntu12_32/steam-runtime/run.sh` keep working, but without scout libraries. The full scout runtime now ships as the Steam app **LegacySteamRuntime** (`steamapps/common/LegacySteamRuntime`).

---

## 3. Command-line arguments that steam.sh itself looks at

steam.sh passes every argument through to the client binary. On the SteamRT3 path it does no parsing at all and everything goes straight to `steamrt64/steam`. Flags such as `-shutdown`, `-silent`, `-steamdeck`, `-gamepadui` and `-noverifyfiles` are handled by the bootstrapper or client; see [bootstrapper.md](bootstrapper.md).

| Argument | Position | Path | Behaviour |
|---|---|---|---|
| `--reset` | must be `$1` | legacy | Calls `reset_steam` and then exits. It refuses if `steam_dev.cfg` exists, if Steam is running (`INITIAL_LAUNCH` false, i.e. the pid in `~/.steam/steam.pid` is alive), or if no bootstrap tarball is found. Otherwise it ignores SIGINT and removes the `~/.steam/steam` data link. It moves `bootstrap.tar.xz`, `ssfn*`, `SteamApps`, `steamapps`, `userdata` and `package` into `$STEAMROOT/.save/`, renames `~/.steam/registry.vdf` to `registry.vdf.bak`, and runs `rm -rf $STEAMROOT/*`. It then restores the saved items, re-extracts the bootstrap tarball (`umask 077`) and recreates the data link. Note that `-reset` with a single dash is **not** handled here. **Inferred:** with the steamrt64 client opted in, `--reset` reaches the steamrt64 bootstrapper unparsed, because the SteamRT3 branch runs before this check. |
| `--run` | must be `$1` | legacy | `exec $STEAM_RUNTIME_SCOUT/run.sh "${@:2}"`. Runs an arbitrary command inside the scout LD_LIBRARY_PATH runtime with Steam's environment, then exits 255 if exec fails. |
| `-steamos` | anywhere | legacy | Sets `STEAMOS=1`, which skips the missing-32-bit-library dialog. Also forwarded to the client. |
| `-steamos3` | anywhere | legacy | Same as `-steamos` (comment: "holo/jupiter", i.e. Steam Deck). |
| `-srt-logger-opened` | anywhere | legacy | Input: if present, the logger isn't opened a second time. Output: steam.sh prepends it to argv after it opens the log, so the client and the re-exec on exit code 42 know logging is already set up. The bootstrapper also knows this flag. |
| `-verifyfiles` | appended | legacy | **Note:** `setup_steamrt_override` runs `set -- "$@" -verifyfiles` *inside a function*, so it only changes the function's own positional parameters and never reaches the client. This is a script bug. The intended effect was "Encountered a problem expanding the steamrt runtime, forcing extended file verification". |

Restart protocol: if the client exits with code **42** (`MAGIC_RESTART_EXITCODE`), steam.sh restores `PATH`/`LD_LIBRARY_PATH` and execs itself with the same arguments. On the legacy path those arguments already include the injected `-srt-logger-opened`.

---

## 4. Debugger launch modes (`DEBUGGER=`)

| `DEBUGGER` value | Command run |
|---|---|
| `gdb ...` / `cgdb ...` (first word's basename) | `$DEBUGGER -x $ARGSFILE $DEBUGGER_ARGS --args ubuntu12_32/steam "$@"`. `ARGSFILE` (`mktemp $USER.steam.gdb.XXXX` in `$STEAMROOT`) contains `set env LD_PRELOAD=...`, `set env LD_LIBRARY_PATH=...`, `set index-cache enabled on` and `show index-cache stats`. Deleted afterwards. |
| `valgrind` | `DONT_BREAK_ON_ASSERT=1 G_SLICE=always-malloc G_DEBUG=gc-friendly valgrind --error-limit=no --undef-value-errors=no --suppressions=ubuntu12_32/steam.supp $STEAM_VALGRIND ubuntu12_32/steam "$@" 2>&1 \| tee steam_valgrind.txt`. The scout `run.sh` also sets `STEAM_RUNTIME_USE_LIBCURL_SHIM=1` automatically for valgrind/callgrind/helgrind/drd/memcheck. |
| `callgrind` | `valgrind --tool=callgrind --instr-atstart=no ...` |
| `strace` | `strace -osteam.strace ...` (output goes to `$STEAMROOT/steam.strace`) |
| `lldb-mi` | `lldb-mi $DEBUGGER_ARGS ubuntu12_32/steam -- "$@"` |
| `gdbserver` | `gdbserver $DEBUGGER_ARGS ubuntu12_32/steam "$@"` |
| anything else | `$DEBUGGER $DEBUGGER_ARGS ubuntu12_32/steam "$@"` with the warning "Most likely not what you want!" |

With any `DEBUGGER` set, srt-logger is not used, so output stays on the terminal.

These modes apply only to the legacy ubuntu12_32 client path. On the steamrt64 path, steam.sh ignores `DEBUGGER`. **(Inferred)** The bootstrapper's own strings "srt-logger: disabled during debug" and `-debugbreak` suggest it does its own debugger detection.

---

## 5. Files and directories steam.sh touches or checks

| Path | Use |
|---|---|
| `$STEAMROOT/.steam-enable-steamrt64-client` | Opt-in flag for the 64-bit SteamRT3 client. Created or removed by `STEAM_FORCE_CLIENT`. The bootstrapper (`ReexecToLauncher: opted into steamrt3 client`), `gamelauncher` and `steamui.so` all reference it, so the client UI can toggle it **(inferred)**. |
| `$STEAMROOT/steamrt64/steam` | SteamRT3 bootstrapper. Must be executable for the opt-in flag to take effect. |
| `$STEAMROOT/ubuntu12_32/steam-runtime{,.old}` | Scout runtime (legacy path) or shim tree (SteamRT3 path). |
| `$STEAMROOT/ubuntu12_32/steam-runtime.tar.xz` + `.tar.xz.checksum` | Scout runtime archive and its md5 (`md5sum` format). Unpacking goes through `steam-runtime.tmp`, and `steam-runtime/checksum` records the unpacked version. Return codes: 1 = no archive and no dir; 2 = checksum mismatch; 3 = extraction failed; 4/5 = moving into place failed; 6 = writing the checksum failed. |
| `$STEAMROOT/steamrt64/steam-runtime-steamrt.tar.xz` | If present (legacy path), it is unpacked with `steamrt64/steam-runtime-steamrt.sh --unpack-dir=steamrt64 --runtime=steam-runtime-steamrt`. |
| `$STEAMROOT/ubuntu12_64/steam-runtime-sniper/`, `steam-runtime-sniper.lock`, `steam-runtime-steamrt.lock` | Leftovers from the old sniper runtime. Always deleted. |
| `$STEAMROOT/Steam.cfg`, `$STEAMROOT/steam.cfg` | grepped for `^[Uu]niverse *= *[Bb]eta$`. A match makes the package `steambeta`, which changes `~/.steam/steambeta` and `/usr/bin/steambeta`. See [steam-cfg-and-magic-files.md](steam-cfg-and-magic-files.md). |
| `$STEAMROOT/steam_dev.cfg` | Marks a development install. When present: no `~/.steam/steam` (or `steambeta`) data link is created, the bootstrap is not reinstalled, and `--reset` refuses to run. |
| `$STEAMROOT/bootstrap.tar.xz` | Bootstrap archive used by `--reset` and `install_bootstrap`. Fallback is `/usr/lib/steam/bootstraplinux_ubuntu12_32.tar.xz` (or `/usr/lib/steambeta/...`). |
| `~/.steam/` (`STEAMCONFIG`) | Created on first launch. |
| `~/.steam/steam.pid` | PID of the running Steam. `INITIAL_LAUNCH` is false if `kill -0` on it succeeds. |
| `~/.steam/steam.pipe` | `is_steam_running` checks that the PID has this FIFO open, which detects stale pid files. |
| `~/.steam/bin32` → `ubuntu12_32`, `~/.steam/bin64` → `ubuntu12_64`, `~/.steam/sdk32` → `linux32`, `~/.steam/sdk64` → `linux64`, `~/.steam/root` → `$STEAMROOT`, `~/.steam/steam` (or `steambeta`) → `$STEAMDATA` | API symlinks, rebuilt when Steam isn't running or a link is broken. Skipped if `$STEAMROOT` already *is* one of the links. |
| `~/.steampath` → `~/.steam/sdk32/steam`, `~/.steampid` → `~/.steam/steam.pid`, `~/.steam/bin` → `~/.steam/bin32` | Legacy "bandaid" symlinks, always recreated on first launch. |
| `~/.steam/starting` | Truncated or created just before the client launches, "so we can detect bootstrap launch failure". |
| `~/.steam/registry.vdf` → `registry.vdf.bak` | Renamed by `--reset`. |
| `$STEAMROOT/.save/` | Temporary holding area during `--reset`. |
| `~/.steam/steam/logs/console-linux.txt` | srt-logger output. The folder name comes from `STEAM_CLIENT_LOG_FOLDER`. `mkdir` is used without `-p` on purpose. |
| `/tmp/steam_startup_messages_$USER.txt` | Messages are appended here when no dialog tool is available. |
| `$STEAMROOT/ubuntu12_32/steam.supp` | valgrind suppressions file. |
| `$STEAMROOT/steam_valgrind.txt`, `$STEAMROOT/steam.strace`, `$STEAMROOT/$USER.steam.gdb.XXXX` | Debugger outputs and temp file. |
| `/etc/lsb-release`, `/etc/os-release`, `/etc/debian_version` | Used only for the log line "Running Steam on <distro> <release> <arch>". |
| `ubuntu12_32/steam-runtime/amd64/usr/bin/steam-runtime-check-requirements` | Exit status 71 shows "this computer does not meet the requirements" and is fatal. Any other non-zero status is only logged. |

### Exit codes

| Code | Meaning |
|---|---|
| 42 | Client asked for a restart; steam.sh re-execs itself. |
| 71 | `steam-runtime-check-requirements` says the system is unsupported (EX_OSERR). |
| 255 | `exec` of `steamcmd.sh` or `run.sh` failed. |
| 1 | Unsupported OS (non-Linux), missing STEAMROOT, runtime unpack failure, or missing runtime `setup.sh`/`run.sh`. |
