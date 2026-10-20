# steamui: persistence keys (localStorage, sessionStorage, Steam storage APIs, cookies)

Source: all `root/steamui/*.js` chunks, Linux client manifest 1791918634. Found by:

- a script that matches calls to `localStorage.*` and `sessionStorage.*`;
- calls to `SteamClient.Storage.*`, `.MachineStorage.*`, `.RoamingStorage.*` and `.CloudStorage.*`;
- calls on the storage-wrapper classes (`GetObject`, `StoreObject`, `GetString`, `StoreString`, `RemoveObject`);
- the `useLocalStorage` hook (module `35035`, `(0,X.M)(key, default)`);
- the cookie helpers (`VY` = get cookie, `lc` = set cookie).

When a key was passed as a variable, the script followed it back to its string constant. Keys built at runtime are shown as patterns.

**IndexedDB:** no `indexedDB.open` or `createObjectStore` call exists in the steamui bundles. The UI does not use IndexedDB directly; Chromium's own caches aside.

## Storage back-ends

All wrappers derive from a base class (`library.js` module `33183`) that JSON-encodes objects on top of `GetString`/`StoreString`.

| Wrapper | Backed by | Scope |
|---|---|---|
| user local storage (`m_localStorage`, `new s.A`; module `33113`) | `SteamClient.Storage.GetString/SetString/DeleteKey` | Per user, local machine (client local config). It asserts if used before login. One variant falls back to browser `localStorage` and migrates the value. |
| machine storage (`m_machineStorage`, `m_MachineStorage`) | `SteamClient.MachineStorage.*` | Per machine, all users |
| roaming storage (`m_roamingStorage`) | `SteamClient.RoamingStorage.GetString/SetString/GetJSON/SetObject/DeleteKey` | Per user, synced to the cloud (asserts before login) |
| cloud config store (`m_cloudStorage`, `m_cloudStorageMap`) | `CCloudConfigStore` namespaces (server-synced key/value with versions) | Per user, synced |
| browser `localStorage` / `sessionStorage` | CEF profile of steamwebhelper | Per CEF profile (shared by all users of the install) |
| "cloud storage" JSON | `SteamClient.CloudStorage.WriteKey(key, json)` and HTTP GET `<CloudStorage.Root>/<key>.json`, with fallback to localStorage `U<accountid>-<key>` | Per user |

## Keys in the Steam storage wrappers

| Key | Back-end | Purpose (inferred from surrounding code) |
|---|---|---|
| `CachedCommunityPreferences` | user local | Cached community preferences (nickname display, chat text filter) |
| `CachedStorePreferences` | user local | Cached store preferences (content descriptors, review score preference, languages) |
| `CachedNotificationPreferences` | user local | Cached notification-type targets |
| `CachedBatteryPreferences` | user local | `{bShowBatteryPercentage}` |
| `UIStoreLocalSteamUIState` | user local | Persisted UI state of the Steam UI store |
| `user-collections` | user local | Library collections (local copy) |
| `collection-bootstrap-complete` | cloud config | Collections migrated to cloud |
| `sc-version` | cloud config | inferred: collections ("showcase/collection") schema version |
| `GameReleased` | cloud config | Seen game-release notices |
| `/steam/guidedtour` | cloud config | Guided tour state |
| `showcases` | roaming | Library home showcases |
| `CurrentKeyboardTheme`, `GetKeyboardSkins` | user local | On-screen keyboard theme and skins cache |
| `keyboard_layout` | user local + machine | On-screen keyboard layout |
| `keyboard_haptic_preset`, `keyboard_haptic_custom` | user local | On-screen keyboard haptics |
| `keyboard_initial_location_desktop`, `keyboard_initial_location_overlay` | user local | Keyboard position |
| `keyboard_trackpad_typing_scale`, `keyboard_trackpding_typing_trigger_as_click` [sic] | user local | Trackpad typing |
| `deck_compatibility_feedback_ask`, `deck_compatibility_feedback_eligible_apps`, `deck_compatibility_feedback_user_responded` (deprecated, removed) | user local | Steam Deck compatibility feedback prompts |
| `GetEquippedProfileItemsForUser`, `GetStartupMovies` | user local | Cached community-item responses (startup movies, profile items) |
| `spotlight_dlc_store`, `spotlight_gameplaysession_store` | user local | App spotlight state |
| `emoji_storage`, `playnextstore_storage` | user local (`m_LocalStorage`) | Recent emoji; Play Next cache |
| `DownloadsStoreRecentlyCompleted` | machine | Recently completed downloads list |
| `LockScreenSettings` | machine | Lock screen (PIN) settings (SteamOS) |
| `continuously_render_store` | machine | Valve Internal "Continuously Render Frames" |
| `AllowInternalDisplayScaling` | display-scaling dev settings store | Valve Internal "Show advanced display scaling settings for internal display" |
| `Deck_GuidedTourVersionSeen`, `Deck_SeasonalSale`, `tour_history`, `timeline_intro`, `whatsnew_lastseen`, `wishlist_recent_categories`, `gamepadui_last_library_tab_and_collection`, `deck_desktopapp_intro_seen`, `ea_dialog_seen`, `seen_clip_saved_hint`, `updatedNowHint`, `LaunchOptionTipsShown`, `TimesSeenLocalPlayCallout`, `TimesSeenStatusChangeCallout`, `TimesSeenStreamingCallout` | wrapper (user local unless noted; back-end not traced for each) | "Seen" / onboarding / last-tab state |
| `` `LocalizedTagNames2_${language}` `` | wrapper | Localized store tag-name cache |
| `APPINFO_<appid>` | app info cache storage | Cached app info |
| `BrowserBookmarks_<appid>` | overlay storage | Overlay web-browser bookmarks per game |
| `SortedAchievements_<appid>` | wrapper | User's achievement sort order |
| `OverlaySavedDataV2_<appid>_<kind>` | wrapper | Per-game overlay saved data, versioned |
| `CCMList_<EUNIVERSE>` | `library.js` CM-list storage | Cached Connection Manager server list |
| `PopupSavedDimensions_<accountid>` | wrapper | Saved popup window sizes and positions |
| `DownloadListSection_<section>` | wrapper | Collapsed state of download-list sections |
| `spotlight.review.<appid>`, `library.review.<appid>` | roaming / wrapper | Review-prompt dismissal state |
| `<prefix>_<accountid>` (for example `CTextFilterStore_TextFilterPreferences_<accountid>`) | wrapper | Chat text-filter preferences |
| `InflightMessageQueue_<id>` | wrapper | Pending chat messages (friends UI) |
| `friendstore_playercache`, `FriendLastMessageCache`, `RecentChats.HiddenItems`, prefix `LocalStorageFriendsSettings` | friends UI storage | Friends/chat caches |
| `oFriendsUIStartupParam` | sessionStorage | Friends UI startup parameter hand-off |

## Browser localStorage keys

| Key | Purpose |
|---|---|
| `EnabledWebLogs`, `IncludeBacktraceInLog`, `AllowCSSInLogColors` | Web debug-log channel settings (Valve Internal > Log Settings; `window.DebugLog*`) |
| `DEBUG_LogCMTraffic` | Log all CM traffic to the devtools console |
| `ReactQueryDevtoolsVisible` | Show React Query devtools |
| `Internal_ForceBetaSectionVisible` | Valve Internal "Force Beta Section Visible" |
| `Internal_RemainInBigPictureModeOnClose` | Valve Internal "Remain in Big Picture Mode on Window Close" |
| `GamepadPage_MaxWidthEnabled_2`, `GamepadPage_MaxWidth` | Valve Internal "Constrain GamepadPage width" |
| `DebugPointer_Enabled`, `DebugPointer_Size`, `DebugPointer_Opacity_Hovering`, `DebugPointer_Opacity_NotHovering` | Valve Internal debug pointer |
| `GamepadUI_KeyboardNavGlyphsDisabled` | Developer > Steam Input > "Keyboard Glyphs" (inverted) |
| `EnableContextMenuBlurDelay3` | Context menu blur-delay debug option |
| `AppGridDisplaySettings` | `{eSortBy}` library grid sort |
| `GameListWidthPercentage` | Desktop library left-column width |
| `Login_RememberMeSetting` | Login "Remember me" checkbox ("0" = off) |
| `bShowLoginQR` | Show the QR-code login ("1") |
| `broadcastSettings` | Broadcast viewer settings `{nVolume, bMuted, ulViewerToken}` |
| `gameRecordingPlayer` | Recording player settings |
| `contenthub_reducemotion` | Content hub reduce-motion flag |
| `unUserdataVersion` | Version appended to the `dynamicstore/userdata` request (`&v=`) |
| `EventsHiddenLocally_*`, `EventsLastFetch_*` | Library events hidden / last fetch |
| `` `OverlayPopupURL${a}_${b}` `` | Last URL of an overlay popup |
| `valve.steam.gamepadui.bar`, `valve.steam.gamepadui.mainmenu` | Gamepad UI window-name keys (saved popup state) |
| `screenshot_defaultprivacy` | Default screenshot upload privacy (useLocalStorage hook) |
| `U<accountid>-<key>` | Fallback for CloudStorage JSON keys |

## Browser sessionStorage keys

| Key | Purpose |
|---|---|
| `steam-dev-configparams` | Stores `location.search` of `index.html`/`sp.html` so that config overrides survive in-app navigation (see injected-config.md) |
| `token_use_id` | Prevents reusing a consumed in-page login token |
| `CSettingsDialogLastPageOpened` | Last settings page opened |
| `startup-movie-played` | Startup movie already played this session |
| `focus-popup-on-show` | Popup focus behavior bookkeeping |
| `focus-nav-show-debug-focus-ring` | "Show Debug Focus Ring" (`"shown"`) |
| `DEBUG_StickyContextMenus`, `DEBUG_StickyKeyboard`, `DEBUG_ForcePopupContextMenus`, `DEBUG_StickyHovers` | Zoo developer toggles |
| `DEBUG_UseNewGameHover` | `window.SetHoverPresentation` |
| `DEBUG_LibrarySettingsZoo_<label>` | Zoo developer-option toggles (written but not reloaded in this build) |
| `bForceRTL` | Force right-to-left layout |
| `debug_suppressed_window_types` | `DEBUG_SuppressWindowType` list |
| `steamdeckcompatibility` | Last Steam Deck compatibility tab (`?tab=<key>`) |
| `oFriendsUIStartupParam` | Friends UI startup parameter |

## Cookies read or written by the UI

Cookie registry (name, then necessity):

| Cookie | Necessity |
|---|---|
| `sessionid` | technically necessary |
| `steamLoginSecure` | technically necessary (httpOnly) |
| `steamLoginSpoofSteamID` | technically necessary |
| `Steam_Language` | technically necessary |
| `cookieSettings` | technically necessary |
| `clientHints` | technically necessary |
| `shoppingCartGID` | technically necessary |
| `steamDidLoginRefresh` | technically necessary |
| `webTradeEligibility` | technically necessary |
| `trailerPrefs` | technically necessary |
| `strResponsiveViewPrefs` | technically necessary |
| `personalcalendarPrefs` | technically necessary |
| `browserid` | optional |
| `app_impressions` | optional (product-impressions analytics) |

Cookies read directly:

| Cookie | Effect |
|---|---|
| `steamLoginSpoofSteamID` | A numeric value is sent as `spoof_steamid` on WebAPI service calls. This is an internal impersonation and debug feature; the server enforces permissions. |
| `presentation_mode` | `1` disables `UserConfig.is_support` |
| `forceallages` | Any non-`0` value forces all-ages media masking |
| `wants_mature_content` | Mature content preference |
| `bDisableAOWarning` | Adults-only warning suppression (expiry timestamp, 2 days) |

## Resource overrides (`/uioverrides`)

Module `9581` (`useOverrideableResource`) sends `HEAD /uioverrides<path>` before it uses a built-in resource. If that request succeeds, the override URL is used instead. In this build it applies to:

- the platform startup movie: `/movies/deck_startup.webm`, `/movies/oled_startup.webm`, `/movies/steam_os_startup.webm`, `/movies/startup_machine.webm`, `/movies/bigpicture_startup.webm` and others;
- the suspend animations: `/movies/*-suspend-animation*.webm`, `/movies/steam_os_suspend*.webm`.

Inferred: a file placed at `steamui/uioverrides/movies/<name>.webm` in the client install would replace the default animation.
