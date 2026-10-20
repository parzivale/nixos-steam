# On-disk configuration files used by the client

Steam Linux client, manifest `1791918634`.

## Method and evidence

The client writes these files at runtime, so none of them ship in the depot. The key names below come from the `strings` dumps of the binaries. Each table gives an evidence source:

* **SC-ordered**: `strs/steamrt64__steamclient.so.txt` in its first ~100k lines. Strings there are in source order, so a key list sitting right after a filename string is the set of keys written to that file. This is the strongest evidence.
* **SC**: present somewhere in `steamclient.so`, but in the hash-ordered region. The file a key belongs to is then **inferred**.
* **UI**: present in `steamui.so`. That table is hash-ordered, so attribution is **inferred**.
* **BS**: present in the bootstrapper `steamrt64/steam`. Hash-ordered.
* **Script**: seen in a shell script.

All VDF files are Valve KeyValues text, `"key" "value"` pairs and `{ }` blocks, except `appinfo.vdf`, `packageinfo.vdf` and `shortcuts.vdf`, which are binary KeyValues. Paths are relative to the Steam root unless stated.

---

## 1. Config stores: `config/config.vdf`, `localconfig.vdf`, `sharedconfig.vdf`, `local.vdf`

SC-ordered strings: `InstallConfigStore`, `UserRoamingConfigStore`, `UserLocalConfigStore`, `MachineUserConfigStore`, followed by `local_%s.vdf`, `local.vdf`, `config.vdf`, `sharedconfig.vdf`, `localconfig.vdf` and `config`.

| Store (root key) | File | Scope |
|---|---|---|
| `InstallConfigStore` | `config/config.vdf` | Machine / install |
| `MachineUserConfigStore` | `local.vdf` / `local_<x>.vdf` | Per-machine-per-user, e.g. `userdata/<accountid>/config/…` **(inferred location)** |
| `UserLocalConfigStore` | `userdata/<accountid>/config/localconfig.vdf` | Per-user, not synced |
| `UserRoamingConfigStore` | `userdata/<accountid>/7/remote/sharedconfig.vdf` **(path is community knowledge)** | Per-user, cloud-synced (app 7 = Steam client cloud). Strings: `@nRoamingConfigReconnectCloudSyncWindowSec`, `LastConfigstoreUploadTime`. |

Log strings about the stores:

* "CConfigStore::FlushToDisk() - saving roaming config while in offline mode"
* "Config store has m_bDisableDiskSave on beta or public!"

Inside each store, keys use Windows-registry-style paths, written in the binaries as `Software\Valve\Steam\…`. Every path starting with `Software\Valve\Steam` is listed below (86 unique strings in steamclient).

### 1a. `Software\Valve\Steam\…` paths found in steamclient.so

The store column is **inferred** from community-observed file contents unless stated.

| Path (after `Software\Valve\Steam\`) | Likely store / file | Notes |
|---|---|---|
| `Accounts` (+ `\SteamID`) | config.vdf | Account name to SteamID cache (`CUser::CacheAccountNameAndSteamID`). |
| `Apps\%u` (`\LastPlayed`, `\Playtime`, `\Playtime2wks`, `\PlaytimeDisconnected`, `\DisableUpdatesUntil`, `\BadgeData`, `\cloud\last_sync_state`, `\cloud\%s`, `\%s`) | localconfig.vdf | Per-app user state. Playtime keys are SC-ordered next to `GetAppMinutesPlayedData`. |
| `apps\%u\cloudenabled`, `apps\%u\cloudsynconsuspendenabled` | sharedconfig/localconfig | Per-app Steam Cloud toggles. |
| `%s\apps\%u\autocloud\lastlaunch`, `\lastexit` | localconfig | Auto-Cloud session bookkeeping. |
| `Apps\%u_%u` | localconfig | Per-app, per-launch-option entry (next to `LaunchOptions`, `%command%`, `workingdir`, `RunAsAppID`). |
| `%s\Apps\%d\betadate_%s`, `betadesc_%s`, `betahash_%s` | localconfig | App beta branch info. |
| `CompatToolMapping` (`%s\%u\Name`, `\Config`, `\Priority`) | config.vdf | Steam Play / Proton tool chosen per app; `0` = global default. SC-ordered in compatmanager. |
| `ToolMapping`, `Tools\%u\Registered`, `Tools\%u\SizeOnDisk` | config.vdf | Registered tools. |
| `ConnectCache`, `cip`, `CurrentCellID`, `CellIDServerOverride`, `TimeCellIDSet` | config.vdf | CM / cell selection cache. |
| `Depots\%u\DecryptionKey` | config.vdf | Cached depot keys. |
| `DownloadThrottleKbps`, `DownloadsUseHTTPSWhenPossible`, `RecentDownloadRate`, `StreamingThrottleEnabled` | config.vdf | Download settings. Also SC-ordered: `GlobalDefaultAppUpdateBehavior`, `AllowDownloadsDuringGameplay`, `AutoUpdateWindowStart`, `AutoUpdateWindowEnd`, `AutoUpdateWindowEnabled` (next to `libraryfolders.vdf`). |
| `RecentTCPFailures`, `RecentUDPFailures`, `RecentWebSocket443Failures`, `RecentWebSocketNon443Failures`, `PercentDefaultWebSockets` | config.vdf | Connection heuristics. |
| `Embedded\%d`, `Embedded\%d\LastSteamID`, `Embedded\%d\LastBetaSteamID` | config.vdf | Embedded-client logins. |
| `IsSteamDeck`, `IsSteamDeck_01` | config.vdf | Device flag. |
| `LastConfigstoreUploadTime`, `LastPlayedTimesSyncTime` | localconfig | Sync timestamps. |
| `MaxServerBrowserPingsPerMin`, `Rate` | config.vdf / registry | Server browser and network rate. |
| `MTBF` | config.vdf | Stability telemetry counter. |
| `NoSavePersonalInfo` | config.vdf / registry | "Don't save account credentials on this computer" (cafe mode). |
| `Perf\GameProfiles`, `Perf\GameProfiles\App` | localconfig | Per-game performance profiles (Deck). |
| `PlayerLevel` | localconfig | |
| `PPU` | ? | **(unknown)** |
| `ShaderCacheManager\…` (`App\%u\ShaderCacheSize`, `CommittedDepotManifests`, `CompatToolBucketHashes`, `CurrentBucketDriver`, `CurrentBucketGPU`, `DisableShaderCache`, `EnableShaderBackgroundProcessing`, `HasCurrentBucket`, `LastSeenBackendHitCacheGeneration`, `ProcessingQueue`) | config.vdf | Shader pre-caching. `DisableShaderCache` and `EnableShaderBackgroundProcessing` back the Settings › Shader Pre-Caching toggles **(inferred)**. |
| `Shortcuts\%u` | localconfig | Per-shortcut state. |
| `SurveyDate`, `SurveyDateType`, `SurveyDateVersion` (UI also has `SurveyDateBeta`, `SurveyDateSteamDeckDelay`, `SurveyID`) | config.vdf | Hardware survey scheduling. |
| `System\…` (`AdaptiveBrightnessEnabled`, `DisplayBrightness`, `DisplayColorGamut`, `DisplayColorTemp`, `DisplayColorTempEnabled`, `DisplayNightMode*` ×9, `FanMode`, `IdleBacklightDimACSeconds`, `IdleBacklightDimBatterySeconds`) | config.vdf | SteamOS / Deck system settings. |
| `CloudEnabled` | sharedconfig | Global cloud toggle. |
| `Software\Valve\SteamService` | registry | Service install (Windows heritage). |

### 1b. Other store-relative keys found (no `Software\…` prefix)

SC means steamclient, UI means steamui.

| Prefix | Keys | Evidence |
|---|---|---|
| `Authentication\` | `RememberedMachineID` | SC, UI |
| `Broadcast\` | `DelaySeconds`, `EncoderSetting`, `FirstTimeComplete`, `IncludeDesktop`, `MaxKbps`, `OutputHeight`, `OutputWidth`, `Permissions`, `RecordMic`, `RecordSystemAudio`, `ShowChat`, `ShowDebugInfo`, `ShowReminder` | SC, UI |
| `GameRecording\` | `Audio_Mic`, `BackgroundMaxKeep`, `BackgroundRecordMode`, `BackgroundRecordPath`, `BackgroundTimeResolution`, `BitRateKbps`, `ExportCodec`, `ExportDirectory`, `ExportLimitHeight`, `ExportLimitSize`, `ExportLimitType`, `ExportLimitWidth`, `ForceMicMono`, `InstantClipKey`, `MarkerKey`, `MaxFPS`, `Recording_Audio_Option`, `ToggleKey`, `VideoBitRate`, `VideoMaxHeight` | UI (`BackgroundRecordMode` also SC) |
| `GameStream\` | `EnableVideoH265`, `HardwareVideoEncode` | UI |
| `streaming_v2\` | `WifiAPChannel5GHz`, `WifiAPChannel6GHz`, `WifiAPChannelWidth`, `WifiAPEnabled`, `WifiAPHotspotMode`, `WifiAPHotspotPassword`, `WifiAPHotspotRouting`, `WifiAPHotspotSSID`, `WifiAPPairedPassword`, `WifiAPPairedSSID`, `WifiAPPairedTime`, `WifiAPPlanChannelOverride`, `WifiAPPlanHidden`, `WifiAPPlanMode`, `WifiAPPlanName`, `dongle\%llu\%s` | SC |
| `Music\` | `DownloadHighQualityAudioSoundtracks`, `MusicVolume`, `PauseOnAppStartedProcess`, `PauseOnVoiceChat` | SC, UI |
| `FamilyGroup\` | `country`, `groupid`, `members`, `members\%d\accountid`, `members\%d\role`, `name`, `role`, `version` | SC |
| `Offline\` | `EncryptedSignature`, `EncryptedTicket`, `Signature`, `Ticket` | SC (offline-mode logon ticket) |
| `ParentalSettings\` | `Settings`, `Signature` | SC |
| `SharedAuth\` | `AuthData`, `ID` | SC (family library sharing) |
| `PeerContent\` | `ClientMode`, `ServerMode` | SC (LAN peer content: 0=off, 1=only me, 2=friends, 3=anyone, per `nPeerContentDefaultMode` help) |
| `VR\` | `AttemptingInit`, `BuildIDAttempted`, `BuildIDCompleted` | SC |
| `NameHistory\` | `0`, `%d` | SC |
| `controller_config\` | `autosave`, `%s\usetime` | SC, UI |
| `controller_registration\%s_%s\%u\` | `personalization_file_id`, `registration_complete` | SC |
| `%u\` | `UseSteamControllerConfig`, `SteamControllerRumble`, `SteamControllerRumbleIntensityV2` | SC, UI (per-app Steam Input) |
| `%d\` | `OverlayAppEnable`, `CDDialog` | SC, UI |
| `system\` | `EnableGameOverlay`, `EnableSCTenFootOverlayCheckNew`, `EnableUISounds`, `GameOverlayHomePage`, `InGameOverlayScreenshotSaveUncompressedPath`, `InGameOverlayShortcutKey`, `InGameOverlayShowFPSSaturation`, `JumplistSettings`, `SteamVRHMDVGUIWarning` | UI |
| `FriendsUI\` | `FriendsUIJSON` | UI (friends settings blob in localconfig) |
| `WebStorage\` | `Auth\AlwaysShowUserChooser`, plus other WebStorage keys | UI (the steamui JS persists its localStorage into `WebStorage`) |
| `CloudManager\` | `HintAppsToPreload` | UI |
| `Storage\` | `NextTrimRunTime` | UI |
| `news\` | `NotifyAvailableGames` | UI |
| `launcher\` | `appid` | UI |
| `UserAppConfig\%u` | | SC |
| `Developer\` | `HDRCompatTesting` | SC-ordered (compatmanager) |
| `%s\%s\` | `LastLoadValue`, `LastPingTimestamp`, `LastPingValue` | SC (server browser) |
| `%s\` | `ipv6check_%s_state`, `DeviceID`, `Secret`, `Expiry`, `Authorized`, `NoSavePersonalInfo` | SC |
| `%s\` | `Rate`, `SmallMode`, `ShowScreenshotManager`, `Apps\%i\IgnoreInstallError` | UI |
| (top level) | `Software\Valve\Source\Settings`, `KHKEY_CURRENT_USER\Software\Valve\Steam\GamescopeEnableAppTargetRefreshRate2` | UI |
| appinfo `config\` | `CheckForUpdatesBeforeLaunch`, `ExternalRegistrationURL\default`, `ExternalRegistrationURL\%s`, `GameOverlay_CompatMode`, `GameOverlay_TestMode`, `IgnoreIdleTimeout`, `LaunchWithoutWorkshopUpdates`, `NoUpdatesAfterInstall`, `oscpu`, `oslist`, `SteamTraceEnter`, `SteamTraceExit`, `SteamTraceModule`, `UseLaunchCommandLine`, `videoformat`, `steam_china_only\steam_china_duration_control_show_interstitial` | SC/UI. These are **appinfo** "config" section keys, not user files. Listed here because they control launch behaviour. |

---

## 2. `registry.vdf` (`~/.steam/registry.vdf`)

**Evidence:**

* steam.sh renames `$STEAMCONFIG/registry.vdf` on `--reset`.
* The strings `registry.vdf` and `%s/Steam/registry.vdf` appear in every major binary (tier0 registry emulation).
* `HKEY_CURRENT_USER`, `HKEY_LOCAL_MACHINE`, `HKEY_CLASSES_ROOT` and the `*_WOW64_*` variants appear in the bootstrapper.

**Structure** (community knowledge, consistent with the hive names): `"Registry" { "HKCU" { "Software" { "Valve" { "Steam" { … } } } } "HKLM" { … } }`. On Linux this file emulates the Windows registry for Steam's own registry API calls.

| Key (under `HKCU\Software\Valve\Steam`) | Evidence | Meaning |
|---|---|---|
| `AutoLoginUser` | UI | Account name used for auto-login. |
| `RememberPassword` | UI, SC-ordered (also a `loginusers` key) | |
| `AlreadyRetriedOfflineMode` | UI | |
| `Language`, `language` | BS, SC, UI | Client UI language. |
| `SkinV5` | UI | Selected skin (empty = default). |
| `StartupMode`, `StartupModeTmp` | UI | Startup window (library, store, …) and a one-shot override. |
| `SteamExe` | UI | Path to the steam executable. |
| `SourceModInstallPath` | UI | `steamapps/sourcemods` location. |
| `SteamPID` | BS | PID of the running Steam (Windows-style pid record; on Linux `~/.steam/steam.pid` serves the same role). |
| `Universe` | BS, SC, UI | Universe name. |
| `Restart` | SC, UI | **(inferred)** restart request flag. |
| `GamescopeEnableAppTargetRefreshRate2` | UI (`HKEY_CURRENT_USER\…`) | Gamescope / Deck setting. |
| `Rate` (`%s\Rate`) | UI, SC | Network rate. |
| `BootStrapperVersion` | BS | **(inferred)** written by the bootstrapper. |

`ActiveProcess\{pid,SteamClientDll,SteamClientDll64,ActiveUser}` and `RunningAppID` are well-known `registry.vdf` keys, but none of them exist as literal strings in these binaries (they are probably built at runtime), so they are not confirmed here.

---

## 3. `config/loginusers.vdf`

Evidence: `loginusers.vdf` in UI; `config/` in SC; the log-upload string `loginusers.vdf.error` in SC-ordered.

Structure: `"users" { "<SteamID64>" { … } }`.

| Key | Evidence |
|---|---|
| `AccountName` | UI, SC |
| `PersonaName` | UI, SC |
| `RememberPassword` | UI, SC |
| `WantsOfflineMode` | UI |
| `SkipOfflineModeWarning` | UI |
| `AllowAutoLogin` | UI |
| `MostRecent` | UI |
| `Timestamp` | UI, SC |

The siteserver/cafe variant writes `users` → `AccountName`, `RememberPassword`, `Timestamp` (SC-ordered, next to `%s/config`, `%s/siteserverui`, `SiteServer`, `language`; i.e. `config/siteserver.vdf` **(inferred)**).

---

## 4. `steamapps/libraryfolders.vdf` and `<library>/libraryfolder.vdf`

The SC-ordered strings give the following.

**Global file** (`config/libraryfolders.vdf`, mirrored at `steamapps/libraryfolders.vdf`):

* Root key `libraryfolders`. The legacy key `LibraryFolders` is also accepted when loading ("Loaded Steam library folders configuration: %s"; "Steam library folders configuration will be reset.").
* Under it, one numbered entry per library, `"0" { … }`, `"1" { … }`, and so on.

| Key | Meaning |
|---|---|
| `path` | Absolute library path. It must be absolute, must not be nested inside another library, and must not duplicate another library. Read-only libraries get a warning. |
| `label` | User label. |
| `contentid` | 64-bit random ID of the library ("Mounted library folder "%s" : content id %llu"). |
| `totalsize` | Drive size. |
| `update_clean_bytes_tally` | Bytes verified clean since the last corruption. Used by `@nContentUpdateAutoVerify*`. |
| `time_last_update_verified` | Last auto-verify time ("Last verify in '%s' was %u days ago, clean bytes tally reset to 0"). |
| `time_last_update_corruption` | **(community-observed; not found as a string)** |
| `apps { "<appid>" "<size>" }` | Installed apps in this library. |

**Per-library file** (`<library>/libraryfolder.vdf`): `contentid`, `label`, from the SC-ordered block containing `LibraryFolder`, `contentid`, `label`. Default library folder name: `SteamLibrary`; content subfolder `steamapps`.

The per-library `steamapps/` directory contains:

* `appmanifest_<appid>.acf`
* `common/`
* `downloading/`
* `temp/`
* `shadercache/`
* `compatdata/`
* `workshop/` (`appworkshop_<appid>.acf`, `content/<appid>/<itemid>/`)
* `content/` (depot builder)

---

## 5. `steamapps/appmanifest_<appid>.acf`

Evidence: SC-ordered block under `CSteamClientApp::BYieldingWriteAppState`, with the filename strings `%s/%s_%u.acf`, `\%s_*.acf` and `appmanifest`.

Root key `AppState`:

| Key | Meaning |
|---|---|
| `AppID` | |
| `Universe` | Universe of the install (1 = public). |
| `Name` | |
| `StateFlags` | `EAppState` bitmask (4 = fully installed, 1026 = update required + update running, …). |
| `InstallDir` | Folder under `steamapps/common`. |
| `DebugInstall` | **(inferred)** developer install flag. |
| `LastUpdated` | Unix time. |
| `LastPlayed` | Unix time. |
| `SizeOnDisk` | |
| `StagingSize` | |
| `BuildID` | |
| `LastOwner` | SteamID64 of the license owner. |
| `DownloadType` | |
| `UpdateResult` | `EAppUpdateError`. |
| `BytesToDownload`, `BytesDownloaded`, `BytesToStage`, `BytesStaged` | Progress of the current update. |
| `TargetBuildID` | |
| `AutoUpdateBehavior` | 0 = always keep updated, 1 = only update on launch, 2 = high priority. |
| `AllowOtherDownloadsWhileRunning` | 0 = use global setting, 1 = allow, 2 = never. |
| `ScheduledAutoUpdate` | Unix time of a scheduled background update. |
| `FullValidateBeforeNextUpdate`, `FullValidateAfterNextUpdate` | Force a verify around the next update. |
| `SingleFileUpdateMode` | **(inferred)** |
| `StagingFolder` | Index of the library used for staging. |
| `InstalledDepots { "<depotid>" { "manifest" "size" "dlcappid" } }` | |
| `CheckGuid` | **(inferred)** |
| `InstallScripts { "<depotid>" "<path>" }` | |
| `SharedDepots { "<depotid>" "<appid>" }` | Depots imported from another app (`%u/sharedinstall`, `%u/depotfromapp`). |
| `StagedDepots` | Depots staged for the pending update. |
| `DlcDownloads` | |
| `UserConfig { "language" "betakey" … }`, `MountedConfig { … }` | Requested vs. currently mounted config. Keys seen in the same block: `language`, `BetaKey`/`betakey`, `sharedinstall`, `shadercachedepot`, `NoUpdatesAfterInstall`, `VerifyUpdates`, `releasestatesteamchina`. |
| `PrivateDepots` | |

Related files:

* `steamapps/workshop/appworkshop_<appid>.acf`. Root `AppWorkshop` with `AppID`, `SizeOnDisk`, `NeedsUpdate`, `NeedsDownload`, `TimeLastUpdated`, `TimeLastFullCheck`, `TimeLastAppRan`, `LastBuildID`, `WorkshopItemsInstalled { <id> { size, timeupdated, manifest } }` and `WorkshopItemDetails`. All SC-ordered.
* `depotcache/<depot>_<manifest>.manifest`. Binary depot manifests.
* `steamapps/state_<appid>.files`, `state_<appid>_*.patch`, `depot_<id>_*.delta`. Update staging state.

---

## 6. Compatibility tools: `compatibilitytools.d/<tool>/compatibilitytool.vdf` and `toolmanifest.vdf`

Evidence: SC-ordered compatmanager block.

**Search path** (`CLoadLocalToolListJob`):

* `<steamroot>/compatibilitytools.d`
* `/usr/share/steam/compatibilitytools.d`
* `/usr/local/share/steam/compatibilitytools.d`
* `$STEAM_EXTRA_COMPAT_TOOLS_PATHS` (colon-separated)

Log strings: "Processing local tool list at %s...", "No local tool list detected at %s.".

### `compatibilitytool.vdf`

Root `compatibilitytools` → `compat_tools` → `"<internal name>" { … }`.

| Key | Meaning |
|---|---|
| `install_path` | Relative (usually `.`) or absolute path of the tool. |
| `display_name` | Name shown in the UI. |
| `from_oslist` | Source platform, e.g. `windows`. |
| `to_oslist` | Target platform, e.g. `linux`. A tool for another target platform is ignored ("Ignoring tool %s as it's for a different target platform %s", arm64 is special-cased). |
| `aliases`, `legacy`, `depotid`, `depotsize_mb` | Also parsed in "YldProcessCompatManifests KV version - Compat Tools". Mainly used by appinfo-published tools. |

### `toolmanifest.vdf` (in the tool directory)

Root `manifest`.

| Key | Meaning |
|---|---|
| `version` | Manifest version. Must be 2 for the full feature set (`pTool->nToolManifestVersion == 2`). |
| `commandline` | Command used to run the game. `%verb%` is replaced with `waitforexitandrun`, `run` or `getcompatpath`. |
| `commandline_waitforexitandrun` | Alternate command for the `waitforexitandrun` verb. |
| `commandline_getcompatpath` | Alternate command for the `getcompatpath` verb. |
| `require_tool_appid` | Another compat tool this one runs inside, e.g. Proton requires the Steam Linux Runtime. "Tool %u "%s" has a dependency on tool %u". |
| `unlisted` | Hide from the compat-tool picker. `-compat-disable-filtering` shows such tools anyway ("Disable filtering of normally unlisted runtimes."). |
| `use_tool_subprocess_reaper` | Wrap the tool in `reaper`. |
| `compatmanager_layer_name` | Layer name, e.g. `container-runtime` or `proton`. Used for `STEAM_COMPAT_LAUNCHER_SERVICE` matching. |
| `filter_exclusive_priority` | **(inferred)** Priority in the tool picker. |

Related:

* **App mappings from appinfo** (app 891390 "SteamPlay 2.0 Manifests"): `app_mappings` (`appid`, `tool`, `priority`, `platform`, `config`), `app_compat_configs` (`environment`, `dtst1_compat_category`, `steam_deck_compatibility`, `steam_frame_compatibility`, `configuration`, `recommended_runtime`, `tests`, `token`, `requires_h264`, `requires_voice_files`, `proton_compat_config`, `branch`, `hdr_support`, `rpo_debug`, `fdm_debug`, `tso_enable`), `selectable_aliases`, `default`.
* **User mapping:** config.vdf `CompatToolMapping\<appid>\{Name,Config,Priority}`.
* **Platform override cache:** `userdata/<id>/config/compat.vdf` (`%s/%s/%u/config/%s` + `compat.vdf`) with `platform_overrides { <appid> { dest, src } }` **(inferred key mapping)**.
* **Per-app compat data:** `steamapps/compatdata/<appid>/` (Proton prefix `pfx/`, with the paths `pfx/drive_c/users/steamuser/…` listed in the strings). Deleted when the app is uninstalled ("deleting compatibility data library folder").
* **Client switch:** `-compat-force-slr` "Force enable/disable using SLR 1.0 by default over legacy LD_* setup."

---

## 7. Other per-user files (`userdata/<accountid>/…`)

| File | Evidence | Keys |
|---|---|---|
| `config/localconfig.vdf` | SC-ordered | See §1. |
| `7/remote/sharedconfig.vdf` | SC | See §1. Per-app `tags`, `Hidden`, `cloudenabled` are community-known. |
| `config/shortcuts.vdf` (binary KV) | SC-ordered (`%s/%s/%u/config/%s`) | `shortcuts { "<n>" { AppID, AppName, Exe, StartDir, Icon, ShortcutPath, LaunchOptions, IsHidden, AllowDesktopConfig, AllowOverlay, OpenVR, Devkit, DevkitGameID, DevkitOverrideAppID, LastPlayTime, FlatpakAppID, SortAs, tags { } } }`. A backup copy goes to `logs/shortcuts.previous.txt`. |
| `<appid>/remotecache.vdf` (`%s/%s/%u/%u/remotecache.vdf`) | SC-ordered | `<appid> { ChangeNumber, OSType, <file> { root, size, localtime, time, remotetime, sha, syncstate, persiststate, platformstosync2 } }`. appinfo cloud keys nearby: `rootoverrides`, `oscompare`, `useinstead`, `addpath`, `pathtransforms`, `find`, `replace`. |
| `760/screenshots.vdf` (`%s/%s/%u/%u/screenshots.vdf`) | SC-ordered | `screenshots { <gameid> { <n> { type, filename, thumbnail, vrfilename, imported, timelineid, timelinetime, externalfilename, externalthumbname, externalvrfilename, location, taggedusers, taggedpublishedfiles, spoiler, width, height, gameid, creation, caption, permissions, hscreenshot, publishedfileid } } }`, plus `shortcutnames`. |
| `<appid>/…/steam_autocloud.vdf` | SC | Auto-Cloud marker in the game's save folder (`accountid`). |
| `config/coplay_<steamid>.vdf` | SC-ordered (`config/coplay_%llu.vdf`) | Recent co-players. |
| `config/serverbrowser_hist.vdf`, `serverbrowser_ui.vdf`, `config/serverbrowser.vdf` | SC | Server browser favourites and history. |
| `config/controller_configs/…`, `%llu_controller_config.vdf`, `controller_config/game_actions_<appid>.vdf`, `game_actions_dev.vdf` | SC, UI | Steam Input configs (same schema as `controller_base/*.vdf`; see [fossilize-filters.md](fossilize-filters.md) §4). |
| `config/compat.vdf` | SC-ordered | See §6. |
| `config/playtimelog.vdf`, `personalization.vdf`, `assetcache.vdf`, `data.vdf` | SC | **(inferred)** auxiliary caches. |
| `config/steamevents_<n>.pkv` | SC | **(inferred)** event cache. |

---

## 8. Install-wide caches and miscellaneous files

| File | Evidence | Notes |
|---|---|---|
| `appcache/appinfo.vdf`, `appcache/packageinfo.vdf` | SC-ordered | Binary KV caches of PICS app and package info. |
| `appcache/librarycache/`, `appcache/httpcache/`, `appcache/stats/UserGameStats_<id>_<app>.bin`, `UserGameStatsSchema_<app>.bin` | SC, UI | |
| `config/proxyconfig.vdf` | SC, UI | Proxy settings for the client and webhelper. |
| `config/remoteclients.vdf` | SC | Remote Play paired clients. |
| `config/mangohud.conf` | SC | Performance overlay config (`MANGOHUD_CONFIGFILE`). |
| `legacycompat/evaluatorscript_<n>.vdf`, `installscript_<app>_<x>.vdf`, `standalone_installscript_progress_<app>.vdf` | SC | Install-script execution (`resource/registrykeys.vdf` is a shipped example). |
| `package/beta`, `package/*.manifest`, `update_hosts_cached*.vdf` | BS | See [steam-cfg-and-magic-files.md](steam-cfg-and-magic-files.md). |
| `steam.cfg`, `steam_dev.cfg` | BS, SC | See the same file. |
| `logs/*`, `dumps/*` | SC | Logs and minidumps. |
