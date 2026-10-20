# steam.cfg and file-based switches ("magic files")

Steam Linux client, manifest `1791918634`.

## Method and sources

* **Shell scripts:** I read them directly. See [steam-sh.md](steam-sh.md) and [steam-runtime.md](steam-runtime.md).
* **Native binaries:** I grepped the `strings` dumps (`strs/*.txt`) for file names and config keys. In the tables, "Seen in" lists the steamrt64 binaries that contain the exact string. The `ubuntu12_32` and `linux{32,64}` builds have the same strings unless noted.
* **String order:**
  * The bootstrapper (`steamrt64/steam`, `gamelauncher`), `steamui.so`, and the back half of `steamclient.so` have hash-ordered string tables, so neighbouring strings there tell you nothing.
  * The first ~100k strings of `steamclient.so` are in source order, so key names that sit next to each other there belong together.
* **Meanings:** marked **(inferred)** unless code, a log string or an official string states them.

---

## 1. `steam.cfg` (install root)

**Location:** `$STEAMROOT/steam.cfg` or `$STEAMROOT/Steam.cfg`. Both spellings appear in the bootstrapper strings, and steam.sh checks both. The client also exports the path to games as `STEAM_CLIENT_CONFIG_FILE=<root>/steam.cfg`.

**Format:** plain `Key=Value` lines. steam.sh's regex `^[Uu]niverse *= *[Bb]eta$` shows that spaces around `=` are allowed and that matching is case-insensitive for that key. Valve's own cafe/LAN documentation uses `enable`/`disable` as the value for the `BootStrapper*` keys.

| Key | Read by | Values | Effect |
|---|---|---|---|
| `BootStrapperInhibitAll` | bootstrapper, gamelauncher | `enable` | Disables all bootstrapper update activity: no client update check or download. The steam.sh comments name it as the way to keep a custom runtime ("Inhibit the bootstrapper via Steam.cfg (otherwise the bootstrapper will overwrite it)"). |
| `BootStrapperInhibitUpdateOnLaunch` | bootstrapper | `enable` | Skips only the update check at launch. **(inferred)** Background update checks still happen. Related strings: "Checking for update on startup", "IsUpdateSuppressed", "Suppressing Steam update". |
| `BootStrapperInhibitClientChecksum` | bootstrapper | `enable` | Skips checksum verification of client files, so locally modified files survive. **(inferred)** |
| `BootStrapperInhibitBootstrapperChecksum` | bootstrapper | `enable` | Same, for the bootstrapper binary itself. **(inferred)** |
| `ClientDownloadHost` | bootstrapper | hostname | Replaces the client-update CDN host. Log string: "ClientDownloadHost in Steam.cfg". |
| `Universe` | steam.sh, bootstrapper, steamclient | `Public` (default), `Beta`, … | steam.sh: `Beta` changes the package name to `steambeta`, which changes the `~/.steam/steambeta` data link and `/usr/bin/steambeta` as `STEAMSCRIPT`. The client checks `GetConnectedUniverse() == pfnBootstrapperEUniverse()`, and the universe is exported to games as `SteamUniverse`. Non-public universes are Valve-internal. |
| `CMForce` | steamclient (next to `STEAM_CLIENT_CONFIG_FILE`/`steam.cfg`, in source order) | host:port | Forces a specific Connection Manager server. **(inferred)** |
| `DisableDownloads` | steamclient (same block) | `1` | Disables content downloads. **(inferred)** |

**Not present in this build:** `BootStrapperForceSelfUpdate`. Valve's older cafe documentation lists it, but no binary in this manifest contains the string.

---

## 2. `steam_dev.cfg` (install root)

**Location:** `$STEAMROOT/steam_dev.cfg`.

**Seen in:** steam.sh, bootstrapper, gamelauncher, steamclient.so (read in `CSteamEngine::Init`), steamui.so, gameoverlayui.so.

**What it does:**

* **Marks a development install.**
  * steam.sh: no `~/.steam/steam` (or `steambeta`) symlink is created, the bootstrap tarball is not reinstalled, and `--reset` refuses to run ("Can't reset development directory").
  * Bootstrapper log string: "Skipping ~/.steam/steam symlink, dev environment detected".
* **Sets client convars.** Each line is `name value`. This is community-documented and consistent with the strings: convar names that start with `@` are the ones that can be overridden this way, e.g. `@nClientDownloadEnableHTTP2PlatformLinux 0`, `@fDownloadRateImprovementToAddAnotherConnection 1.0`. Non-`@` settings such as `unShaderBackgroundProcessingThreads` are also reported to work. The full list of `@` convars, with defaults and descriptions where the binary has them, is in [steam-dev-cfg-convars.md](steam-dev-cfg-convars.md).

---

## 3. Flag and state files in the Steam install root (`~/.steam/steam` → `$STEAMROOT`)

| File | Seen in | Effect |
|---|---|---|
| `.steam-enable-steamrt64-client` | steam.sh, bootstrapper, gamelauncher, steamui.so | When present, start the **64-bit SteamRT3 client** (`steamrt64/steam`) instead of the scout `ubuntu12_32/steam`. steam.sh creates or deletes it when `STEAM_FORCE_CLIENT` is set. The bootstrapper logs its decision with "ReexecToLauncher: opted into / not opted into steamrt3 client". The string also appears in steamui.so, so **(inferred)** the client can toggle it, for example through a beta or settings option. |
| `steam_dev.cfg` | many | See section 2. |
| `steam.cfg` / `Steam.cfg` | many | See section 1. |
| `.cef-enable-remote-debugging` | steamui.so | Enables the Chrome DevTools remote-debugging port of steamwebhelper. Community-known: port 8080, inspectable at `localhost:8080`. **Hidden developer switch.** |
| `.cef-dev-tools-size.vdf` | steamwebhelper | Saved size of the DevTools window. **(inferred)** |
| `.cef-initialize-sentinel` | steamwebhelper | Sentinel written during CEF initialisation. **(inferred)** If it is still there on the next start, the previous initialisation crashed, which can trigger GPU or sandbox fallbacks. |
| `.force-ath11k-reload` | steamui.so | Steam Deck (OLED) Wi-Fi workaround: forces a reload of the `ath11k` driver. **(inferred)** Related env var: `SteamDeckWifiResumeWorkaround`. |
| `.crash` | bootstrapper, gamelauncher, steamui.so | Created while Steam runs and removed on clean shutdown. **(inferred)** If it is present at start, the bootstrapper logs "Looks like steam didn't shutdown cleanly, scheduling immediate update check", which leads to update and verification. |
| `.steam-first-start-breadcrumb` | bootstrapper, gamelauncher | Marker for the first-ever start of an install. **(inferred)** |
| `.steam_exec_test` | nearly all binaries (tier0) | Temporary file used to test whether a directory allows execution, i.e. to detect `noexec` mounts. **(inferred)** |
| `<dir>/.writable` (`%s/.writable`) | bootstrapper | Probe file for the "Directory %s not writable." check, which leads to `SteamBootstrapper_NotWriteable` / `ReadOnlyInstall`. |
| `.forceupdate` | bootstrapper, gamelauncher | Forces the bootstrapper to re-apply or re-download the client package. **(inferred)** File-based equivalent of `-forcesteamupdate`. |
| `bootstrap.tar.xz` | steam.sh | Bootstrap archive used for `--reset` and reinstall. |
| `steam.token` | bootstrapper, gamelauncher, steamui.so | **(inferred)** Cached token, e.g. for the embedded login or client session. Valve-internal semantics. |
| `steam.dbg` | bootstrapper | Debug symbol name (`.gnu_debuglink`), not a switch. |
| `ssfn*` | steam.sh (`--reset` keeps them) | Legacy Steam Guard sentry files. |
| `steamapps/`, `SteamApps/`, `userdata/`, `package/` | steam.sh (`--reset` keeps them) | Content and user data. |
| `logs/console-linux.txt`, `logs/webhelper-linux.txt`, `logs/bootstrap_log.txt` **(inferred name)**, `logs/*.previous.txt`, `logs/container-runtime-info.txt.XXXXXX`, `logs/ipc_%s.log`, `logs/netapi_log.txt`, `logs/service_log.txt`, `logs/gameoverlay_renderer.txt`, `logs/gameoverlay_ui.txt`, `logs/vrhw_*.vdf` | various | Log files. The folder name comes from `STEAM_CLIENT_LOG_FOLDER`, default `logs`. |
| `dumps/`, `dumps/reports/` | steamclient | Crash dumps (`*.dmp`). |
| `config/mangohud.conf` | steamclient/steamui | MangoHud configuration that Steam writes for its performance overlay (`MANGOHUD_CONFIGFILE`). **(inferred)** |
| `appcache/sdr_config.txt` | steamclient | Cached Steam Datagram Relay config. |
| `steamrt64/pv-runtime/steam-runtime-steamrt{,.tar.xz,.version.txt,.VERSIONS.txt}` | steam.sh, scripts, bootstrapper | steamrt3c runtime. A version file that differs from the unpacked one triggers a re-unpack. |
| `ubuntu12_32/steam-runtime{,.tar.xz,.tar.xz.checksum,/checksum}` | steam.sh | Scout runtime. |
| `ubuntu12_32/steam-runtime/pinned_libs_{32,64}/{done,has_pins,system_*}` | scout `setup.sh` | Library-pinning state. Deleting `done` forces re-pinning. |
| `steamrt64/pv-runtime/steam-runtime-steamrt/var/` | `_v2-entry-point`, `run` | pressure-vessel variable dir (runtime copies, `slr-*.log`). It must not be a symlink. |
| `steam-dialog` | `steam-runtime-steamrt.sh`, launch-options | If `~/.steam/root/steam-dialog` is executable, it is preferred over zenity. |

### `package/` (bootstrapper state)

| File | Seen in | Effect |
|---|---|---|
| `package/beta` (`%s/beta`) | bootstrapper | Holds the name of the opted-in **client beta**. Log string: "Opted in to client beta '%s' via beta file". `-setbeta`/`-clearbeta` change it. `-clientbeta` overrides it for one session without writing it. Delete it to leave the beta (equivalent to `-clearbeta`). |
| `package/beta_cache.vdf` | steamclient/steamui | Cached list of available client betas. **(inferred)** |
| `package/steam_client_<platform>[_<beta>].manifest` | bootstrapper (`steam_client_`, `%s/%s/%s.manifest`) | Downloaded client manifest. Same format as `manifest.vdf` in this work dir: per-package `file`, `size`, `sha2`, `zipvz`, `sha2vz`, plus the top-level `version`. |
| `package/*.zip.<sha>`, `*.installed` | bootstrapper | Package zips and markers for installed packages. "Package file %s missing or incorrect size, not installing update". |
| `package/update_hosts_cached<suffix>.vdf` **(path inferred)** | bootstrapper, steamclient | Cached list of client-update hosts (`clientupdatehosts`). |
| `package/*.old`, `*.old.N`, `*.temp_write_*`, `*.async*.tmp` | bootstrapper | Rollback and atomic-write temporaries ("Failed to apply update, reverting..."). |

---

## 4. Files in `~/.steam/` (`STEAMCONFIG`)

| File | Seen in | Effect |
|---|---|---|
| `steam.pid` | steam.sh, all UI binaries | PID of the running Steam. With `steam.pipe` it is used to detect a running instance. |
| `steam.pipe` | steam.sh, bootstrapper | Command FIFO. A second `steam` invocation forwards its command line through it and exits. steam.sh checks that the PID holds it open. |
| `starting` | steam.sh | Touched just before the client launches, to detect bootstrap launch failure. |
| `registry.vdf` | steam.sh (`--reset` renames it to `.bak`), all binaries (`registry.vdf`, `%s/Steam/registry.vdf`) | Emulated Windows registry. See [on-disk-config-files.md](on-disk-config-files.md). |
| `machine-id` (`~/.steam/machine-id`) | bootstrapper, client, UI | Steam's own machine ID, used alongside `/var/lib/dbus/machine-id`. **(inferred)** |
| `root`, `steam` (or `steambeta`), `bin32`, `bin64`, `sdk32`, `sdk64`, `bin` | steam.sh | Symlinks to the install and its library dirs. `sdk32`/`sdk64` are what games and dedicated servers use to find `steamclient.so`. |
| `~/.steampath`, `~/.steampid` | steam.sh | Legacy symlinks in `$HOME`. |

---

## 5. System-wide paths checked

| Path | Checked by | Effect |
|---|---|---|
| `/etc/ca-certificates/trust-source/anchors/constraind-valve-ca.cer` | `ubuntu12_64/steamwebhelper.sh` | **Valve-internal switch:** if present, `PRESSURE_VESSEL_IMPORT_CA_CERTS=1`, so host CA certificates are imported into the webhelper container ("testing against dev stores"). |
| `/proc/sys/kernel/unprivileged_userns_clone`, `/proc/sys/user/max_user_namespaces` | steamwebhelper.sh | A value of `0` makes the script add `--no-sandbox` for CEF. |
| `/.flatpak-info` | steamwebhelper.sh | Flatpak detected: adds `--no-sandbox`. |
| `/run/pressure-vessel` | pv-run.sh | Refuses to run inside a container. |
| `/usr/share/steam/compatibilitytools.d`, `/usr/local/share/steam/compatibilitytools.d` | steamclient | System compat tool directories. Extra ones come from `STEAM_EXTRA_COMPAT_TOOLS_PATHS`. |
| `/usr/lib/steam/bootstraplinux_ubuntu12_32.tar.xz` (`steambeta` variant) | steam.sh | Distro package's copy of the bootstrap. |
| `/usr/share/applications/steam.desktop`, `steambeta.desktop`, `~/.local/share/applications` | bootstrapper | Desktop-entry install and check. system-info reports `SRT_STEAM_ISSUES_MISSING_STEAM_URI_HANDLER` when it is missing. |
| `/tmp/.steam-sem-names` | tier0 (most binaries) | Registry of named-semaphore names. **(inferred)** |
| `/tmp/steam_startup_messages_$USER.txt` | steam.sh | Fallback message log. |
| `/tmp/proton_crashreports` | steamclient | Default `PROTON_CRASH_REPORT_DIR`. |
| `/usr/lib/jupiter-dock-updater/jupiter-dock-updater-mock.sh` | bootstrapper | Steam Deck dock firmware updater (mock path in strings). **(inferred)** |
| `bin/hardwareupdater/hardwareupdater.cfg` (shipped) | hardwareupdater | Controller firmware timestamps. See [fossilize-filters.md](fossilize-filters.md) §3. |
| `/etc/lsb-release`, `/etc/os-release`, `/etc/debian_version` | steam.sh | Used only for the distro log line. |
