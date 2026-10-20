# steamui: injected configuration objects (Config, UserConfig, ...)

Source: `root/steamui/library.js`, which holds the shared web-platform modules `30610` (config objects), `76196` (config loader), `2804` (steamui bootstrap), `22545` (user-agent detection) and `77680` (steamui-only config). Also `sp.js`, for the readers of these objects and the URL store. Linux client manifest 1791918634.

The defaults below are the literal initial values in the bundle.

## How values get in

| Source | Applies to | Mechanism |
|---|---|---|
| **Query string of `steamui/index.html` / `sp.html`** | `Config`, `UserConfig`, steamui config | `library.js` module 2804 parses `location.search` with `qs.parse`. Any key whose name matches an existing property is assigned. Values are coerced: `"true"` and `"false"` become booleans, numeric strings become numbers, anything else stays a string. The string is cached in sessionStorage `steam-dev-configparams`. Unknown keys are logged as "Got unknown config property". This is how the C++ client hands its config to the SharedJSContext. |
| `data-*` attributes on the `#webui_config` element | `Config` (`data-config`), `UserConfig` (`data-userinfo`), `BroadcastConfig` (`data-broadcast`), `CommunityConfig` (`data-community`), `EventConfig` (`data-event`) | Same shared code as the Steam websites (`GetConfigJSON`). Not used by `index.html`, which has no such element. Relevant for web pages rendered with the same library. |
| `ajaxgetconfig` / `ajaxgetuserconfig` | `Config` / `UserConfig` | Optional fetch helper (web) |
| `SharedConnection` logon info (`OnLogonInfoChanged`) | `Config.EUNIVERSE`, `MEDIA_CDN_COMMUNITY_URL`, `COUNTRY`; `UserConfig.logged_in`, `steamid`, `accountid`, `account_name` | Fields `eUniverse`, `strCommunityImagesURL`, `strUserCountry`, `bLoggedOn`, `strSteamid`, `strPersonaName`, `strAccountName` |
| URL store (`SteamClient.URL.GetSteamURLList`) | `*_BASE_URL`, CDN URLs, `WEBAPI_BASE_URL` | Assigned from the client's named URL list (`GetStoreURL`, `GetCommunityURL`, `GetWebApiURL`, `GetHelpURL`, `ResolveURL("ChatRoot")`, ...) |
| `steam://devmode/enable\|disable` | `Config.DEV_MODE` | Also calls `SteamClient._internal.SetDevMode` |
| Bootstrap | `Config.IN_STEAMUI = true`; `EREALM` derived from `LAUNCHER_TYPE` when unknown; `UserConfig.country_code` defaults to `COUNTRY` | |

## `Config` (export `TS`)

| Key | Default | Meaning (inferred unless obvious) |
|---|---|---|
| `EUNIVERSE` | 0 | Steam universe (1 = Public) |
| `LANGUAGE` | "english" | UI language |
| `SUPPORTED_LANGUAGES` | [] | Supported language list |
| `COUNTRY` | "" | User country code |
| `AVATAR_BASE_URL` | "" | Avatar CDN |
| `MEDIA_CDN_COMMUNITY_URL` | "" | Community media CDN (set from logon info) |
| `MEDIA_CDN_URL` | "" | Media CDN |
| `CLAN_CDN_ASSET_URL` | "" | Clan asset CDN |
| `COMMUNITY_ASSETS_BASE_URL` | "" | `${BASE_URL_SHARED_CDN}community_assets/` |
| `VIDEO_CDN_URL` | "" | Video CDN |
| `COMMUNITY_CDN_URL` | "" | Community CDN |
| `COMMUNITY_CDN_ASSET_URL` | "" | Community CDN assets |
| `BASE_URL_SHARED_CDN` | "" | Shared CDN |
| `STORE_CDN_URL` | "" | Store CDN |
| `PUBLIC_SHARED_URL` | "" | Public shared assets |
| `COMMUNITY_BASE_URL` | "" | steamcommunity.com base |
| `CHAT_BASE_URL` | "" | Chat base (`ResolveURL("ChatRoot")`) |
| `STORE_BASE_URL` | "" | store.steampowered.com base |
| `STORE_CHECKOUT_BASE_URL` | "" | Checkout base |
| `LOGIN_BASE_URL` | "" | login.steampowered.com base (`jwt/finalizelogin`) |
| `SUPPORT_BASE_URL` | "" | Support site |
| `STORE_ICON_BASE_URL` | "" | Store icons |
| `STORE_ITEM_BASE_URL` | "" | `${BASE_URL_SHARED_CDN}store_item_assets/` |
| `IMG_URL` | "" | Image base |
| `STEAMTV_BASE_URL` | "" | steam.tv |
| `HELP_BASE_URL` | "" | help.steampowered.com |
| `PARTNER_BASE_URL` | "" | partner site |
| `STATS_BASE_URL` | "" | stats site |
| `INTERNAL_STATS_BASE_URL` | "" | internal stats site |
| `BASE_URL_STORE_CDN_ASSETS` | "" | `${MEDIA_CDN_URL}store/` |
| `IN_CLIENT` | false | Running inside the Steam client |
| `USE_POPUPS` | false | Use popup windows |
| `IN_MOBILE` | false | Mobile app |
| `IN_MOBILE_WEBVIEW` | false | Mobile webview (affects `forceallages` handling on Android) |
| `IN_TENFOOT` | false | Tenfoot (legacy Big Picture) |
| `PLATFORM` | "" | `windows` / `macos` / `linux` (helpers `Y()`, `_()`, `$()`) |
| `ARCH` | "" | CPU arch (`arm64` checked) |
| `SNR` | "" | Store navigation tracking string |
| `LAUNCHER_TYPE` | 0 | Launcher type (China launcher sets the realm) |
| `EREALM` | 0 | Steam realm (Unknown, Global, China). China switches the protocol prefix to `steamchina:` |
| `IN_CHROMEOS` | false | ChromeOS build |
| `TESLA` | false | Tesla in-car build (inferred) |
| `LOCAL_HOSTNAME` | "" | Local hostname |
| `PACKAGE_CL` | "" | Package changelist (also read directly from the query string) |
| `WEBAPI_BASE_URL` | "" | api.steampowered.com base |
| `TOKEN_URL` | "" | Token endpoint |
| `BUILD_TIMESTAMP` | 0 | Build timestamp |
| `PAGE_TIMESTAMP` | 0 | Page generation timestamp |
| `FROM_WEB` | false | Page served from the web |
| `WEBSITE_ID` | "Unknown" | Website identifier (`steamui` returned by `yK()`) |
| `IN_STEAMUI` | false (forced to true by bootstrap) | Running in steamui SharedJSContext |
| `FORCED_DISPLAY_MODE` | undefined | `"steamdeck"` or `"steammachine"` forces device-specific UI (`G()`, `ae()`). Combined with `IS_STEAMOS` it selects Deck-style settings. |
| `ON_FRAME` | false | Running on Steam Frame (VR headset) hardware (inferred; gates many audio and display options) |
| `IS_STEAMOS` | false | Running on SteamOS (gates SteamOS-only settings, the Devkit section and others) |
| `ON_STEAMOS_CLIENT_BRANCH` | false | SteamOS client branch |
| `IN_GAMESCOPE` | false | Running under the gamescope compositor |
| `USE_LONGEST_LOC_STRING` | false | Load the pseudo-localization that picks the longest translation of each string (layout testing) |
| `SILENT_STARTUP` | false | Start silently (the JS sets it back to false) |
| `DEV_MODE` | false | Developer mode (see hidden-dev-options.md) |
| `CLIENT_SESSION` | 0 | Client session id |
| `NOW` | 0 | Server time snapshot |

## `UserConfig` (export `iA`)

| Key | Default | Notes |
|---|---|---|
| `logged_in` | false | |
| `steamid` | "" | |
| `accountid` | 0 | |
| `account_name` | "" | |
| `token` | undefined | In-page login token |
| `token_use_id` | undefined | Single-use id, remembered in sessionStorage `token_use_id` |
| `webapi_token` | "" | |
| `authwgtoken` | "" | |
| `is_support` | false | Forced false when cookie `presentation_mode=1` |
| `is_limited` | false | Limited account |
| `is_partner_member` | false | |
| `is_valve_email` | false | |
| `short_url` | "" | |
| `country_code` | "" | Defaults to `Config.COUNTRY` |
| `excluded_content_descriptors` | [3 descriptor ids] | Mirrors the store content-descriptor preferences |

## steamui-only config (module `77680`, also settable through the query string)

| Key | Default | Meaning |
|---|---|---|
| `SHOW_CONSOLE` | "" | Truthy value enables the Steam Console |
| `CLOUD_GAMING_PLATFORM` | 0 | Non-zero means running on a cloud gaming platform (`r()` helper). Values 0, 1 and 2 are defined; names are not visible. |

## Other web-config objects defined in the same module (used by the shared web code)

- `BroadcastConfig` (`GP`): `steamid`, `clanid`, `listid`.
- `CommunityConfig` (`UF`): `CLANSTEAMID`, `CLANACCOUNTID`, `APPID`, `VANITY_ID`, `IS_CREATOR_HOME`, `IS_CURATOR`, `IS_OGG`, `CAN_UPLOAD_IMAGES`, `IS_VALVE_GROUP`, `IS_ALLOWED_SC`.
- `EventConfig`: `ANNOUNCEMENT_GID`, `TAKEOVER_ANNOUNCEMENT_GID`.

## Per-window `ConfigContext` (React context, `library.js` export `ss`/`rP`)

| Key | How it is determined |
|---|---|
| `IN_GAMEPADUI` | Explicit prop. Otherwise the user agent family starts with "Gamepad" (UA `Valve Steam Gamepad[ VR][/Steam Deck] [betaid]/<launcher>/<version>`). |
| `IN_DESKTOPUI` | Explicit prop |
| `IN_VR` | Explicit prop. Otherwise the UA family starts with "Gamepad VR". |

It is also attached to each popup window as `window.ConfigContext`. The UA regex also extracts the client beta name (`Steam Main Client`, `Steam Beta Update`, `Steam Deck Beta`, `Steam Deck Main`), the launcher and the version.

## Named URLs (`URLStore.ResolveURL(name)`, from `SteamClient.URL.GetSteamURLList`)

The UI resolves 67 named URLs:

AppNewsPage, AvatarBaseURL, BaseURLSharedCDN, ChatRoot, ClaimEntitlements, ClanAssetCDN, CommunityAddFriends, CommunityCDN, CommunityFilePage, CommunityFrontPage, CommunityImages, CommunityMarketSearch, CommunityRecommendations, EventAnnouncementPage, FamilyManagement, FamilySharing, GameHubDiscussions, GameHubGuides, GameHubNews, GlobalLeaderboardsPage, HelpAppPage, HelpChangeEmail, HelpChangePassword, HelpFAQ, HelpFrontPage, HelpVacBans, ItemStoreDetailPage, ItemStorePage, JoinTrade, LibraryAppDetails, ManageGiftsPage, ManageSteamGuard, OfficialGameGroupPage, ParentalBlocked, PendingGift, PointsShop, RecommendGame, SteamClientBetaBugReports, SteamIDAppTradingCardsPage, SteamIDBadgeInfo, SteamIDBroadcastPage, SteamIDEditPrivacyPage, SteamIDMyProfile, SteamIDPage, SteamPreferences, SteamVRHMDHelp, SteamWorkshopPage, StoreAccount, StoreAddFundsPage, StoreAppHover, StoreAppImages, StoreAppPage, StoreAppPageAddToCart, StoreCDN, StoreDlcPage, StoreFrontPage, StoreGameSearchPage, StoreGreatOnDeck, StoreGreatOnFrame, StorePublisherPage, StoreVR, UserAchievementsPage, UserLeaderboardsPage, UserStatsPage, VideoCDN, WatchVideo, WebAPI.

The same names work in `steam://url/<Name>` links.
