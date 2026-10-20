# Console commands (ConCommands)

> **What it does** is written from how the option is used in the code (strings and log messages near each
> read site, related options, Valve help). The confidence tag *(high/medium/low)* follows each inferred description.
> Untagged descriptions restate Valve's own help text.
>
> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

Every console command registered in the client binaries (name and help text). Run them in the Steam
console (`steam://open/console`).

Total: **133**.

| Command | What it does | Valve help text | Binaries |
|---|---|---|---|
| `achievement_clear` | Developer console: clear one achievement for the current user, probably `achievement_clear <appid> <achievement_api_name>`. The argument format is not in the help; `reset_all_stats` is the 'clear everything' variant. *(medium)* | Clears an achievement | steamui.so |
| `app_backup` | Console: `app_backup <appId> <target folder> [max folder size MB]` writes a Steam backup of an installed app to a folder, split into files of the given size. | <appId> <target folder> [max folder size MB] | steamui.so |
| `app_change_compat_tool` | Console: `app_change_compat_tool <appid> <name> [config=]` sets the Steam Play compatibility tool (e.g. a Proton version's internal name) for an app, with an optional tool config string. | <appid> <name> [config=] | steamui.so |
| `app_delay_update` | Console: `app_delay_update <appid> <seconds>` holds back an app's pending update for the given number of seconds. | <appid> <seconds> force delay update | steamclient.so |
| `app_dlc_status` | Console: `app_dlc_status <appId> <dlcId>` prints the install/ownership status of one DLC of an app. | app_status <appId> <dlcId> | steamclient.so |
| `app_download_enable` | Console: `app_download_enable <0\|1>` turns content downloads off or on globally. *(medium)* | <0\|1> | steamui.so |
| `app_info_find` | Console: `app_info_find <path> <value>` lists apps whose appinfo has the key set to the value, e.g. `app_info_find common/type media`; `*` matches any value. | Find apps with a certain appinfo value set, eg 'common/type media'. * is any.  | steamclient.so |
| `app_info_print` | Console: `app_info_print <appid> [section]` dumps the cached appinfo (PICS) KeyValues of an app, optionally only one section such as `config` or `depots`. | app_info_print <appid> [section] : print app info for appID | steamui.so |
| `app_info_update` | Console: `app_info_update [0\|1]` refreshes appinfo from the PICS servers; with 1 it updates all apps. | [0\|1] : trigger app info update, optionally for update all | steamclient.so |
| `app_install` | Console: `app_install <appId> [volumeindex]` starts installing an app, optionally into the library folder with that index (see `library_folder_list`). | <appId> [volumeindex]  | steamui.so |
| `app_installed_files` | Console: `app_installed_files <AppID>` lists the files installed for an app. *(medium)* | <AppID>  | steamclient.so |
| `app_license_request` | Console: `app_license_request <AppID>` asks for a free license for an app the account doesn't own yet (free-to-play/free apps). | <AppID> - Requests a free licenses for this app if not already owned. | steamui.so |
| `app_mark_validation` | Console: `app_mark_validation <appId> <0\|1>` marks an app as needing file validation; 1 requests a full validation. *(medium)* | <appId> <0\|1:full> | steamui.so |
| `app_move` | Console: `app_move <appId> <volumeindex>` moves an installed app to another library folder, given by its volume index. | <appId> <volumeindex> | steamui.so |
| `app_set_config` | Console: `app_set_config <AppID> <key> <value>` sets a per-app config value in the client's app config. | <AppID> <key> <value> - sets a config value for given app. | steamclient.so |
| `app_start_validation` | Console: `app_start_validation <appId>` starts verifying the integrity of an app's files, like 'Verify integrity of game files'. | <appId> | steamui.so |
| `app_status` | Console: `app_status <appId>` prints install state, size, update and download status for an app. | app_status <appId> | steamclient.so |
| `app_stop` | Console: `app_stop <appid> [force:0\|1]` stops a running app; with `1` it forces termination. | <appid> [force:0\|1] stop this running app | steamclient.so |
| `app_uninstall` | Console: `app_uninstall <appId>` uninstalls an app. | <appId> | steamui.so |
| `app_update_cancel` | Console: `app_update_cancel <EAppUpdateError>` cancels the running app update, taking the EAppUpdateError code to report as the reason. Mainly a debug command. *(medium)* | <EAppUpdateError> | steamclient.so |
| `app_update_status` | Console: `app_update_status [appId]` prints update/download progress for one app, or for all apps that are updating. | app_update_status [appId] | steamclient.so |
| `apps_installed` | Console: list all installed apps with their IDs and install status. *(medium)* |  | steamclient.so |
| `apps_running` | Console: show the running games Steam tracks (app IDs, processes). | displays information about running games tracked by Steam  | steamclient.so |
| `async_disconnect` | Console debug command: disconnect from the Steam CM server asynchronously, to test reconnect handling. *(medium)* | async disconnect | steamclient.so |
| `build_installer` | Console: `build_installer <project file> <target folder> [beta key] [beta pwd]` builds a retail/backup installer from a project file, optionally from a beta branch. | <project file> <target folder> [beta key] [beta pwd] | steamui.so |
| `cloud_file_exists` | Console: `cloud_file_exists <appid> <root> <file>` checks whether a file exists in an app's Steam Cloud storage under the given root. | <appid> <root> <file> | steamui.so |
| `cloud_get_file_info` | Console: `cloud_get_file_info <appid> <index> [bExternalAPI=1]` prints info about the Nth Steam Cloud file of an app. | <appid> <index> [bExternalAPI=1] | steamui.so |
| `cloud_get_num_files` | Console: `cloud_get_num_files <appid> [bExternalAPI=1]` prints how many Steam Cloud files an app has. | <appid> [bExternalAPI=1] | steamui.so |
| `cloud_sync_app` | Console: `cloud_sync_app <appid>` runs the background Steam Cloud sync for an app. | <appid> Manually triggers background cloud sync of app | steamui.so |
| `cloud_sync_down` | Console: `cloud_sync_down <appid>` runs the on-launch Steam Cloud sync for an app, which downloads newer cloud saves. | <appid> Manually triggers on-launch cloud sync for the given app. | steamui.so |
| `cloud_sync_up` | Console: `cloud_sync_up <appid>` runs the after-game Steam Cloud sync for an app, which uploads saves. | <appid> Manually triggers after-game cloud sync for the given app. | steamui.so |
| `cm_force_change` | Console: drop the current Connection Manager and switch to another CM server from the list. | Change CM List | steamclient.so |
| `compute_file_sha` | Console: `compute_file_sha <path>` computes and prints the SHA-1 of a file on disk. | Compute and print SHA of file on disk | steamui.so |
| `config_refresh` | Console: reload the client configuration (config/convars from the server/config store) without restarting. *(medium)* | Refresh client configuration | steamui.so |
| `connect_remote` | Console: `connect_remote <ip:port>` connects to a Remote Play / In-Home Streaming host at that address. | <ip:port> | steamui.so |
| `controller_calibration_stage` | Console: `controller_calibration_stage <stage> [controller index]` sends a calibration-stage message to the controller hardware (factory calibration/testing). | controller_calibration_stage <stage> [controller index] - send a calibration stage message to the controller hardware | steamclient.so |
| `disable_license` | Console (Steamworks developers): `disable_license <packageid>` temporarily disables a license granted through the Steamworks partner site, so you can test as a non-owner. | <packagid> Temporarily disables a license that was granted through the Steamworks site | steamui.so |
| `download_chunk` | Console: `download_chunk <appid> <depotid> <sha>` downloads one content chunk from a depot. | download_chunk <appid> <depotid> <sha>: download a single chunk from a depot | steamui.so |
| `download_depot` | Console: `download_depot <appid> <depotid> [<target manifestid>] [<delta manifestid>]` downloads one depot, optionally a specific (older) manifest. Commonly used to fetch old game versions; output lands under `steamapps/content/app_<id>/depot_<id>`. | download_depot <appid> <depotid> [<target manifestid>] [<delta manifestid>] : download a single depot | steamui.so |
| `download_item` | Console: `download_item <appid> <PublishedFileId>` downloads a Workshop item. | download_item <appid> <PublishedFileId> : download a workshop item | steamui.so |
| `download_sources` | Console: print the list of content download sources (CDN/cache servers) in use. | Dumps list of download sources | steamclient.so |
| `dump_box_ips` | Console: print the local IP addresses the client has detected on this machine. | dump the list of detected local box IP addresses | steamclient.so |
| `dump_offline_playtime` | Console: print the playtime sessions recorded locally while offline, which are later reported to the server. | Dumps recorded playtime sessions | steamclient.so |
| `dump_scheduled_functions` | Console: list the client's internal scheduled function/callback timers. | usage: "dump_scheduled_functions" Displays internal Steam function callback timers | steamclient.so |
| `enable_license` | Console (Steamworks developers): `enable_license <packageid>` re-enables a license that was turned off with `disable_license`. | <packagid> Enables a previously disabled license that was granted through the Steamworks site | steamui.so |
| `find` | Console: `find <substring>` lists console commands and convars whose names or help contain the text. | find substrings in console commands | steamui.so |
| `gamestream_debug` | Console: `gamestream_debug <0\|1>` turns verbose game-streaming (Remote Play) debug logging on or off. | Turns verbose debug logging for game streaming on (1) / off (0) | steamui.so |
| `gamestream_fail` | Console debug command: force the current game-stream session to fail, to test error handling. | Fails the current game stream session | steamui.so |
| `get_download_throttle` | Console: print the current download bandwidth limit (see `set_download_throttle`). *(high)* |  | steamclient.so |
| `gr_enum_audio` | Console (game recording): list the audio sessions/sources that game recording can capture. | Enumerate audio sessions | steamui.so |
| `gr_write_json` | Console (game recording): write the game-recording metadata JSON (clip timeline: time, duration). *(medium)* | Writes the game recording JSON | steamui.so |
| `http_cache_clearall` | Console: delete all cached data from the client's internal HTTP client and the CEF browser cache. | Delete all data from internal HTTP client and CEF browser | steamclient.so |
| `http_test` | Console: `http_test [url]` tests HTTP connectivity with a request to the given URL (or a default one). | <optional_url> test HTTP connectivity via specified URL | steamui.so |
| `httpclients` | Console: print statistics for the client's HTTP clients. | Dumps HTTP client stats | steamui.so |
| `jobs` | Console: `jobs [group_by_attribute]` lists the active internal jobs (async tasks) in this process, optionally grouped. | usage: jobs [group_by_attribute] Lists the currently active jobs running in this shell | steamui.so |
| `kv_stats` | Console: print KeyValues memory/usage statistics. | Render KeyValues stats | steamui.so |
| `library_asset_cache_print` | Console: `library_asset_cache_print <appid>` prints the cached library artwork (capsule, hero, logo with logo_position) for an app. | Prints library assets info for the given appid | steamui.so |
| `library_asset_cache_recheck` | Console: `library_asset_cache_recheck <appid>` checks an app's cached library artwork again and refetches it, e.g. to fix missing or stale capsule images. | Rechecks the library assets for the given appid | steamui.so |
| `library_folder_add` | Console: `library_folder_add <path>` adds a directory as a Steam library folder. | <path> | steamui.so |
| `library_folder_list` | Console: list all mounted Steam library folders (volumes) with their indexes. These indexes are what `app_install`/`app_move` take as `volumeindex`. | list all mounted Steam volumes | steamclient.so |
| `licenses_for_app` | Console: `licenses_for_app <appid>` lists the account's active licenses (packages) that grant the app. | <appid> : shows active licenses for appid | steamclient.so |
| `licenses_print` | Console: list all licenses (packages) owned by the logged-in account. | display users's Steam3 licenses | steamclient.so |
| `log_callbacks` | Console: `log_callbacks <first callbackID> [last callbackID]` logs Steam API callbacks with IDs in the range as they are posted. | usage: "log_callbacks <first callbackID> [last callbackID] | steamclient.so |
| `log_ipc` | Console: `log_ipc [counts\|verbose\|#maxcount] <filter>` turns on logging of IPC calls between Steam processes and games, filtered by name. The default mode is `counts`. | usage: "log_ipc [counts\|verbose\|#maxcount] <filter>" Enables IPC logging. Specifying "counts" or "verbose" is optional, defaulting to counts. | steamclient.so |
| `manifest_dump` | Console: `manifest_dump <filename> [0\|1]` prints the contents of a depot manifest file; with 1 it also lists the chunks. | <filename> [0\|1: include chunks] | steamclient.so |
| `mem_stats` | Console: print memory allocation statistics for the steamclient process. | Dump memory stats | steamclient.so |
| `mem_validate` | Console: `mem_validate <dump\|leaks> <threshold>` runs a memory validation pass in the Steam UI process and dumps allocations or reports leaks above the threshold. *(medium)* | <dump\|leaks> <threshold> : validates memory | steamui.so |
| `mem_walk` | Console: `mem_walk [full]` walks and validates the heap; `full` does a complete pass. *(medium)* | [full] : validates memory | steamui.so |
| `@metricsDisabledCatalogs` | Not an ordinary command: a server/config-driven setting (`@` prefix) holding a comma-separated list of metrics catalogs to disable. It is checked last, after the enabled/disabled operation lists. | Comma separated list of metrics catalogs to disable.  This is the last check. | gamelauncher, libvideo.so, steam, steamservice.so, steamui.so |
| `@metricsDisabledOperations` | Config-driven setting (`@` prefix): a comma-separated list of metrics operations to disable. It has the highest priority over the other metrics settings, including `@bMetricsEnabled`. | Comma separated list of metrics operations that are disabled.  This setting has highest priority | gamelauncher, libvideo.so, steam, steamservice.so, steamui.so |
| `@metricsEnabledOperations` | Config-driven setting (`@` prefix): a comma-separated list of metrics operations to enable even if their catalog is in `@metricsDisabledCatalogs`. | Comma separated list of metrics operations.  Overrides disabled catalogs | gamelauncher, libvideo.so, steam, steamservice.so, steamui.so |
| `minidump_assert` | Console debug command: trigger an assert so the assert/minidump reporting path runs. | generates an assert | steamui.so |
| `minidump_crash` | Console debug command: crash the Steam client on purpose, to test crash dumps and reporting. | crashes the Steam client | steamui.so |
| `net_fake_state` | Console: `net_fake_state <normal\|NoLAN\|CaptivePortal_Redirected\|CaptivePortal_InPlace\|NoInternet\|NoSteam>` simulates network conditions to test offline and captive-portal UI. Use `normal` to restore. The `-net_fake_state` switch sets the startup value. | {normal\|NoLAN\|CaptivePortal_Redirected\|CaptivePortal_InPlace\|NoInternet\|NoSteam} Simulate network conditions | steamclient.so |
| `net_msgdump` | Console: print the list of network messages sent to the Steam backend. | Dumps list of sent net messages | steamclient.so |
| `net_msgspew` | Console: log every sent and received Steam network (CM) message as it happens. | Spews sent and recv net messages | steamclient.so |
| `open` | Console: `open <internal url>` opens a main Steam navigation page, like `steam://open/<page>` (e.g. `open games`, `open settings`). The argument format is assumed. *(medium)* | opens a main Steam navigation page to the specified internal URL | steamui.so |
| `p2p_info` | Console: print the current state of the P2P networking subsystem (sessions, relays). | usage: "p2p_info" Displays the current state of the P2P networking subsystem. | steamclient.so |
| `package_info_print` | Console: `package_info_print <packageid>` prints the cached package info (apps, depots, license type) for a package (sub). | Dumps package info for packageID | steamclient.so |
| `patch_dump` | Console: `patch_dump <filename> <depotid>` prints the contents of a depot delta-patch file. | <filename> <depotid> | steamclient.so |
| `peer_content_server_status` | Console: print the status of the local peer content server, the LAN game-transfer server that listens on TCP port 27040 by default. | Dumps status of peer content server | steamclient.so |
| `print_sdr_ping` | Console: print this client's Steam Datagram Relay (SDR) ping-location string, i.e. the measured relay latencies used for matchmaking. | print current sdr ping location string  | steamclient.so |
| `profile` | Console: `profile <seconds>` runs the vprof profiler in the Steam UI process for N seconds. | <seconds> profile for N seconds | steamui.so |
| `profile_dump` | Console: dump the full vprof profile of all threads. If vprof is off, it uses the last collected data. | Tells vprof to dump the full profile of all threads (using the last profile data if vprof is off) | steamui.so |
| `profile_off` | Console: stop vprof profiling. | Turns off vprof and halts profiling | steamui.so |
| `profile_on` | Console: start vprof profiling. | Turns on vprof and begins profiling | steamui.so |
| `profile_on_dump_spikes` | Console: `profile_on_dump_spikes <ms>` starts vprof and automatically dumps any frame that takes longer than the threshold in milliseconds. Stop with `profile_off`. | Turns on vprof, and enables automatic dumping of any single frame that contains spikes above the given threshold in milliseconds (use the regular profile_off to stop) | steamui.so |
| `profile_show_gui` | Console: open a vprof profile window for each known thread. Data collection still needs `profile_on`/`profile_off`. | Tells UI to pop a profile dialog for each known thread, must use profile_on/off separately to actually enable/disable data gathering | steamui.so |
| `protobuf_parse_stats` | Console: `protobuf_parse_stats [reset]` prints a histogram of parsed protobuf message body sizes and how many were parsed on worker threads; `reset` clears the counters. Related settings: `@bProtobufParseTimeProfile`, `@bAssertOnProtoBufBodyMismatch`. | [reset] Dump the histogram of protobuf message body sizes parsed, and how many were parsed on a worker thread | steamclient.so, steamui.so |
| `quit` | Console: `quit [force\|now\|system]` exits the Steam client. Without an argument it exits safely; `force`/`now` skip waiting; `system` is probably a system-initiated exit such as a shutdown. | quit [force\|now\|system] : instructs the Steam client to do a safe or forced exit | steamui.so |
| `remote_client_dongle` | Console: controls a Remote Play/Steam Link wireless dongle. Syntax: `remote_client_dongle [[connect] clientid ssid password] \| disconnect \| status \| disable \| enable \| leddebug \| lednodebug \| verbose 0\|1 \| debugpdthresh <thres>` (default threshold -75). | remote_client_dongle [[connect] clientid ssid password]\|disconnect\|status\|disable\|enable\|leddebug\|lednodebug\|[verbose 0\|1]\|[debugpdthresh thres (default -75)] | steamclient.so |
| `remote_client_softapcmd` | Console: `remote_client_softapcmd <args>` sends a raw command to the soft access point used for direct Remote Play / Steam Link connections. *(medium)* | remote_client_softapcmd <softapcmd args> | steamclient.so |
| `remote_clients` | Console: print information about Remote Play / In-Home Streaming clients found on the LAN. | dump remote client info | steamclient.so |
| `render_ipc_connections` | Console: list or draw the active IPC connections between Steam and connected processes. *(medium)* | usage: "render_ipc_connections | steamclient.so |
| `reset_all_stats` | Console (developer): clear all stats and achievements for the current user, probably `reset_all_stats <appid>`. *(medium)* | Clears all stats and achievement | steamui.so |
| `serverbrowser_debug_toggle` | Console: turn debug logging for the game server browser (master server queries) on or off. | Enable debug spew for server browser | steamclient.so |
| `serverbrowser_debug_verbose` | Console: turn on verbose debug logging for the server browser. Valve's help string is the same as for `serverbrowser_debug_toggle`. *(medium)* | Enable debug spew for server browser | steamclient.so |
| `service_repair` | Console: repair the Steam Client Service. Windows only; no effect on Linux. | Repair Steam service | steamui.so |
| `service_restart` | Console: restart the Steam Client Service. Windows only. | Restarts Steam Windows service  | steamui.so |
| `service_test` | Console: test that the Steam Client Service works. Windows only. | Test Steam service | steamui.so |
| `set_display_state` | Console: `set_display_state <eState>` forces the display into a given state (a numeric display-state enum, e.g. on/off/dimmed on SteamOS). Used to test display power handling. *(medium)* | <eState> Force the display to a specific state. | steamui.so |
| `set_download_throttle` | Console: `set_download_throttle <kbps> [bPersistent]` limits download bandwidth in kbps. 0 is probably unlimited; with a true second argument the limit is saved across sessions. | set_download_throttle <kbps> <bPersistent = false> | steamclient.so |
| `set_spew` | Console: `set_spew <group> <spewlevel> <loglevel>` sets the console-spew and log-file levels for one logging group. | <group> <spewlevel> <loglevel> Sets spew and log levels for a given group | steamui.so |
| `set_spew_level` | Console: `set_spew_level <spewlevel> <loglevel>` sets the console-spew and log-file levels for all logging groups. | <SpewLevel LogLevel> Sets spew and log levels for all groups | steamui.so |
| `set_var` | Console: `set_var <name> <value>` sets the value of a console variable (convar). | <name> <value>- Set the value of a Cvar | steamui.so |
| `shader_build` | Console: `shader_build <appId> [threadCount]` compiles an app's pre-cached shaders (Fossilize replay) now, optionally with that many threads. | shader_build <appId> <optionalThreadCount> | steamui.so |
| `shader_process` | Console: `shader_process <appId> <bucketID> [overrideBasePath]` processes one shader-cache bucket for an app, optionally from a different base path. *(medium)* | shader_process <appId> <bucketID> <optionalOverrideBasePath> | steamui.so |
| `shader_prune` | Console: delete stale or unneeded shader cache data. *(medium)* | shader_prune | steamui.so |
| `shader_scan` | Console: `shader_scan <appId> [overridePath]` scans an app's shader cache, optionally from another path. *(medium)* | shader_scan <appId> <optionalOverridePath> | steamui.so |
| `stats_dump` | Console: `stats_dump [filter]` prints the internal debug stats (counters) whose names match the filter. | stats_dump [filter] : dumps matching debug stats | steamui.so |
| `stats_monitor` | Console: `stats_monitor <stat name>` keeps watching one debug stat and shows its value as it changes. | stats_monitor <stat name> : monitor a debug stat value | steamui.so |
| `stats_reset` | Console: `stats_reset [filter]` sets matching debug stats back to 0. | stats_reset [filter] : set matching stats back to 0 | steamui.so |
| `test_concurrent_textfilter_change` | Console test command: queue several text-filter (chat profanity filter) setting changes for the UI at once, to test race handling. | Queue up multiple text filter changes to the UI | steamclient.so |
| `test_dropcon` | Console test command: drop the current Steam backend connection, to test reconnect behavior. | Tests dropping a connection | steamclient.so |
| `test_failnextconnect` | Console test command: make the next connection attempt to the backend fail. | Tests failing the next connection | steamclient.so |
| `test_opus_voice_encode` | Console test command: encode voice data with the Opus codec as a test. | test an opus voice encode | steamclient.so |
| `test_os_suspend` | Console test command (steamclient): simulate the OS announcing a system suspend. | Simulate the OS telling us it is suspending | steamclient.so |
| `test_reconnect` | Console test command: reconnect after `test_failnextconnect` or `test_dropcon`. | Reconnect after using test_failnextconnect&test_dropcon | steamclient.so |
| `test_resume` | Console test command (steamclient): simulate resuming from a system suspend; pairs with `test_os_suspend`. | Resumes from a system suspend | steamclient.so |
| `test_resume_from_suspend` | Console test command (Steam UI): run the UI's resume-from-suspend handling. | test on resume from suspend | steamui.so |
| `test_suspend` | Console test command (Steam UI): fake a system suspend event. | Fakes a system suspend event | steamui.so |
| `test_voice_encode` | Console test command: encode voice data with the default/legacy voice codec as a test. | test a voice encode | steamclient.so |
| `timed_trial_add_playtime` | Console (developer only): `timed_trial_add_playtime <appId> <seconds>` adds playtime to a timed-trial app, to test trial expiry. | timed_trial_add_playtime <appId> <seconds>: add trial app playtime (developer only) | steamclient.so |
| `timed_trial_reset_playtime` | Console (developer only): `timed_trial_reset_playtime <appId>` resets the playtime used on a timed-trial app. | timed_trial_reset_playtime <appId> : reset trial app playtime (developer only) | steamclient.so |
| `timed_trial_status` | Console: `timed_trial_status <appId>` shows the timed-trial status (time allowed and used) for an app. | timed_trial_status <appId> : show time trial app status | steamclient.so |
| `toggle_idle_suspend_inhibit` | Console: `toggle_idle_suspend_inhibit <delay>` toggles inhibiting idle suspend after the given delay, to test SteamOS idle-suspend handling. | <delay> Enable/disable suspend inhibit after specified delay | steamui.so |
| `user_friends` | Console: print the logged-in user's friends list. | Dumps list of friends | steamclient.so |
| `user_info` | Console: print various information about the Steam session and user (account, login state). | Dump various Steam info | steamui.so |
| `verify_chunk_store` | Console: `verify_chunk_store <appid> <depotid> <datafile>` checks a depot chunk store / data file. Valve's help text ('run app depot build as specified in appbuildfile') looks copied from another command, so the exact behavior is uncertain. *(medium)* | verify_chunk_store <appid> <depotid> <datafile> : run app depot build as specified in appbuildfile | steamui.so |
| `vgui_spewpanelstats` | Console: print statistics about the active VGUI panels (counts per type), for the legacy VGUI UI. | spew active panel stats | steamui.so |
| `voice_game_usage` | Console: show how the running game uses Steam Voice (ISteamUser voice APIs). | displays information about the game's use of Steam voice | steamclient.so |
| `workshop_download_item` | Console: `workshop_download_item <appid> <PublishedFileId>` downloads a Workshop item. Works like `download_item` and is commonly used to fetch mods manually. | workshop_download_item <appid> <PublishedFileId> : download a workshop item | steamui.so |
| `workshop_status` | Console: `workshop_status <appId>` prints the Workshop subscription and download status for an app's items. | workshop_status <appId> | steamclient.so |
