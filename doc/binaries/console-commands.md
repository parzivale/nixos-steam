# Console commands (ConCommands)

> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

Every console command registered in the client binaries (name and help text). Run them in the Steam
console (`steam://open/console`).

Total: **133**.

| Command | Description (Valve help text) | Binaries |
|---|---|---|
| `achievement_clear` | Clears an achievement | steamui.so |
| `app_backup` | <appId> <target folder> [max folder size MB] | steamui.so |
| `app_change_compat_tool` | <appid> <name> [config=] | steamui.so |
| `app_delay_update` | <appid> <seconds> force delay update | steamclient.so |
| `app_dlc_status` | app_status <appId> <dlcId> | steamclient.so |
| `app_download_enable` | <0\|1> | steamui.so |
| `app_info_find` | Find apps with a certain appinfo value set, eg 'common/type media'. * is any.  | steamclient.so |
| `app_info_print` | app_info_print <appid> [section] : print app info for appID | steamui.so |
| `app_info_update` | [0\|1] : trigger app info update, optionally for update all | steamclient.so |
| `app_install` | <appId> [volumeindex]  | steamui.so |
| `app_installed_files` | <AppID>  | steamclient.so |
| `app_license_request` | <AppID> - Requests a free licenses for this app if not already owned. | steamui.so |
| `app_mark_validation` | <appId> <0\|1:full> | steamui.so |
| `app_move` | <appId> <volumeindex> | steamui.so |
| `app_set_config` | <AppID> <key> <value> - sets a config value for given app. | steamclient.so |
| `app_start_validation` | <appId> | steamui.so |
| `app_status` | app_status <appId> | steamclient.so |
| `app_stop` | <appid> [force:0\|1] stop this running app | steamclient.so |
| `app_uninstall` | <appId> | steamui.so |
| `app_update_cancel` | <EAppUpdateError> | steamclient.so |
| `app_update_status` | app_update_status [appId] | steamclient.so |
| `apps_installed` |  | steamclient.so |
| `apps_running` | displays information about running games tracked by Steam  | steamclient.so |
| `async_disconnect` | async disconnect | steamclient.so |
| `build_installer` | <project file> <target folder> [beta key] [beta pwd] | steamui.so |
| `cloud_file_exists` | <appid> <root> <file> | steamui.so |
| `cloud_get_file_info` | <appid> <index> [bExternalAPI=1] | steamui.so |
| `cloud_get_num_files` | <appid> [bExternalAPI=1] | steamui.so |
| `cloud_sync_app` | <appid> Manually triggers background cloud sync of app | steamui.so |
| `cloud_sync_down` | <appid> Manually triggers on-launch cloud sync for the given app. | steamui.so |
| `cloud_sync_up` | <appid> Manually triggers after-game cloud sync for the given app. | steamui.so |
| `cm_force_change` | Change CM List | steamclient.so |
| `compute_file_sha` | Compute and print SHA of file on disk | steamui.so |
| `config_refresh` | Refresh client configuration | steamui.so |
| `connect_remote` | <ip:port> | steamui.so |
| `controller_calibration_stage` | controller_calibration_stage <stage> [controller index] - send a calibration stage message to the controller hardware | steamclient.so |
| `disable_license` | <packagid> Temporarily disables a license that was granted through the Steamworks site | steamui.so |
| `download_chunk` | download_chunk <appid> <depotid> <sha>: download a single chunk from a depot | steamui.so |
| `download_depot` | download_depot <appid> <depotid> [<target manifestid>] [<delta manifestid>] : download a single depot | steamui.so |
| `download_item` | download_item <appid> <PublishedFileId> : download a workshop item | steamui.so |
| `download_sources` | Dumps list of download sources | steamclient.so |
| `dump_box_ips` | dump the list of detected local box IP addresses | steamclient.so |
| `dump_offline_playtime` | Dumps recorded playtime sessions | steamclient.so |
| `dump_scheduled_functions` | usage: "dump_scheduled_functions" Displays internal Steam function callback timers | steamclient.so |
| `enable_license` | <packagid> Enables a previously disabled license that was granted through the Steamworks site | steamui.so |
| `find` | find substrings in console commands | steamui.so |
| `gamestream_debug` | Turns verbose debug logging for game streaming on (1) / off (0) | steamui.so |
| `gamestream_fail` | Fails the current game stream session | steamui.so |
| `get_download_throttle` |  | steamclient.so |
| `gr_enum_audio` | Enumerate audio sessions | steamui.so |
| `gr_write_json` | Writes the game recording JSON | steamui.so |
| `http_cache_clearall` | Delete all data from internal HTTP client and CEF browser | steamclient.so |
| `http_test` | <optional_url> test HTTP connectivity via specified URL | steamui.so |
| `httpclients` | Dumps HTTP client stats | steamui.so |
| `jobs` | usage: jobs [group_by_attribute] Lists the currently active jobs running in this shell | steamui.so |
| `kv_stats` | Render KeyValues stats | steamui.so |
| `library_asset_cache_print` | Prints library assets info for the given appid | steamui.so |
| `library_asset_cache_recheck` | Rechecks the library assets for the given appid | steamui.so |
| `library_folder_add` | <path> | steamui.so |
| `library_folder_list` | list all mounted Steam volumes | steamclient.so |
| `licenses_for_app` | <appid> : shows active licenses for appid | steamclient.so |
| `licenses_print` | display users's Steam3 licenses | steamclient.so |
| `log_callbacks` | usage: "log_callbacks <first callbackID> [last callbackID] | steamclient.so |
| `log_ipc` | usage: "log_ipc [counts\|verbose\|#maxcount] <filter>" Enables IPC logging. Specifying "counts" or "verbose" is optional, defaulting to counts. | steamclient.so |
| `manifest_dump` | <filename> [0\|1: include chunks] | steamclient.so |
| `mem_stats` | Dump memory stats | steamclient.so |
| `mem_validate` | <dump\|leaks> <threshold> : validates memory | steamui.so |
| `mem_walk` | [full] : validates memory | steamui.so |
| `@metricsDisabledCatalogs` | Comma separated list of metrics catalogs to disable.  This is the last check. | gamelauncher, libvideo.so, steam, steamservice.so, steamui.so |
| `@metricsDisabledOperations` | Comma separated list of metrics operations that are disabled.  This setting has highest priority | gamelauncher, libvideo.so, steam, steamservice.so, steamui.so |
| `@metricsEnabledOperations` | Comma separated list of metrics operations.  Overrides disabled catalogs | gamelauncher, libvideo.so, steam, steamservice.so, steamui.so |
| `minidump_assert` | generates an assert | steamui.so |
| `minidump_crash` | crashes the Steam client | steamui.so |
| `net_fake_state` | {normal\|NoLAN\|CaptivePortal_Redirected\|CaptivePortal_InPlace\|NoInternet\|NoSteam} Simulate network conditions | steamclient.so |
| `net_msgdump` | Dumps list of sent net messages | steamclient.so |
| `net_msgspew` | Spews sent and recv net messages | steamclient.so |
| `open` | opens a main Steam navigation page to the specified internal URL | steamui.so |
| `p2p_info` | usage: "p2p_info" Displays the current state of the P2P networking subsystem. | steamclient.so |
| `package_info_print` | Dumps package info for packageID | steamclient.so |
| `patch_dump` | <filename> <depotid> | steamclient.so |
| `peer_content_server_status` | Dumps status of peer content server | steamclient.so |
| `print_sdr_ping` | print current sdr ping location string  | steamclient.so |
| `profile` | <seconds> profile for N seconds | steamui.so |
| `profile_dump` | Tells vprof to dump the full profile of all threads (using the last profile data if vprof is off) | steamui.so |
| `profile_off` | Turns off vprof and halts profiling | steamui.so |
| `profile_on` | Turns on vprof and begins profiling | steamui.so |
| `profile_on_dump_spikes` | Turns on vprof, and enables automatic dumping of any single frame that contains spikes above the given threshold in milliseconds (use the regular profile_off to stop) | steamui.so |
| `profile_show_gui` | Tells UI to pop a profile dialog for each known thread, must use profile_on/off separately to actually enable/disable data gathering | steamui.so |
| `protobuf_parse_stats` | [reset] Dump the histogram of protobuf message body sizes parsed, and how many were parsed on a worker thread | steamclient.so, steamui.so |
| `quit` | quit [force\|now\|system] : instructs the Steam client to do a safe or forced exit | steamui.so |
| `remote_client_dongle` | remote_client_dongle [[connect] clientid ssid password]\|disconnect\|status\|disable\|enable\|leddebug\|lednodebug\|[verbose 0\|1]\|[debugpdthresh thres (default -75)] | steamclient.so |
| `remote_client_softapcmd` | remote_client_softapcmd <softapcmd args> | steamclient.so |
| `remote_clients` | dump remote client info | steamclient.so |
| `render_ipc_connections` | usage: "render_ipc_connections | steamclient.so |
| `reset_all_stats` | Clears all stats and achievement | steamui.so |
| `serverbrowser_debug_toggle` | Enable debug spew for server browser | steamclient.so |
| `serverbrowser_debug_verbose` | Enable debug spew for server browser | steamclient.so |
| `service_repair` | Repair Steam service | steamui.so |
| `service_restart` | Restarts Steam Windows service  | steamui.so |
| `service_test` | Test Steam service | steamui.so |
| `set_display_state` | <eState> Force the display to a specific state. | steamui.so |
| `set_download_throttle` | set_download_throttle <kbps> <bPersistent = false> | steamclient.so |
| `set_spew` | <group> <spewlevel> <loglevel> Sets spew and log levels for a given group | steamui.so |
| `set_spew_level` | <SpewLevel LogLevel> Sets spew and log levels for all groups | steamui.so |
| `set_var` | <name> <value>- Set the value of a Cvar | steamui.so |
| `shader_build` | shader_build <appId> <optionalThreadCount> | steamui.so |
| `shader_process` | shader_process <appId> <bucketID> <optionalOverrideBasePath> | steamui.so |
| `shader_prune` | shader_prune | steamui.so |
| `shader_scan` | shader_scan <appId> <optionalOverridePath> | steamui.so |
| `stats_dump` | stats_dump [filter] : dumps matching debug stats | steamui.so |
| `stats_monitor` | stats_monitor <stat name> : monitor a debug stat value | steamui.so |
| `stats_reset` | stats_reset [filter] : set matching stats back to 0 | steamui.so |
| `test_concurrent_textfilter_change` | Queue up multiple text filter changes to the UI | steamclient.so |
| `test_dropcon` | Tests dropping a connection | steamclient.so |
| `test_failnextconnect` | Tests failing the next connection | steamclient.so |
| `test_opus_voice_encode` | test an opus voice encode | steamclient.so |
| `test_os_suspend` | Simulate the OS telling us it is suspending | steamclient.so |
| `test_reconnect` | Reconnect after using test_failnextconnect&test_dropcon | steamclient.so |
| `test_resume` | Resumes from a system suspend | steamclient.so |
| `test_resume_from_suspend` | test on resume from suspend | steamui.so |
| `test_suspend` | Fakes a system suspend event | steamui.so |
| `test_voice_encode` | test a voice encode | steamclient.so |
| `timed_trial_add_playtime` | timed_trial_add_playtime <appId> <seconds>: add trial app playtime (developer only) | steamclient.so |
| `timed_trial_reset_playtime` | timed_trial_reset_playtime <appId> : reset trial app playtime (developer only) | steamclient.so |
| `timed_trial_status` | timed_trial_status <appId> : show time trial app status | steamclient.so |
| `toggle_idle_suspend_inhibit` | <delay> Enable/disable suspend inhibit after specified delay | steamui.so |
| `user_friends` | Dumps list of friends | steamclient.so |
| `user_info` | Dump various Steam info | steamui.so |
| `verify_chunk_store` | verify_chunk_store <appid> <depotid> <datafile> : run app depot build as specified in appbuildfile | steamui.so |
| `vgui_spewpanelstats` | spew active panel stats | steamui.so |
| `voice_game_usage` | displays information about the game's use of Steam voice | steamclient.so |
| `workshop_download_item` | workshop_download_item <appid> <PublishedFileId> : download a workshop item | steamui.so |
| `workshop_status` | workshop_status <appId> | steamclient.so |
