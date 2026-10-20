# steamui: hidden, developer, debug and internal options

Source: `root/steamui/sp.js` (the main bundle) and `library.js` (bootstrap), Linux client manifest 1791918634. Found by:

- grepping for non-localized English `label:` / `strLabel:` strings (a strong sign of dev-only UI);
- grepping for the `Settings_Developer_*` localization keys, `DEV_MODE`, `SteamClient._internal`, `window.*` assignments, `DEBUG_*`, and session/local storage keys;
- reading the code that renders the Developer page (module `55136`) and the Valve Internal page (module `26420`).

Labels in quotes are hard-coded English. `#Key` means a localization key, with its English text alongside. Anything marked "inferred" is a guess.

## 1. Gates that unlock hidden UI

| Gate | How it is set | What it unlocks |
|---|---|---|
| `Config.DEV_MODE` (`TS.DEV_MODE`) | `steam://devmode/enable` or `steam://devmode/disable`. The handler also calls `SteamClient._internal.SetDevMode(bool)`. It can also be set with the `?DEV_MODE=true` query parameter on `index.html`/`sp.html` (see injected-config.md). | The **Developer** settings page, and the Steam Console (`IsConsoleEnabled()` = `SHOW_CONSOLE` \|\| `DEV_MODE` \|\| user-enabled). |
| Client setting `developer_mode_enabled` (CMsgClientSettings 20007) | Settings > System > `#Settings_System_EnableDeveloperMode` ("Enable Developer Mode") | The **Developer** page (`/settings/developer`). The page is visible when `developer_mode_enabled \|\| Config.DEV_MODE`. |
| `settings.bIsValveEmail` (legacy settings object) together with developer mode | Account e-mail is a Valve address | The **Valve Internal** page (`/settings/internal`, `#Settings_Page_Internal` = "Valve Internal"). Developer-mode plus Valve-email also gates other internal UI (`Ki()`). |
| `Config.SHOW_CONSOLE` (module `77680`) | Query parameter `SHOW_CONSOLE=...` on `index.html`/`sp.html` | Steam Console tab (`steam://open/console`, `/console`) |
| `Config.IS_STEAMOS`, `PLATFORM=="linux"`, `IN_GAMESCOPE`, `IN_GAMEPADUI` | Injected config / user agent | Many developer items are SteamOS-only or Linux-only (noted below) |
| Compile-time `!1&&` / `Kn=!0` | — | The items "Force QAM perf tab to show all deck settings" and the desktop "Developer Only Settings Zoo" button are compiled out in this build. |

## 2. Developer settings page (`/settings/developer`, module `55136`)

| Section | Item | Backing | Notes |
|---|---|---|---|
| Profiling | `#Settings_Tracing` "Enable System Tracing" ("Toggle background tracing of CPU/GPU events") | `steamos_system_tracing_enabled` | |
| Profiling | `#Settings_Profiling` | perf/profiling service | inferred: graphics profiling |
| Development Kit (SteamOS) | `#Settings_System_Devkit_PairingLabel` "Development host pairing", "Pair new host" | `SteamClient.System.Devkit.SetPairing`, `RespondToPairingPrompt`, `RegisterForPairingPrompt` | Devkit (SteamOS Devkit Client) pairing |
| Steam Play (Linux) | `#Settings_SteamPlay_IsWildcardEnabled` | read-only info | |
| Wi-Fi (SteamOS) | `#Settings_Developer_WiFi_Title` group | `steamos_wifi_debug` ("Enable Wi-Fi debug data collection"), `steamos_wifi_force_wpa_supplicant` ("Force WPA Supplicant Wi-Fi backend"), `steamos_wifi_power_management_enabled` ("Enable Wi-Fi Power Management": "Disabling power management may increase connection reliability on 5GHz networks"), `steamos_wifi_reload_wifi_driver_on_sleep` ("Reload Wi-Fi driver on sleep") | |
| Logging | `#Settings_Developer_EnableECLog` "Enable EC logging" ("Output the EC firmware log to the system journal") | `steamos_ec_logging_enabled` | Shown only when supported |
| Miscellaneous | `#ControllerWelcome_Setting_Label` "Show Steam Controller Tour" | `controller_show_ibex_tour` | |
| Miscellaneous (SteamOS) | `#Settings_Developer_ShowAdvancedOSBranches` "Show Advanced Update Channels" | `show_advanced_update_channels` | |
| Miscellaneous (SteamOS) | `#Settings_Developer_DesktopPreferX11Mode` "Use Legacy X11 Desktop Mode", or `#Settings_Developer_DesktopSessionDropdown` "Session to use for Desktop Mode" | `SetDefaultDesktopSession({session_name})` (`plasma.desktop` / `plasmax11.desktop`) | |
| Miscellaneous (SteamOS) | `#Settings_HDRVisualization_Label` | `gamescope_hdr_visualization` | Options seen in the zoo: None / Heatmap / Heatmap Extended / Heatmap Classic / Analysis |
| Miscellaneous (SteamOS) | `#Settings_System_ForceFormatSD_Label` | `SteamClient.System.FormatStorage` (forced) | |
| Miscellaneous (SteamOS) | `#Settings_Developer_SpeakerTest`, `#Settings_Developer_MuraReArm` "Re-arm Mura Calibration", HDR debug items (`#Settings_HDR_Debug_Force10PQ` "Force output to HDR10 PQ", `#Settings_HDR_Debug_HeatmapEnable`, `#Settings_HDR_Debug_ForceSupport` "Force HDR support"), `#Settings_Developer_ForceTriggerCaptivePortal` | Various components (the HDR ones probably map to `CMsgSystemPerfSettingsGlobal.is_hdr_debug_heatmap_enabled` etc., inferred) | Exact placement inferred from the localization keys |
| Miscellaneous (Gamepad UI) | `#Settings_Developer_ClearGameLaunchInterstitialsSeen` "Clear All" | clears the stored "interstitials seen" state | |
| Miscellaneous (Gamepad UI) | `#Settings_Developer_OpenSteamConsoleTab` | navigates to `/console` | |
| Miscellaneous | `#Settings_Developer_ShowTimestampsInConsole` | `show_timestamps_in_console` | |
| Miscellaneous (Linux) | `#Settings_Developer_EnableGamescopeComposer` | `enable_gamescope_composer` | Requires restart |
| Miscellaneous (Linux) | `#Settings_Developer_EnableGamescopeVRComposer` | `enable_gamescope_composer_vr` | Requires restart |
| Miscellaneous (Linux) | `#Settings_Developer_ForceSystemComposer` "Force system browser composer" | `override_browser_composer_mode` (switches between two enum values, then prompts for a restart) | |
| Miscellaneous | "Enable browserview underlays" ("Allow browserview underlays to be used if hardware requirements are met.") | `browserview_underlays_allowed` | Requires restart |
| Miscellaneous | `#Settings_Developer_CefRemoteDebugging` "CEF Remote Debugging" ("Toggle to auto-enable CEF remote debugging at startup") | `cef_remote_debugging_enabled` | Requires restart. `SteamClient._internal.IsDebuggingEnabled()` adds the report tag `cef_debugging`. |
| Miscellaneous (SteamOS) | `#Settings_System_User_Password` set/change the OS user password | `SetUserPassword({current_password,new_password})` | |
| Miscellaneous | "Force QAM perf tab to show all deck settings" | `force_deck_perf_tab` | Compiled out (`!1&&`), but the QAM still reads the setting |
| Miscellaneous | `#Settings_Developer_HDRCompatTesting` "HDR Compatibility Testing" ("Ignore previously published per-app HDR compatibility information") | `hdr_compat_testing` | |
| Steam Input | `#Settings_Developer_SteamInputDev` "Steam Input Layout Dev Mode" | `steam_input_configurator_error_msg_enable` | |
| Steam Input | `#Settings_Developer_SteamInputConfigAuthor` "Steam Input API Config Author Mode" | `controller_siapi_config_author_mode` | |
| Steam Input | `#Settings_Developer_KeyboardNavGlyphs` "Keyboard Glyphs" | localStorage `GamepadUI_KeyboardNavGlyphsDisabled` (inverted) | |
| (other pages) | `#Settings_Developer_UseGameRefreshRateInSteam` | `gamescope_use_game_refresh_rate_in_steam` | |
| (Power) | `#Settings_Battery_ChargeLimitDevMode` "Allow battery limit full range" | `steamos_charge_limit_devmode` | |
| (SteamOS crash reports) | `Developer_SLS_*`: enable crash reports, minidump, kdump, GPU, journal, system info, devcoredump collection | SteamOS crash-report service | |

## 3. Valve Internal page (`/settings/internal`, module `26420`; requires developer mode and a Valve e-mail)

| Item (hard-coded English) | Backing |
|---|---|
| Buttons "Open Zoo", "Open Drive Info", "Set system Steam as default" / "Set sideload Steam as default", "Add Client Beta" | `/zoo` route; drive info modal; `SteamClient.Settings.ToggleSteamInstall()`; `SteamClient.Settings.AddClientBeta(name, password)` ("Specify a name and password for a new Steam Client beta") |
| "Internal Links": "Lock Screen", "Guided Tour" (resets guided-tour state), "Hardware Survey" | — |
| "Show Debug Focus Ring" | `NavigationManager.SetShowDebugFocusRing`; sessionStorage `focus-nav-show-debug-focus-ring` |
| "Continuously Render Frames" (puts a flashing pixel in the corner so Chromium keeps producing frames instead of showing 0 fps) | MachineStorage key `continuously_render_store` |
| "Enable Soft Process Kill" | `SteamClient.Settings.SetEnableSoftProcessKill`; legacy `bEnableSoftProcessKill` |
| "Force Beta Section Visible" | localStorage `Internal_ForceBetaSectionVisible` |
| "Remain in Big Picture Mode on Window Close" ("Changing setting will exit Big Picture Mode to apply."; hidden in gamescope) | localStorage `Internal_RemainInBigPictureModeOnClose` |
| "Enable Native Resolution on External Displays" (gamescope only) | `gamescope_native_external_res_in_steam` |
| "Log Settings": "Enabled Debug Logs", "Include backtrace in logs", "Allow css in log styling" | localStorage `EnabledWebLogs`, `IncludeBacktraceInLog`, `AllowCSSInLogColors` |
| "Internet Connectivity Test": "Simulate connectivity condition" = None / Not connected to AP (NoLAN) / No Internet / Captive Portal - redirected / Captive Portal - in place / Can't connect to Steam | `SetNetFakeLocalSystemState(k_ENetFakeLocalSystemState_*)`; shows "Connectivity state" and "Captive portal detected" |
| "Miscellaneous": "Use New Achievements Pages" (read-only indicator), "Enable Hardware Updater" | `hardware_updater_enabled` (requires restart) |
| "Accessibility": "Enable Accessibility Debug Visualizer" | `accessibility_debug_visualizer` |
| "Video": "Video Test Pattern", "Audio Sync Clap" | test modals |
| "Reboot to alternate system partition" | `SteamClient.System.RebootToAlternateSystemPartition` |
| "Delete all CEF & internal HTTP client data" | `SteamClient.Settings.ClearAllHTTPCaches` |
| "Display": "Show advanced display scaling settings for internal display", "Reset window size" (1280x800), "Show display scale dialog", `#Settings_Developer_UseGameRefreshRateInSteam` | storage key `AllowInternalDisplayScaling`; `gamescope_use_game_refresh_rate_in_steam` |
| "Bluetooth WakeAllowed" (per paired device toggle) | Bluetooth device wake permission |
| "Constrain GamepadPage width" / "Max width in virtual pixels" (200–2000) | localStorage `GamepadPage_MaxWidthEnabled_2`, `GamepadPage_MaxWidth` |
| "Show debug pointer", "Debug pointer size" (1–100, default 12), "Debug pointer opacity (when inside window)" (default 1), "Debug pointer opacity (when outside window)" (default 0.5) | localStorage `DebugPointer_Enabled`, `DebugPointer_Size`, `DebugPointer_Opacity_Hovering`, `DebugPointer_Opacity_NotHovering` |
| OOBE: "Restart into Gold Master OOBE" ("Are you sure you want download and boot into Gold Master?"), "Do a clean OOBE?", "Show OOBE UI Without Restart", "Show OOBE Stage 2 UI Without Restart", `#Settings_ForceOOBE` "Force OOBE", "Force OOBE Stage 2" | `TriggerGoldMasterOOBETest`; `force_oobe`; `force_stage_2_oobe` |
| "Show Advanced Display Options [main only]" | Display page extra options |
| Haptics test: "Haptic Type" Tick/Click, "Intensity", "Gain", "Custom (Valve only)" | controller haptics |

## 4. GamepadUI "zoo" (`/zoo/*` routes) and Developer Options toggles

The zoo routes are `/zoo`, `/zoo/fieldlayouts`, `/dropdowns`, `/modals`, `/buttons`, `/sliders`, `/toggles`, `/clientsettings`, `/misc`, `/glyphs`, `/svg`, `/input`, `/developeroptions`, `/vrdeveloperoptions`, `/appspotlight`, `/playnext`, `/type`, `/soundtester`, `/weblinks`, `/interstitials`, `/desktopappshortcuts`, `/threedeetests`, `/grapheditor`, `/notifications` and `/share`. The zoo opens from Valve Internal > "Open Zoo". `/zoo/clientsettings` exercises the `setting_validation_*` client settings.

**Developer Options toggles** (store module `20816`). Each `SetToggle` writes sessionStorage `DEBUG_LibrarySettingsZoo_<label>`. In this build the loader skips reading those keys back (`const V=!0`), so the toggles do not survive a reload.

| Toggle | Description (from source) |
|---|---|
| Simulate VR UI on Desktop | VR UI instance will be created, using desktop popups instead of VR overlays. |
| VR Dashboard Bar has Many Tabs | Adds many tabs to the VR Dashboard Bar to test layout overflow. |
| "Sticky" VR Dashboard Bar Popups | Dashboard Bar Popups will remain open to facilitate debugging and styling. |
| "Sticky" Hovers | Hovers will remain open (sessionStorage `DEBUG_StickyHovers`). |
| Sticky Context Menus | Context menus will remain open (sessionStorage `DEBUG_StickyContextMenus`). |
| Sticky Keyboard | Keyboard will remain open on focus lost (sessionStorage `DEBUG_StickyKeyboard`). |
| Force Popup Context Menus | All context menus will be created as popups rather than DOM elements (sessionStorage `DEBUG_ForcePopupContextMenus`). |
| Apps Have Tons of Friends | Duplicate friend entries for styling tests. |
| Force Show Header Items | Force show header items on GamepadUI. |
| Allow Repeat Apps / No Minimum / Slow Query / Break Images / Debug Spew / Force Empty / Ignore App History / Force Fresh Query / Ignore Unowned Limit | Friends-activity / content-hub server query debugging |
| Force Showing Owned DLC / Force Showing New Content Spotlight / Show Already Viewed Featured Events | App spotlight debugging |
| Don't Filter / Slow Query (Play Next) | Play Next query debugging |
| Mark all notifications read | Notifications debugging |
| Force RTL | Force `dir=rtl` (sessionStorage `bForceRTL`, `SteamClient._internal.SetRightToLeftMode`). |

Desktop-side zoo ("Settings Zoo", "Library Settings Zoo") items include "Log all CM Traffic" (localStorage `DEBUG_LogCMTraffic`: "All messages to and from the steam servers will be logged to the browser console (F12)"), a context-menu option backed by localStorage `EnableContextMenuBlurDelay3`, and "React Query Devtools" (localStorage `ReactQueryDevtoolsVisible`).

## 5. Hidden steam:// URLs and internal SteamClient API

| Item | Effect |
|---|---|
| `steam://devmode/enable`, `steam://devmode/disable` | Sets `Config.DEV_MODE` and calls `SteamClient._internal.SetDevMode` |
| `steam://webhelper/disablegpu` | `SteamClient._internal.RequestDisableGpu()` (restarts the web helper without GPU, inferred) |
| `steam://open/console`, `steam://nav/console` | Steam console (only when the console is enabled) |
| `steam://open/systemreport`, `steam://open/runtimeinfo`, `steam://open/systeminfo` | Diagnostics dialogs |
| `SteamClient._internal.*` | `SetDevMode`, `RequestDisableGpu`, `IsDebuggingEnabled`, `GetBrowserProcessDetails` (process list; refreshed on `browser_process_details_changed`), `SetRightToLeftMode` |
| `SteamClient.Console.ExecCommand(cmd)`, `GetAutocompleteSuggestions`, `RegisterForSpewOutput` | Used only by the Console page. Commands are typed by the user; the UI hard-codes none. |

## 6. Debug globals exposed on `window` (callable from the CEF devtools console)

| Global | Purpose |
|---|---|
| `EnableSteamConsole(bEnable=true)` | Enables the "SteamClient" debug log |
| `DebugLogEnable(...)`, `DebugLogDisable(...)`, `DebugLogEnableAll()`, `DebugLogDisableAll()`, `DebugLogEnableBacktrace()`, `DebugLogDisableBacktrace()`, `DebugLogNames()`, `DebugLogEnabled()` | Web log channel control (saved in localStorage `EnabledWebLogs` etc.) |
| `SetVoiceEchoLocalMic`, `SetVoiceLogDetails`, `SetVoiceForceReconnectingStatus`, `SetVoiceForceConnectingStatus`, `SetVoiceAutoShowVideoStream` | Voice chat debugging |
| `SetHoverPresentation(mode)` | Game hover style (sessionStorage `DEBUG_UseNewGameHover`, default "default") |
| `DEBUG_SuppressWindowType(type, bSuppress)`, `DEBUG_GetDesiredSteamUIWindows()` | Suppress Steam UI window types (sessionStorage `debug_suppressed_window_types`; `"VR"` is shorthand for both VR gamepad windows) |
| `protoPathPropertyDebug` (bool) | When true, records VR path property values for debugging |
| `toJS`, `jsonit` | MobX / JSON helpers |
| `ResetNewContentRollup`, `ShowVROverlay`, `fnLoyalty_ShowAwardModal` | Misc test hooks |
| `g_EventCalendarDevFeatures` | Event calendar dev overrides (`?t=` time override parsed by `ParseDevOverrides`) |
| Store singletons | `settingsStore`, `appStore`, `appDetailsStore`, `appInfoStore`, `collectionStore`, `downloadsStore`, `friendStore`, `uiStore`, `SteamUIStore`, `NotificationStore`, `overlayStore`, `securitystore`, `loginStore`, `consoleStore`, `SystemPerfStore`, `SystemNetworkStore`, `SystemDisplayManagerStore`, `SystemAudioDevicesStore`, `SystemDevkitStore`, `SystemPowerStore`, `SystemDockStore`, `SystemReportStore`, `SystemStoragStore` [sic], `SuspendResumeStore`, `UpdateStore`, `RemotePlayStore_SteamUI`, `streamingStore`, `ControllerStore`, `controllerConfiguratorStore`, `installFolderStore`, `screenshotStore`, `serverBrowserStore`, `settingsZooStore`, `vrFrameStore`, `vrGamepadInput`, `vrPooledPopupStore`, `vrAudioSettingsStore`, `VRPathProperties`, `protoPathProperties`, `MainWindowBrowserManager`, `FocusNavController`, `FocusedAppWindowStore`, `BrowserAndBackstackInstances`, `LocalizationManager`, `g_PopupManager`, `g_LogManager`, `g_FriendsUIApp`, `g_GRS`, `g_SubscriptionStore`, `g_WindowFocusCoordinator`, `cm` (CM interface), `cloudStorage`, `cloudStorageInternalState` and others (about 100 assignments in total) |

## 7. Feature flags, experiments and A/B testing

- No generic feature-flag or experiment framework is visible in the UI bundle. The only experiment-like hooks are:
  - `SendExperimentEventToSteam` (event-calendar view telemetry);
  - `ExperimentService` (protobuf service name);
  - `EDiscoveryQueueExperimentalCohort` / `experimental_cohort` (discovery queue);
  - `SpecifyCompatExperiment` / `strCompatExperiment` (per-app Proton experiment selection; see steamclient-api-config.md).
- Family View features: settings controls carry a `feature:` prop. It refers to the parental-control features (`ParentalSettings.enabled_features` / `temporary_enabled_features`), not to rollout flags.
- `SteamClient.FriendSettings.GetEnabledFeatures()` returns the friends UI `featuresEnabled` map.
- Config switches that act like flags are `USE_LONGEST_LOC_STRING` (loads the "longest string" pseudo-localization for layout testing), `FORCED_DISPLAY_MODE` (`steamdeck` / `steammachine`), `SILENT_STARTUP`, `CLOUD_GAMING_PLATFORM` and `TESLA`. See injected-config.md.
