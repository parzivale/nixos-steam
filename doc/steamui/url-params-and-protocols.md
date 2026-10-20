# steamui: URL / query parameters and steam:// protocol handling

Source: `root/steamui/index.html`, `library.js` (bootstrap) and `sp.js`, Linux client manifest 1791918634. Found by:

- grepping for `location.search`, `URLSearchParams`, the query-param hooks (`f3`/`Bm` in module `4190`) and `[?&]name=` regexes;
- extracting the steam:// navigation handler table (`NavHandlers`, module `92819`) and every `RegisterForRunSteamURL(...)` call;
- collecting every literal `steam://...` string the UI emits;
- reading the react-router route table (module `80344`).

## 1. Startup query parameters of the SharedJSContext page (`index.html` / `sp.html`)

The client loads `steamui/index.html` (title `SharedJSContext`), which pulls in `library.js` and `sp.js`. On start, `library.js` module `2804` does the following:

1. If the page path contains `index.html` or `sp.html`, it saves `window.location.search` into sessionStorage `steam-dev-configparams` ("Storing new config params"). Otherwise it reloads the saved string ("Loading previous config params").
2. It parses the string with `qs.parse`. **Every key whose name matches a property of `Config` (`TS`), `UserConfig` (`iA`) or the steamui-only config object (`SHOW_CONSOLE`, `CLOUD_GAMING_PLATFORM`) is assigned.** Values are coerced: `"true"` becomes true, `"false"` becomes false, numeric strings become numbers, anything else stays a string. Unknown keys are logged as "Got unknown config property".
3. Afterwards it fixes up a few values: if `EREALM` is unknown it is derived from `LAUNCHER_TYPE` (China or Global), `UserConfig.country_code` defaults to `COUNTRY`, and `Config.IN_STEAMUI` is forced to true.

So the client injects its configuration as URL query parameters. The full key list (EUNIVERSE, LANGUAGE, IS_STEAMOS, IN_GAMESCOPE, DEV_MODE, ...) is in **injected-config.md**. A developer can append, for example, `?DEV_MODE=true&USE_LONGEST_LOC_STRING=true` to the page URL.

Other query parameters read directly:

| Parameter | Where | Effect |
|---|---|---|
| `PACKAGE_CL` | `URLSearchParams(window.location.search).get("PACKAGE_CL")` | Client package changelist, used as the display version in usage/crash reporting ("Shared SteamUI", "Client Login") |
| `force_client_view`, `force_tenfoot_client_view`, `force_overlay_view`, `force_mac_view`, `force_ios_view`, `force_android_view` | `library.js` module `22545`: `location.href.match("[?&]<name>=")` | Override user-agent based detection (in Steam client, Tenfoot/Big Picture, game overlay, Mac, iOS, Android) |
| `need_password` | login refresh / `jwt/finalizelogin` | Forces the password prompt; removed from `redir` |
| `tab` | settings, library and app-detail pages (query-param hook `f3`/`Bm`) | Selected tab |
| `t` | Event calendar `ParseDevOverrides` (`g_EventCalendarDevFeatures`) | Dev time override (only `has("t")` is checked in this build) |
| `fromsettings=1` | Appended to the FamilyManagement URL when opened from Settings | — |
| `low_bandwidth=1`, `dlc_appid_overrides=[...]` | Marketing message URLs (`marketingmessages/<id>`, `/preview/<id>`) | Low-bandwidth rendering; preview DLC override |
| `snr`, `curator_clanid` | Added to store links (`AddNavParamToURL`) | Navigation tracking |
| `l=<language>`, `cc=<country>` | Store/community AJAX requests (`dynamicstore/userdata/?id=..&cc=..&origin=..&v=<unUserdataVersion>`) | Language / country |
| `access_token`, `spoof_steamid`, `origin`, `input_json`, `input_protobuf_encoded` | WebAPI service calls | `spoof_steamid` comes from cookie `steamLoginSpoofSteamID` |

## 2. Steam URL parsing

`steam://` URLs reach the UI through `SteamClient.URL.RegisterForRunSteamURL` and the internal `RegisterForRunSteamURL(uiMode(s), name, cb)` dispatcher. The parser (`zK`):

- accepts the protocols `steam:`, `steambeta:`, `steamchina:` and `steamchinabeta:`;
- splits the rest into `rgParts` (path segments after the handler name) and `params` (from `?a=b`).

Registrations are made per UI mode (EUIMode enum from `library.js`: -1 Unknown, 0 VGUI, 1 Tenfoot, 2 Mobile, 3 Web, 4 GamepadUI, 7 Desktop). A handler only runs in the modes it is registered for.

Two flags appear on handlers:

- `bRequiresLargeMode`: the handler needs the full desktop or Big Picture main window, not the small-mode library.
- `bForceOpenInMainInstance`: the handler opens in the main window instance.

### 2a. Main navigation handler table (`NavHandlers`)

| steam:// URL | UI modes | Flags |
|---|---|---|
| `steam://url` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://helpurl` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://openurl` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://openurl_external` | Desktop/GamepadUI |  |
| `steam://openurlforpid` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://openexternalforpid` | Desktop |  |
| `steam://openexternalforpid` | GamepadUI |  |
| `steam://open/apprunningcontrols` | GamepadUI |  |
| `steam://publisher` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://open/storefront` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://open/defaultdialog/maininstance` | Desktop/GamepadUI | bForceOpenInMainInstance:true |
| `steam://open/defaultdialog` | Desktop/GamepadUI |  |
| `steam://store`, `steam://purchase`, `steam://advertise`, `steam://store_demo` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://storeurl` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://broadcast/watch` | Desktop/GamepadUI |  |
| `steam://video/watch` | Desktop |  |
| `steam://appnews`, `steam://updatenews` | Desktop | bRequiresLargeMode:true |
| `steam://open/library`, `steam://open/games`, `steam://nav/games` | Desktop/GamepadUI/VGUI |  |
| `steam://open/downloads`, `steam://nav/downloads` | Desktop/GamepadUI/VGUI | bRequiresLargeMode:true |
| `steam://open/minigameslist` | Desktop |  |
| `steam://open/largegameslist` | Desktop | bRequiresLargeMode:true |
| `steam://open/largegameslist` | GamepadUI |  |
| `steam://cdkeys` | Desktop/GamepadUI |  |
| `steam://open/friends` | GamepadUI |  |
| `steam://open/console`, `steam://nav/console` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://open/screenshots` | GamepadUI |  |
| `steam://settings`, `steam://open/settings` | GamepadUI |  |
| `steam://settings`, `steam://open/settings` | Desktop | bForceOpenInMainInstance:true |
| `steam://currentcontrollerconfig` | Desktop/GamepadUI |  |
| `steam://viewfriendsgame` | Desktop/GamepadUI |  |
| `steam://joinfriendsgame` | Desktop/GamepadUI |  |
| `steam://ClientBeta` | Desktop |  |
| `steam://ClientBeta` | GamepadUI |  |
| `steam://open/activateproduct` | Desktop |  |
| `steam://backup` | Desktop |  |
| `steam://validate` | Desktop |  |
| `steam://open/tools`, `steam://nav/tools` | Desktop/GamepadUI |  |
| `steam://open/restoredialog` | Desktop |  |
| `steam://exit` | Desktop/GamepadUI |  |
| `steam://friends/add` | Desktop/GamepadUI |  |
| `steam://friends/status/online` | Desktop/GamepadUI |  |
| `steam://friends/status/away` | Desktop/GamepadUI |  |
| `steam://friends/status/invisible` | Desktop/GamepadUI |  |
| `steam://friends/status/offline` | Desktop/GamepadUI |  |
| `steam://friends/ShowChatRoomGroupInvite` | Desktop/GamepadUI |  |
| `steam://itemstore` | Desktop/GamepadUI |  |
| `steam://itemstoredetail` | Desktop/GamepadUI |  |
| `steam://guestpasses` | Desktop/GamepadUI |  |
| `steam://connect` | Desktop |  |
| `steam://open/bigpicture/storefront` | Desktop/GamepadUI | bRequiresLargeMode:true |
| `steam://open/bigpicture/store` | Desktop/GamepadUI |  |
| `steam://open/bigpicture/games` | Desktop/GamepadUI |  |
| `steam://open/bigpicture/librarydetails` | Desktop/GamepadUI |  |
| `steam://open/bigpicture/workshopitem` | Desktop/GamepadUI |  |
| `steam://open/bigpicture` | Desktop/GamepadUI |  |
| `steam://devmode` | Desktop/GamepadUI |  |
| `steam://webhelper/disablegpu` | Desktop/GamepadUI |  |
| `steam://changeuser` | Desktop/GamepadUI |  |
| `steam://signout` | Desktop/GamepadUI |  |

Handler details worth noting:

- `steam://settings/<page>`: `<page>` is looked up in the settings slug map. Slugs: network, audio, controller, display, power, downloads, DiskManagement, storage, family, account, SteamPlay, system, security, notifications, bluetooth, keyboard, customization, friends, cloud, home, library, ingame, compatibility, interface, music, broadcast, developer, internal, voice, gamerecording (desktop alias `gr`), accessibility, store. Unknown slugs fall back to "System" in GamepadUI and "Account" on desktop.
- `steam://devmode/enable|disable`: sets `Config.DEV_MODE` and calls `SteamClient._internal.SetDevMode` (hidden).
- `steam://webhelper/disablegpu`: `SteamClient._internal.RequestDisableGpu()` (hidden).
- `steam://connect/<ip[:port]>[/<password>]`: default port 27015; opens the server info dialog and connects.
- `steam://open/apprunningcontrols/<appid>`: opens the in-game overlay for the app.
- `steam://currentcontrollerconfig/<appid>`: opens the controller configurator.
- `steam://friends/status/online|away|invisible|offline` sets the persona state. `steam://friends/ShowChatRoomGroupInvite/<code>` and `steam://friends/add` are also handled.
- `steam://validate/<appid>`: verifies app files. `steam://backup` and `steam://open/restoredialog` open the backup and restore dialogs.
- `steam://ClientBeta/...`: client beta selection (handled separately on desktop and in GamepadUI).
- `steam://changeuser`, `steam://signout`, `steam://exit` (`SteamClient.User.StartShutdown`).

### 2b. Other `RegisterForRunSteamURL` registrations

| steam:// URL | Mode / registrar |
|---|---|
| `steam://open/friends` | Desktop (friends list popup) |
| `steam://open/musicplayer` | Desktop + GamepadUI (no-op placeholder on desktop) |
| `steam://open/systemreport` | Desktop + GamepadUI |
| `steam://open/about`, `steam://open/changeemail`, `steam://open/systeminfo` | Desktop dialogs |
| `steam://checkforupdates` | Desktop |
| `steam://open/addnonsteamgame` | Desktop |
| `steam://checkout_return/paypal_success`, `steam://checkout_return/paypal_cancel` | `SteamClient.URL.RegisterForRunSteamURL` (checkout popups) |
| Friends UI URLs | Forwarded with `RegisterForSteamURLs` from the friends UI. Names are supplied by friendsui at runtime (for example `friends/...`, `joinlobby`). |
| Dialog-specific `open/*` names, registered through a reusable dialog hook | `open/servers`, `open/screenshots`, `open/media`, `open/recording`, `open/clip`, `open/runtimeinfo`, `open/supportalert`, `open/settings` (string literals present; exact registration site inferred) |

### 2c. steam:// URLs emitted by the UI (links and buttons)

Paths are listed without the `steam://` prefix; a trailing `/` means an argument follows.

- **open/…**: open/friends, open/addnonsteamgame, open/servers, open/screenshots, open/screenshots/, open/library, open/library/, open/library/details/, open/library/view/home, open/library/view/tools, open/library/view/soundtracks, open/library/collection/hidden, open/library/shared-apps/, open/games, open/games/, open/goonline, open/systemreport, open/settings, open/settings/voice, open/settings/ingame, open/settings/friends, open/settings/audio, open/runtimeinfo, open/minigameslist, open/largegameslist, open/downloads, open/bigpicture, open/bigpicture/librarydetails/, open/workshop, open/systeminfo, open/supportalert, open/recording/, open/newforyou, open/media, open/inventory, open/console, open/changeemail, open/apprunningcontrols, open/about
- **settings/…**: settings, settings/account, settings/system, settings/interface, settings/ingame, settings/downloads, settings/broadcast
- **Running games**: rungame/, rungameid/, run/, run/250820 (SteamVR), install/, joinlobby/, joinparty/, connect/, gamewebcallback/, stopstreaming, remoteplay/connect, remoteplay/connect/
- **url/…**: url/StoreAddFundsPage, url/StoreAccount, url/SteamPreferences, url/SteamIDMyProfile, url/SteamIDFriendsPage, url/SteamIDEditPage, url/SteamIDBroadcastPage/, url/SteamAnnouncements, url/SSA, url/RedeemWalletVoucher, url/PrivacyPolicy, url/ManageGiftsPage, url/LegalInformation, url/HelpFrontPage, url/EventAnnouncementPage/593110/…, url/CommunityHome
- **Friends**: friends/status/online, friends/status/offline, friends/status/invisible, friends/status/away, friends/add, friends/players
- **Navigation**: nav/games/, nav/games/details/, store, store/, cdkeys/, controllerconfig/, broadcast/watch/, viewfriendsgame/, musicplayer/playappalbum/
- **Window control**: close, close/, close/bigpicture, close/cancel, close/authorize, exit
- **Other**: openurl, openurl/, openurl_external/, openexternalforpid/, checkout_return/paypal_success/, checkout_return/paypal_cancel/, checkforupdates

## 3. In-app routes (react-router, module `80344`)

These are not URL parameters, but they are the addressable pages of the Gamepad UI and the overlay. Route parameters are written `:name`.

- **Library**: `/library`, `/library/home`, `/library/app/:appid` (plus `/achievements`, `/achievements/my`, `/achievements/my/individual`, `/achievements/my/global`, `/achievements/friend/:accountid[/individual|/global]`), `/library/collection/:collectionid[/:appid]`, `/library/collections`, `/library/downloads`, `/library/tab/:id`, `/library/app/:appid/tab/:id`
- **App properties**: `/app/:appid/properties/{general,compatibility,updates,localfiles,language,betas,controller,shortcut,dlc,workshop,feedback,privacy,gamerecording,customization,performance}`
- **Overlay**: `/app/:appid/overlay/{achievements,controller,guides,notes,browser,gamerecording}`
- **Controller configurator**: `/app/:appid/controllerconfigurator/{main,summary,preview,sharedlayout,actionsets,actions,buttons,dpad,triggers,sticks,touchpads,gyroscopes,virtualmenus,choosebinding/…,modesettings/…,mouseposition/…,multibinding/…,chooseconfiguration[/community]}`, `/standalonecontrollerconfigurator`
- **Settings**: `/settings/{system,display,power,internet,notifications,bluetooth,audio,storage,security,internal,developer,controller/:type/:controllerIndex,keyboard,customization,friends,downloads,cloud,remoteplay,library,family,home,account,ingame,compatibility,interface,music,broadcast,voice,ingamevoice,desktopsecurity,gamerecording,accessibility,store}`
- **OOBE**: `/oobe`, `/oobe/current`, `/oobe/1[/language|/timezone|/network|/update|/screenreaderconfirm]`, `/oobe/2[/hardwareupdater|/pairsteamcontroller|/paircontroller|/underscan|/audiodevice|/audiochannels]`
- **Controller tools**: `/controller/bindinput/:controllerIdx`, `/controller/devicesupport/:controllerIdx`, `/controller/calibration/:controllerIdx/{General,LInputs,RInputs,Trackpads,Gyro,LeftGyro,GyroDemo,LeftGyroDemo,GripSensors,Sensors,Outputs,LEDs}`
- **Other pages**: `/routes`, `/init`, `/console`, `/media[/grid|/list|/item/:type/:id]`, `/browser/`, `/login`, `/createaccount`, `/account`, `/decksetup`, `/apprunning`, `/gameapiosk`, `/error`, `/colorsettings`, `/keyboard`, `/search[/tab/:id]`, `/steamweb`, `/externalweb`, `/microtxnauth`, `/about`, `/accessibility`, `/chat`, `/invites`, `/store`, `/workshop`
- **Developer zoo**: `/zoo` and its sub-pages (see hidden-dev-options.md)
