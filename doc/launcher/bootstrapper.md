# Bootstrapper (`steamrt64/steam`, `ubuntu12_32/steam`, `gamelauncher`): arguments and environment

Steam Linux client, manifest `1791918634`.

## Method and sources

* `steamrt64/steam` (11.8 MB, SteamRT3c / GCC 14.2) is the native bootstrapper and updater. On the SteamRT3 path, `steam.sh` hands it the full command line with no parsing. The legacy path uses the ubuntu12_32 counterpart, `ubuntu12_32/steam`. The strings dumps are `strs/steamrt64__steam.txt` (194k lines) and `strs/ubuntu12_32__steam.txt`.
* `steamrt64/gamelauncher` and `steamrt32/gamelauncher` contain the same bootstrapper code under a different product name. Their unique strings include `Game Launcher`, `Updating Game Launcher...`, `gamelauncher.dbg` and `steamchina_review_`. **(inferred)** They are a rebranded bootstrapper for standalone or China game-launcher builds. They accept the same flags and `steam.cfg` keys.
* The bootstrapper's string table is **hash-ordered**: adjacent strings are not related, so a flag's description can't be taken from its neighbours. In `steamclient.so`, by contrast, the first ~100k lines are in source order, so its description strings sit next to the flags they describe.
* "Evidence" below means the exact string is present in the binary. Meanings are **(inferred)** unless a log or description string states them, in which case that string is quoted.

---

## 1. Command-line flags found in the bootstrapper

Single-dash flags are Valve's style. The bootstrapper consumes the ones that relate to updating and passes the rest through to the client (`steamui.so`/`steamclient.so`). It writes the forwarded command line out with `SteamBootstrapper_GetForwardedCommandLine`. If Steam is already running, it forwards the command line over IPC and exits: "Steam is already running, exiting (command line was forwarded)."

### Update, bootstrap and install control

| Flag | Evidence / meaning |
|---|---|
| `-inhibitbootstrap` | Skips the bootstrap/update step: the client starts with whatever is installed **(inferred)**. Same idea as `BootStrapperInhibitAll` in `steam.cfg`. |
| `-nobootstrapperupdate` | Don't update the bootstrapper binary itself **(inferred)**. |
| `-skipinitialbootstrap` | Skips the first-run bootstrap step **(inferred)**. |
| `-forcesteamupdate` | Forces a client update check and apply **(inferred)**. |
| `-forcepackagedownload` | Re-downloads the package zips even when cached ones look valid **(inferred)**. |
| `-forcemanifestsuffix` | Takes an argument. Overrides the manifest filename suffix, e.g. `steam_client_<suffix>` **(inferred)**. |
| `-overridepackageurl` | Takes an argument. Alternate CDN base URL for packages. Related string: `ClientDownloadHost in Steam.cfg` **(inferred)**. |
| `-bootstrapperproxy` | Takes an argument. HTTP proxy for bootstrapper downloads **(inferred)**. |
| `-installupdate` | Applies a pending update. Related strings: "Found pending update", "Applying update..." **(inferred)**. |
| `-verifyfiles` | Full file verification. Related strings: "Verifying all file checksums", "Verifying installation...". |
| `-noverifyfiles` | Skips verification. Related strings: "Verification skipped", "Verifying file sizes only". |
| `-norepairfiles` | Skips repair of bad files. Related string: "Skipping file repair". |
| `-nodircheck` | Skips the install directory checks (non-ASCII path, writability; strings `SteamBootstrapper_InstallDirNotASCII`, `%s/.writable`) **(inferred)**. |
| `-forcejunction`, `-tryjunction` | Move or link the content directory. Related strings: `SteamBootstrapper_MoveContentDir_*`. Mostly Windows-oriented **(inferred)**. |
| `-alwaysrelaunch` | Always re-exec after updating **(inferred)**. |
| `-simulatedownloaderrors` | Test hook: fake download failures **(inferred)**. |
| `-simulatefatalerror` | Test hook. Related string: "Forcing a fatal error". |
| `-failsystemcheck` | Test hook: make the system check fail **(inferred)**. |
| `-skipsystemcheck` | Skip the system requirements check (`steam-runtime-check-requirements`; strings: `%s: system does not meet steamrt requirements`) **(inferred)**. |
| `-overrideminos` | **Documented** in `public/steambootstrapper_*.txt` (`SteamCmd_OperatingSystemNoLongerSupported`): "You may override this check by passing -overrideminos". Bypasses the minimum-OS-version check. |
| `-forceunsupportedos` | Also runs on an OS the manifest marks unsupported **(inferred)**. |
| `-forceosver` | Takes an argument. Spoofs the OS version sent with the manifest request (`OSVER=%d`) **(inferred)**. |
| `-allosvers`, `-allosarches`, `-arch` | Request packages for every OS version, every architecture, or a given arch. Related strings: `oslist`, `osarch` **(inferred)**. |
| `-download` | Download only **(inferred)**. |
| `-oldlib` | **(inferred)** Legacy library mode. |

### Client beta (branch) selection

| Flag | Evidence / meaning |
|---|---|
| `-clientbeta <name>` | "Overrides Steam client beta for single session". Log string: "Overriding client beta for this session from '%s' to '%s' (clientbeta flag)". |
| `-setbeta <name>` | "Sets Steam client beta branch", i.e. persistent: written to `package/beta`. Log string: "Changing client beta from '%s' (beta file) to '%s' (changebeta flag)" **(inferred pairing)**. |
| `-clearbeta` | Leave the client beta and delete `package/beta` **(inferred)**. |

On a 404 for a beta manifest: "Backing out of client beta '%s' due to manifest download error 404".

### UI and runtime selection

| Flag | Evidence / meaning |
|---|---|
| `-textclient` | Text/console update UI (`CConsoleUpdateUI`) instead of the X11/GLX updater window **(inferred)**. |
| `-forceguiupdater` | Force the graphical update UI **(inferred)**. |
| `-child-update-ui`, `-child-update-ui-socket <fd>` | Internal. The update UI runs as a forked child process connected through an IPC socket (`CUpdateUIChildProcess`; format string ` -child-update-ui-socket %d`). |
| `-no-child-update-ui` | Keep the update UI in-process **(inferred)**. |
| `-srt-logger-opened` | Tells the bootstrapper the srt-logger is already set up. Strings: "srt-logger: disabled, already open". |
| `-console` / `-noconsole` | Enable or disable the developer console (`close_console`, `echo_console`). |
| `-steamconsole` | Load `steamconsole.so` **(inferred)**. |
| `-friendsui` / `-nofriendsui` | Load or skip `friendsui.so`. |
| `-clientui` | Uses `clientui.so` / `clientui/fonts/GoNotoKurrent-*.ttf` **(inferred)**. |
| `-gamepadui` | Start in Big Picture / gamepad UI. |
| `-steamdeck`, `-steamos`, `-steamos3`, `-holo` | Platform selection: Steam Deck / SteamOS 3 (holo) **(inferred)**. |
| `-steamdeckdisplay`, `-steammachinedisplay` | Display panel or device profile **(inferred)**. |
| `-steamframe`, `-deckard`, `-tesla` | Hardware codenames. `Deckard` and `controller_steamframe_pair` also appear as strings **(inferred: VR/hardware device modes)**. |
| `-steamchina` | Steam China (Perfect World) build or universe. A `steamrt64/steamchina` path also appears in strings. |
| `-steamrow` | Rest-of-world counterpart to `-steamchina` **(inferred)**. |
| `-windowed`, `-fulldesktopres` | Window mode options **(inferred)**. |
| `-silent` | Start minimized to tray. |
| `-singleapp` | **(inferred)** Single-app / kiosk mode. |
| `-language <lang>` | UI language. Also selects the `public/steambootstrapper_<lang>.txt` table. |
| `-login`, `-logon` | Followed by credentials: auto-login. |
| `-exitsteam`, `-ifrunning` | **(inferred)** Ask a running instance to exit, or act only if Steam is running. |
| `-hometest` | **(inferred)** Test the home-directory setup (`%s/.steam/...`). |
| `-dev`, `-devsites`, `-devsiteshost <host>` | Developer mode and developer web sites. |
| `-master_ipc_name_override <name>` | Override the IPC/shared-memory name **(inferred)**. |
| `-disable-libusb` / `-enable-libusb` | From `steamclient.so`: "Disable/Enable support for controllers requiring exclusive USB access". |
| `-cef-disable-gpu`, `-cef-disable-gpu-sandbox`, `-cef-disable-sandbox`, `-cef-disable-seccomp-sandbox`, `-no-cef-sandbox`, `-cef-force-gpu`, `-cef-force-accessibility` | CEF / steamwebhelper switches, passed through to the webhelper launch. |
| `-chromeos`, `-chromeosverbose`, `-chromeosdiskmanagement`, `-chromeosnopreallocate` | ChromeOS (Borealis) integration modes. |
| `-set_locale_disable` | Don't call `setlocale` **(inferred)**. |

### Debugging and crash handling

| Flag | Meaning |
|---|---|
| `-debugbreak` | Break into the debugger at startup **(inferred)**. |
| `-noassert` | Suppress assert dialogs. |
| `-nocrashdialog` | No crash dialog. |
| `-full_memory_dump` | Full minidumps. Related env var: `BREAKPAD_DUMP_LOCATION`. |
| `-debugoutputlogs` | **(inferred)** Mirror logs to debug output. |
| `-fs_log`, `-fs_logbins`, `-fs_target` | Filesystem access logging (`filesystem_stdio`) **(inferred)**. |
| `-nojsreload` | Disable Steam UI JavaScript hot-reload **(inferred)**. |

### Options the bootstrapper passes to helper programs

These strings are arguments the bootstrapper builds for programs it launches, not flags it accepts:

* `--alongside-steam`, `--terminate-when-signaled`: passed to `steam-runtime-launch-client` / `steam-runtime-supervisor`.
* `--error`, `--warning`, `--title`: passed to `steam_msg.sh`.
* `--filename=console-linux.txt`: passed to srt-logger.

`steam://close`, `steam://openurl/`, `steam://openurl_external/` and `steam://vr_connection_ready/` are URLs the bootstrapper handles or forwards.

---

## 2. Environment variables found in the bootstrapper strings

| Variable | Also in | Meaning |
|---|---|---|
| `STEAM_RUNTIME_LOGGER` | steam.sh | Log string "srt-logger: enable configured via STEAM_RUNTIME_LOGGER: %d". `0` disables `console-linux.txt` logging. **(inferred)** `1` forces it on. |
| `STEAM_CLIENT_LOG_FOLDER` | steam.sh, srt-logger, client | Log folder name, default `logs`. |
| `STEAM_RUNTIME_STEAMRT` | steam.sh, client, webhelper | Custom steamrt3c runtime path. |
| `STEAM_RUNTIME` | — | Unset or checked when re-executing between scout and steamrt3. Related strings: `ReexecToLauncher: …`. |
| `STEAM_STEAMRT_RECURSION_GUARD` | gamelauncher | Guards against the steamrt64 and scout launchers re-execing each other in a loop **(inferred)**. |
| `STEAM_BOOTSTRAP_LOG_VERBOSE` | gamelauncher | Verbose bootstrap log (`logs/bootstrap_log.txt`) **(inferred)**. |
| `STEAM_UPDATEUI_PNG_BACKGROUND` | — | Custom PNG background for the update window. The default is `tenfoot/resource/images/bootstrapper.jpg` **(inferred)**. |
| `STEAM_CLIENT_CONFIG_FILE` | steamclient | Path to `steam.cfg`. steamclient exports it to games (`%s/steam.cfg`). **(inferred)** The bootstrapper honours an override. |
| `STEAM_BIGPICTURE` | gamelauncher | Set for children when Big Picture is active **(inferred)**. |
| `STEAM_GAME` | gameoverlayrenderer, webhelper, streaming_client | Marks game processes **(inferred)**. |
| `STEAM_DESKTOP_APP_AFFINITY_LIST` | tier0, crashhandler, overlay | CPU-affinity list for desktop apps **(inferred)**. |
| `STEAM_ENABLE_DYNAMIC_BACKLIGHT`, `STEAM_USE_DYNAMIC_VRS` | client, webhelper, others | Steam Deck display features. `RADV_FORCE_VRS_CONFIG_FILE` is related. |
| `SDL_VIDEO_DRIVER`, `SDL_VIDEODRIVER` | steam.sh | Wayland fallback handling, as in steam.sh. |
| `GAMESCOPE_WAYLAND_DISPLAY` | — | Detects a gamescope session. |
| `WSL_DISTRO_NAME` | — | Detects WSL **(inferred)**. |
| `XDG_CONFIG_HOME`, `HOME`, `USER`, `TMPDIR` | — | Locating `~/.steam` and temp directories. `xdg-user-dir %s` is used for `%s/.local/share/applications` desktop entries. |
| `ALL_PROXY`, `NO_PROXY` | — | Proxy settings for downloads. |
| `DONT_BREAK_ON_ASSERT` | steam.sh (valgrind) | Assert handling. |
| `BREAKPAD_DUMP_LOCATION` | — | Minidump directory. |
| `SLEEP_BEFORE_ELEVATED_UPDATE` | — | Debug: delay before the elevated update. Mostly Windows. |
| `DBG_PATHMATCH` | — | **(inferred)** Debug for path matching. |
| `CPU_MHZ` | — | Fallback CPU frequency ("Unable to determine CPU Frequency. Try defining CPU_MHZ."). |
| `STEAMVIDEOTOKEN` | — | **(inferred)** Video-streaming auth token. |
| `ENABLE_VK_LAYER_VALVE_steam_overlay_1` | overlay | Vulkan overlay layer enable switch, handled when launching children. |
| `SRT_LOGGER_READY` | logger-0.bash | Status from srt-logger. |

The bootstrapper also performs the scout ⇄ steamrt3 hand-off (`ReexecToLauncher`). Its log strings are:

* `ReexecToLauncher: opted into steamrt3 client`
* `ReexecToLauncher: not opted into steamrt3 client`
* `ReexecToLauncher: Running steamrt64 client but not opted in. Re-starting the scout environment`
* `ReexecToLauncher: don't have a valid steamrt64/steam executable`
* `%s: received re-exec request with code: %d steamrt: %d`

The decision rests on the `.steam-enable-steamrt64-client` flag. It also starts `steam-runtime-supervisor`, `srt-logger` and `steam-runtime-launch-client` ("Failed to start steamrt auxillary proccesses").

---

## 3. Environment variables the client sets for launched games (cross-reference)

This comes from `steamclient.so`, where the strings near `STEAM_CLIENT_CONFIG_FILE` are still in source order. It is here because it is the launch environment the runtime scripts receive.

| Variable | Notes |
|---|---|
| `STEAM_GAME_LAUNCH_SHELL` | Shell used to run launch-option command lines. Default `/bin/sh` (the next string in order). **Undocumented.** |
| `SYSTEM_PATH`, `SYSTEM_LD_LIBRARY_PATH`, `STEAM_RUNTIME_LIBRARY_PATH`, `PATH`, `LD_LIBRARY_PATH`, `LD_PRELOAD` | Rebuilt for the child. |
| `STEAM_COMPAT_FLAGS` (`search-cwd`) | Same mechanism steamwebhelper.sh uses. |
| `FONTCONFIG_PATH` | Also set for compat tools, together with `PROTON_CRASH_REPORT_DIR=/tmp/proton_crashreports`. |
| `SUPPRESS_STEAM_OVERLAY` | Disables the overlay for a launch. |
| `STEAM_LAUNCH_WRAPPER_SCOPE` | Read by `steam-launch-wrapper` (below). |
| `STEAM_CLIENT_CONFIG_FILE` | Set to `<steamroot>/steam.cfg`. |
| `SteamUniverse`, `SteamRealm` | Universe (`Public`/`Beta`/…) and realm (Steam global or Steam China). |
| `STEAM_COMPAT_PROTON`, `STEAM_COMPAT_TOOL_PATHS`, `STEAM_COMPAT_LIBRARY_PATHS`, `STEAM_COMPAT_SHADER_PATH`, `STEAM_COMPAT_INSTALL_PATH`, `STEAM_COMPAT_MOUNTS`, `STEAM_COMPAT_LAUNCHER_SERVICE`, `STEAM_COMPAT_DATA_PATH`, `STEAM_COMPAT_CONFIG`, `STEAM_COMPAT_CLIENT_INSTALL_PATH`, `STEAM_COMPAT_APP_ID`, `STEAM_COMPAT_TOOL_MAPPINGS` | Compatibility tool environment, from compatmanager. |
| `STEAM_EXTRA_COMPAT_TOOLS_PATHS` | **Input.** Extra directories searched for `compatibilitytools.d` tools, in addition to `/usr/share/steam/compatibilitytools.d`, `/usr/local/share/steam/compatibilitytools.d` and `<steamroot>/compatibilitytools.d`. |
| `STEAM_SPEW_LEVELS` | **Input.** `group=level,loglevel` pairs. Log strings: "STEAM_SPEW_LEVELS: Setting '%s' to %d,%d" and "Ignoring unknown spew group". Sets per-group console and log verbosity. **Undocumented debugging switch.** |

### steam-launch-wrapper (`steamrt64/steam-launch-wrapper`, version `0.20240918.0-7-g96985ed`)

| Option | Env equivalent | Meaning |
|---|---|---|
| `--debug` | `STEAM_LAUNCH_WRAPPER_DEBUG` | Debug output. |
| `--app-id=ID` | `SteamAppId` | Used in the scope name `app-steam-app<ID>-<pid>.scope`. |
| `--game-bin` / `--no-game-bin` | `STEAM_LAUNCH_WRAPPER_GAME_BIN` | Prepends `%s/game-bin` to `PATH`. |
| `--journal` / `--no-journal` | `STEAM_LAUNCH_WRAPPER_JOURNAL` | Redirect output to the systemd Journal (identifier `steam-app<ID>`). |
| `--scope` / `--no-scope` | `STEAM_LAUNCH_WRAPPER_SCOPE`, `PRESSURE_VESSEL_SYSTEMD_SCOPE` | Place the game in a transient systemd user scope, via `/run/user/<uid>/systemd/private`. |
| `--oom-score-adjust=N` | — | Set `oom_score_adj`. |
| `--version` | — | Print version. |

Other strings:

* It reads `%s/steam/env/%s`, a per-app environment file. **(inferred)** The base is `$XDG_RUNTIME_DIR`, the only XDG variable in its strings.
* It inspects `PROTON_LOG`, `WINEDEBUG` and `ENABLE_VULKAN_RENDERDOC_CAPTURE`, and logs "STEAM_RUNTIME not in use".

### reaper (`steamrt64/reaper`, `ubuntu12_32/reaper`)

`reaper SteamLaunch AppId=<id> -- <cmd>`. It uses `prctl` to become a subreaper and then `execvp`s the command. Errors: `reaper: no sub-command!`. It has no environment variables.
