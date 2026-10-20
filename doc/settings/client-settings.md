# Client settings (`CMsgClientSettings`)

This is the canonical list of user-facing *and* hidden client settings. It was recovered from the protobuf
descriptor `steammessages_clientsettings.proto`, which is embedded in `steamclient.so`/`steamui.so`.
The settings UI (`SteamClient.Settings`) reads and writes these fields, and each field carries custom
options that say where the value is persisted and what its default is.

Total settings: **270**

## Storage backends (`EClientSettingStore`)

| Store | Where it lives |
|---|---|
| Install | ConfigStore/Install (config/config.vdf) |
| UserRoaming | ConfigStore/UserRoaming (userdata/<id>/7/remote/sharedconfig.vdf) |
| UserLocal | ConfigStore/UserLocal (userdata/<id>/config/localconfig.vdf) |
| Registry | Registry (registry.vdf) |
| CustomFunc | CustomFunc (computed in code) |

Key paths use `\` as the KeyValues path separator; e.g. `system\EnableGameOverlay` in the UserLocal
store is `UserLocalConfigStore/system/EnableGameOverlay` in `localconfig.vdf`. Registry-store names are
keys under `Registry/HKCU/Software/Valve/Steam` in `~/.steam/registry.vdf`. `CustomFunc` settings have no
single backing key; the client computes them or forwards them to subsystems such as the voice, ping and
screenshot managers.

Flags: `pre-login` = available before a user signs in; `read-only` = cannot be set; `per-game`/`per-display` = stored per profile; `clamp` = value range enforced by the client.

## All settings

| # | Field | Type | Store | Key | Default | Flags | Description |
|---|---|---|---|---|---|---|---|
| 1 | `no_save_personal_info` | bool | Install | `Software\Valve\Steam\NoSavePersonalInfo` |  |  |  |
| 5 | `preferred_monitor` | string | Install | `BigPicture/Monitor` |  |  |  |
| 6 | `steam_cef_gpu_blocklist_disabled` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\CEFGPUBlocklistDisabled` |  |  |  |
| 7 | `bigpicture_windowed` | bool | Install | `BigPicture/Windowed` |  | pre-login |  |
| 8 | `display_name` | string | Install | `UI/Display/Current/Name` |  |  |  |
| 9 | `is_external_display` | bool | Install | `UI/Display/Current/IsExternalDisplay` |  |  |  |
| 10 | `steam_os_underscan_level` | float | Install | `SteamOSScreenUnderscanLevel` |  |  |  |
| 11 | `steam_os_underscan_enabled` | bool | Install | `SteamOSScreenUnderscanEnabled` |  |  |  |
| 12 | `min_scale_factor` | float | Install | `UI/Display/Current/MinScaleFactor` |  |  |  |
| 13 | `max_scale_factor` | float | Install | `UI/Display/Current/MaxScaleFactor` |  |  |  |
| 14 | `auto_scale_factor` | float | Install | `UI/Display/Current/AutoScaleFactor` |  |  |  |
| 16 | `small_mode` | bool | UserLocal | `Software\Valve\Steam\SmallMode` |  |  |  |
| 19 | `skip_steamvr_install_dialog` | bool | UserLocal | `system\SteamVRHMDVGUIWarning` |  |  |  |
| 20 | `always_show_user_chooser` | bool | Install | `WebStorage\Auth\AlwaysShowUserChooser` |  |  |  |
| 21 | `os_version_unsupported` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\OSVersionUnsupported` |  |  |  |
| 3000 | `show_family_sharing_notifications` | bool | CustomFunc |  |  |  |  |
| 3001 | `show_copy_count_in_library` | bool | UserLocal | `ShowCopyCountInLibrary` | `true` |  |  |
| 4000 | `overlay_fps_counter_corner` | int32 | UserLocal | `system\InGameOverlayShowFPSCorner` |  |  |  |
| 4001 | `overlay_fps_counter_high_contrast` | bool | UserLocal | `system\InGameOverlayShowFPSContrast` |  |  |  |
| 4002 | `overlay_key` | CMsgHotkey | UserLocal | `system\InGameOverlayShortcutKey` | `'Shift\tKEY_TAB'` |  |  |
| 4003 | `screenshot_key` | CMsgHotkey | UserLocal | `system\InGameOverlayScreenshotHotKey` | `'KEY_F12'` |  |  |
| 4004 | `enable_overlay` | bool | UserLocal | `system\EnableGameOverlay` | `true` |  |  |
| 4006 | `enable_screenshot_notification` | bool | UserLocal | `system\InGameOverlayScreenshotNotification` | `true` |  |  |
| 4007 | `enable_screenshot_sound` | bool | UserLocal | `system\InGameOverlayScreenshotPlaySound` | `true` |  |  |
| 4008 | `save_uncompressed_screenshots` | bool | UserLocal | `system\InGameOverlayScreenshotSaveUncompressed` |  |  |  |
| 4009 | `screenshots_path` | string | CustomFunc |  |  |  |  |
| 4010 | `default_ping_rate` | int32 | CustomFunc |  |  | read-only | Computed default (automatic) server ping rate based on network speed |
| 4011 | `server_ping_rate` | int32 | CustomFunc |  |  |  |  |
| 4012 | `steam_networking_share_ip` | int32 | CustomFunc |  |  |  |  |
| 4013 | `web_browser_home` | string | CustomFunc |  |  |  |  |
| 4014 | `voice_mic_device_name` | string | CustomFunc |  |  |  |  |
| 4015 | `voice_mic_input_gain` | float | CustomFunc |  |  |  |  |
| 4016 | `voice_speaker_output_gain` | float | CustomFunc |  |  |  |  |
| 4017 | `voice_push_to_talk_setting` | int32 | CustomFunc |  |  |  |  |
| 4018 | `voice_push_to_talk_key` | CMsgHotkey | CustomFunc |  |  |  |  |
| 4019 | `overlay_toolbar_list_view` | bool | UserLocal | `OverlayToolBarListView` |  |  |  |
| 4020 | `always_use_gamepadui_overlay` | bool | UserLocal | `system\EnableSCTenFootOverlayCheckNew` |  |  |  |
| 4021 | `overlay_tabs` | string | UserRoaming | `OverlayTabs` |  |  |  |
| 4022 | `overlay_scale_interface` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\OverlayScaleInterface` | `true` |  |  |
| 4023 | `overlay_restore_browser_tabs` | bool | UserLocal | `system\InGameOverlayRestoreBrowserTabs` | `true` |  |  |
| 4024 | `enable_avif_screenshots` | bool | UserLocal | `system\InGameOverlayScreenshotEnableAVIF` |  |  |  |
| 4025 | `overlay_fps_counter_detail_level` | int32 | UserLocal | `system\InGameOverlayShowFPSDetailLevel` | `1` |  |  |
| 4026 | `overlay_fps_counter_saturation_factor` | float | UserLocal | `system\InGameOverlayShowFPSSaturation` | `1` |  |  |
| 4027 | `overlay_fps_counter_bgopacity` | float | UserLocal | `system\InGameOverlayShowFPSBGOpacity` | `0.8` |  |  |
| 4028 | `overlay_fps_counter_scale_factor` | float | UserLocal | `system\InGameOverlayShowFPSScaling` | `0.7` |  |  |
| 4029 | `overlay_fps_counter_key` | CMsgHotkey | UserLocal | `system\InGameOverlayShowFPSHotKey` | `'Default'` |  |  |
| 4030 | `overlay_fps_counter_fps_graph` | bool | UserLocal | `system\InGameOverlayShowFPSGraphFPS` | `true` |  |  |
| 4031 | `overlay_fps_counter_cpu_graph` | bool | UserLocal | `system\InGameOverlayShowFPSGraphCPU` | `true` |  |  |
| 4032 | `overlay_fps_counter_allow_km_driver` | bool | UserLocal | `system\InGameOverlayAllowKMDriveOnWindows` | `true` |  |  |
| 4033 | `achievement_notification_toast` | bool | UserLocal | `system\AchievementNotificationToast` | `true` |  |  |
| 4034 | `achievement_notification_sound` | bool | UserLocal | `system\AchievementNotificationSound` | `true` |  |  |
| 4035 | `controllerconnect_notification_toast` | bool | UserLocal | `system\ControllerConnectNotificationToast` | `true` |  |  |
| 4036 | `controllerconnect_notification_sound` | bool | UserLocal | `system\ControllerConnectNotificationSound` | `false` |  |  |
| 4037 | `controller_low_battery_notification_toast` | bool | UserLocal | `system\ControllerLowBatteryNotificationToast` | `true` |  |  |
| 4038 | `controller_low_battery_notification_sound` | bool | UserLocal | `system\ControllerLowBatteryNotificationSound` | `false` |  |  |
| 4039 | `logged_in_as_user_notification_toast` | bool | UserLocal | `system\LoggedInAsUserNotificationToast` | `true` |  |  |
| 4040 | `logged_in_as_user_notification_sound` | bool | UserLocal | `system\LoggedInAsUserNotificationSound` | `false` |  |  |
| 5000 | `smooth_scroll_webviews` | bool | CustomFunc |  |  |  |  |
| 5001 | `enable_gpu_accelerated_webviews` | bool | CustomFunc |  |  |  |  |
| 5003 | `enable_hardware_video_decoding` | bool | CustomFunc |  |  |  |  |
| 5004 | `run_at_startup` | bool | CustomFunc |  |  |  |  |
| 5005 | `enable_dpi_scaling` | bool | CustomFunc |  |  |  |  |
| 5006 | `enable_marketing_messages` | bool | UserLocal | `news\NotifyAvailableGames` | `true` |  |  |
| 5007 | `start_in_big_picture_mode` | bool | CustomFunc |  |  |  |  |
| 5008 | `jumplist_flags` | uint32 | UserLocal | `system\JumplistSettings` | `77680` |  |  |
| 5009 | `enable_ui_sounds` | bool | UserLocal | `system\EnableUISounds` | `true` |  |  |
| 5010 | `enable_gamescope_composer` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\EnableGamescopeComposer` | `false` |  |  |
| 5011 | `enable_gamescope_composer_vr` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\EnableGamescopeComposerVR` | `true` |  |  |
| 5012 | `show_switch_to_desktop_at_login` | bool | Install | `system\ShowSwitchToDesktopAtLogin` |  | pre-login |  |
| 5013 | `enable_steamrt64_client` | bool | CustomFunc |  |  |  |  |
| 6000 | `disable_all_toasts` | bool | UserRoaming | `DisableAllToasts` |  |  |  |
| 6001 | `disable_toasts_in_game` | bool | UserRoaming | `DisableToastsInGame` |  |  |  |
| 6002 | `play_sound_on_toast` | bool | UserRoaming | `PlaySoundOnToast` | `true` |  |  |
| 7000 | `library_display_size` | int32 | UserLocal | `LibraryDisplaySize` |  |  |  |
| 7001 | `library_whats_new_show_only_product_updates` | bool | UserRoaming | `LibraryWhatsNewShowOnlyProductUpdates` |  |  |  |
| 7002 | `show_store_content_on_home` | bool | UserRoaming | `ShowStoreContentOnHome` | `true` |  |  |
| 7003 | `start_page` | string | CustomFunc |  |  |  |  |
| 7004 | `library_low_bandwidth_mode` | bool | UserLocal | `LibraryLowBandwidthMode` |  |  |  |
| 7005 | `library_low_perf_mode` | bool | UserLocal | `LibraryLowPerfMode` |  |  |  |
| 7006 | `library_disable_community_content` | bool | UserLocal | `LibraryDisableCommunityContent` |  |  |  |
| 7007 | `library_display_icon_in_game_list` | bool | UserLocal | `LibraryDisplayIconInGameList` | `true` |  |  |
| 7008 | `ready_to_play_includes_streaming` | bool | CustomFunc | `ReadyToPlayIncludesStreaming` |  |  |  |
| 7009 | `show_steam_deck_info` | bool | UserLocal | `ShowSteamDeckInfoInLibrary` |  |  |  |
| 7010 | `library_home_big_art` | bool | UserLocal | `LibraryHomeBigArt` |  |  |  |
| 8000 | `enable_shader_precache` | bool | CustomFunc |  |  |  |  |
| 8001 | `enable_shader_background_processing` | bool | CustomFunc |  |  |  |  |
| 8002 | `shader_precached_size` | uint64 | CustomFunc |  |  | read-only |  |
| 8003 | `needs_steam_service_repair` | bool | CustomFunc |  |  | read-only |  |
| 8004 | `download_peer_content` | int32 | CustomFunc |  |  |  |  |
| 8005 | `download_rate_bits_per_s` | bool | CustomFunc |  |  |  |  |
| 8006 | `restrict_auto_updates` | bool | CustomFunc |  |  |  |  |
| 8007 | `restrict_auto_updates_start` | int32 | CustomFunc |  |  |  |  |
| 8008 | `restrict_auto_updates_end` | int32 | CustomFunc |  |  |  |  |
| 8009 | `download_region` | int32 | CustomFunc |  |  |  |  |
| 8010 | `download_while_app_running` | bool | CustomFunc |  |  |  |  |
| 8011 | `download_throttle_while_streaming` | bool | CustomFunc |  |  |  |  |
| 8012 | `download_throttle_rate` | int32 | CustomFunc |  |  |  |  |
| 8013 | `default_app_update_behavior` | int32 | CustomFunc |  |  |  |  |
| 10000 | `cloud_enabled` | bool | UserRoaming | `Software\Valve\Steam\CloudEnabled` | `true` |  |  |
| 10001 | `show_screenshot_manager` | bool | UserRoaming | `Software\Valve\Steam\ShowScreenshotManager` |  |  |  |
| 11000 | `music_volume` | int32 | CustomFunc |  |  |  |  |
| 11001 | `music_pause_on_app_start` | bool | Install | `Music\PauseOnAppStartedProcess` |  |  |  |
| 11002 | `music_pause_on_voice_chat` | bool | Install | `Music\PauseOnVoiceChat` |  |  |  |
| 11003 | `music_download_high_quality` | bool | Install | `Music\DownloadHighQualityAudioSoundtracks` |  |  |  |
| 12000 | `broadcast_permissions` | EBroadcastPermission | UserLocal | `Broadcast\Permissions` | `1` |  |  |
| 12001 | `broadcast_output_width` | int32 | UserLocal | `Broadcast\OutputWidth` |  |  |  |
| 12002 | `broadcast_output_height` | int32 | UserLocal | `Broadcast\OutputHeight` | `720` |  |  |
| 12003 | `broadcast_bitrate` | int32 | UserLocal | `Broadcast\MaxKbps` | `2500` |  |  |
| 12004 | `broadcast_encoding_option` | EBroadcastEncoderSetting | UserLocal | `Broadcast\EncoderSetting` |  |  |  |
| 12005 | `broadcast_record_all_video` | bool | UserLocal | `Broadcast\IncludeDesktop` |  |  |  |
| 12006 | `broadcast_record_all_audio` | bool | UserLocal | `Broadcast\RecordSystemAudio` |  |  |  |
| 12007 | `broadcast_record_microphone` | bool | UserLocal | `Broadcast\RecordMic` |  |  |  |
| 12008 | `broadcast_show_upload_stats` | bool | UserLocal | `Broadcast\ShowDebugInfo` |  |  |  |
| 12009 | `broadcast_show_live_reminder` | bool | UserLocal | `Broadcast\ShowReminder` | `true` |  |  |
| 12010 | `broadcast_chat_corner` | int32 | UserLocal | `Broadcast\ShowChat` | `1` |  |  |
| 13000 | `gamestream_hardware_video_encode` | bool | UserLocal | `GameStream\HardwareVideoEncode` | `true` |  |  |
| 13001 | `gamestream_enable_video_h265` | bool | UserLocal | `GameStream\EnableVideoH265` | `true` |  |  |
| 14001 | `steam_input_configurator_error_msg_enable` | bool | Install | `SteamInput/Configurator/ErrorMsgEnabled` |  |  |  |
| 14002 | `controller_guide_button_focus_steam` | bool | UserLocal | `Controller_CheckGuideButton` | `true` |  |  |
| 14003 | `controller_ps_support` | int32 | UserLocal | `SteamController_PSSupport` | `1` |  |  |
| 14004 | `controller_xbox_support` | bool | UserLocal | `SteamController_XBoxSupport` |  |  |  |
| 14005 | `controller_xbox_driver` | bool | UserLocal | `SteamController_XBoxDriver` |  |  |  |
| 14006 | `controller_switch_support` | bool | UserLocal | `SteamController_SwitchSupport` |  |  |  |
| 14007 | `controller_generic_support` | bool | UserLocal | `SteamController_GenericGamepadSupport` |  |  |  |
| 14008 | `controller_power_off_timeout` | int32 | UserLocal | `CSettingsPanelGameController.Timeout` | `15` |  |  |
| 14009 | `turn_off_controller_on_exit` | bool | UserLocal | `CSettingsPanelGameController.TurnOff` |  |  |  |
| 14010 | `controller_combine_nintendo_joycons` | bool | Install | `SteamInput/Configurator/CombinedJoycons` |  |  |  |
| 140011 | `controller_enable_chord` | bool | UserLocal | `SteamController_Enable_Chord` | `true` |  |  |
| 140012 | `controller_poll_rate` | bool | UserLocal | `SteamController_Poll_Rate` | `2` |  |  |
| 140013 | `controller_siapi_config_author_mode` | bool | UserLocal | `SteamInput/Configurator/SIAPIAuhtorMode` | `false` |  |  |
| 140014 | `controller_show_ibex_tour` | bool | UserRoaming | `ShowIbexWelcomeTour` | `true` |  |  |
| 140030 | `controller_chat_radial_menu_option_0` | string | UserLocal | `SteamInput/ChatRadialMenu/0` |  |  |  |
| 140031 | `controller_chat_radial_menu_option_1` | string | UserLocal | `SteamInput/ChatRadialMenu/1` |  |  |  |
| 140032 | `controller_chat_radial_menu_option_2` | string | UserLocal | `SteamInput/ChatRadialMenu/2` |  |  |  |
| 140033 | `controller_chat_radial_menu_option_3` | string | UserLocal | `SteamInput/ChatRadialMenu/3` |  |  |  |
| 140034 | `controller_chat_radial_menu_option_4` | string | UserLocal | `SteamInput/ChatRadialMenu/4` |  |  |  |
| 140035 | `controller_chat_radial_menu_option_5` | string | UserLocal | `SteamInput/ChatRadialMenu/5` |  |  |  |
| 140036 | `controller_chat_radial_menu_option_6` | string | UserLocal | `SteamInput/ChatRadialMenu/6` |  |  |  |
| 140037 | `controller_chat_radial_menu_option_7` | string | UserLocal | `SteamInput/ChatRadialMenu/7` |  |  |  |
| 16000 | `startup_movie_id` | uint64 | Install | `Customization/StartupMovie/MovieID` |  | pre-login |  |
| 16001 | `startup_movie_local_path` | string | Install | `Customization/StartupMovie/LocalPath` |  | pre-login |  |
| 16002 | `startup_movie_shuffle` | bool | Install | `Customization/StartupMovie/Shuffle` |  | pre-login |  |
| 16003 | `startup_movie_used_for_resume` | bool | UserLocal | `Customization/StartupMovie/UsedForResume` |  |  |  |
| 16004 | `screensaver_current_id` | string | Install | `Customization/Screensaver/CurrentScreensaver` |  |  |  |
| 16005 | `screensaver_settings` | string | Install | `Customization/Screensaver/Settings` |  |  |  |
| 16006 | `screensaver_while_ingame` | bool | Install | `Customization/Screensaver/WhileInGame` | `true` |  |  |
| 17001 | `game_notes_enable_spellcheck` | bool | UserRoaming | `GameNotesEnableSpellcheck` | `true` |  |  |
| 18000 | `screenshot_items_per_row` | int32 | UserRoaming | `ScreenshotViewItemsPerRow` | `1` |  |  |
| 18201 | `gamerecording_background_path` | string | CustomFunc |  |  |  |  |
| 18202 | `gamerecording_background_max_keep` | string | UserLocal | `GameRecording\BackgroundMaxKeep` | `'120min'` |  |  |
| 18203 | `gamerecording_background_time_resolution` | int32 | UserLocal | `GameRecording\BackgroundTimeResolution` | `6e+04` |  |  |
| 18207 | `gamerecording_background_mk` | CMsgHotkey | UserLocal | `GameRecording\MarkerKey` | `'Ctrl\tKEY_F12'` |  |  |
| 18208 | `gamerecording_background_tg` | CMsgHotkey | UserLocal | `GameRecording\ToggleKey` | `'Ctrl\tKEY_F11'` |  |  |
| 18209 | `gamerecording_background_a_m` | bool | UserLocal | `GameRecording\Audio_Mic` | `false` |  |  |
| 18210 | `gamerecording_video_bitrate` | string | UserLocal | `GameRecording\VideoBitRate` | `'preset_default'` |  |  |
| 18212 | `gamerecording_background_mode` | EGRMode | UserLocal | `GameRecording\BackgroundRecordMode` | `0` |  |  |
| 18213 | `gamerecording_background_audio` | EGRAudio | UserLocal | `GameRecording\Recording_Audio_Option` | `0` |  |  |
| 18214 | `gamerecording_max_fps` | int32 | UserLocal | `GameRecording\MaxFPS` | `60` | clamp [24..120] |  |
| 18215 | `gamerecording_hotkey_ic` | CMsgHotkey | UserLocal | `GameRecording\InstantClipKey` | `'None'` |  |  |
| 18216 | `gamerecording_ic_seconds` | float | UserLocal | `GameRecording\InstantClipDuration` | `3e+01` |  |  |
| 18217 | `gamerecording_export_limit_type` | EGRExportLimitType | UserLocal | `GameRecording\ExportLimitType` |  |  |  |
| 18218 | `gamerecording_export_limit_size_mb` | int32 | UserLocal | `GameRecording\ExportLimitSize` | `100` |  |  |
| 18219 | `gamerecording_export_limit_bitrate` | int32 | UserLocal | `GameRecording\ExportLimitBitrate` | `1` |  |  |
| 18220 | `gamerecording_export_limit_width` | int32 | UserLocal | `GameRecording\ExportLimitWidth` | `3840` |  |  |
| 18221 | `gamerecording_export_limit_height` | int32 | UserLocal | `GameRecording\ExportLimitHeight` | `2160` |  |  |
| 18222 | `gamerecording_export_limit_frame_rate` | int32 | UserLocal | `GameRecording\ExportLimitFrameRate` | `60` |  |  |
| 18223 | `gamerecording_export_directory` | string | CustomFunc | `GameRecording\ExportDirectory` |  |  |  |
| 18224 | `gamerecording_export_codec` | EExportCodec | UserLocal | `GameRecording\ExportCodec` |  |  |  |
| 18225 | `gamerecording_video_maxheight` | int32 | UserLocal | `GameRecording\VideoMaxHeight` | `0` | clamp [0..2160] |  |
| 18226 | `gamerecording_force_mic_mono` | bool | UserLocal | `GameRecording\ForceMicMono` | `false` |  |  |
| 18227 | `gamerecording_automatic_gain_control` | bool | UserLocal | `GameRecording\AutomaticGainControl` | `true` |  |  |
| 20000 | `show_timestamps_in_console` | bool | UserLocal | `Developer\ShowTimestampsInConsole` |  |  |  |
| 20002 | `override_browser_composer_mode` | int32 | CustomFunc |  |  |  |  |
| 20003 | `cef_remote_debugging_enabled` | bool | CustomFunc |  |  |  |  |
| 20004 | `force_deck_perf_tab` | bool | Install | `Developer/ForceDeckPerfTab` |  |  |  |
| 20005 | `force_fake_mandatory_update` | bool | Install | `Developer/FakeMandatoryUpdate` |  |  |  |
| 20006 | `hdr_compat_testing` | bool | Install | `Developer/HDRCompatTesting` |  |  |  |
| 20007 | `developer_mode_enabled` | bool | Install | `Developer/DevModeEnabled` |  |  |  |
| 20008 | `show_advanced_update_channels` | bool | Install | `Developer/ShowAdvancedUpdateChannels` |  |  |  |
| 20009 | `browserview_underlays_allowed` | bool | CustomFunc |  |  |  |  |
| 21001 | `gamescope_hdr_visualization` | EHDRVisualization | UserLocal | `Gamescope/HDRVisualization2` |  |  |  |
| 21002 | `gamescope_app_target_framerate` | int32 | UserLocal | `Gamescope/AppTargetFrameRate` | `0` | per-game+display |  |
| 21003 | `gamescope_enable_app_target_framerate` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\GamescopeEnableAppTargetRefreshRate2` | `true` |  |  |
| 21004 | `gamescope_disable_framelimit` | bool | UserLocal | `Gamescope/DisableFrameLimit` | `false` | per-game+display |  |
| 21005 | `gamescope_display_refresh_rate` | int32 | UserLocal | `Gamescope/RefreshRate` | `0` | per-game+display |  |
| 21006 | `gamescope_use_game_refresh_rate_in_steam` | bool | UserLocal | `Developer/DynamicRefreshRateInSteam` | `true` |  |  |
| 21007 | `gamescope_disable_mura_correction` | bool | UserLocal | `Gamescope/MuraCorrectionDisabled` | `false` |  |  |
| 21008 | `gamescope_include_steamui_in_screenshots` | bool | UserLocal | `Gamescope/IncludeSteamUIInScreenshots` | `false` |  |  |
| 21009 | `gamescope_allow_tearing` | bool | UserLocal | `Gamescope/AllowTearing` | `false` | per-game |  |
| 21010 | `gamescope_composite_debug` | bool | UserLocal | `Gamescope/CompositeDebug` | `false` |  |  |
| 21011 | `gamescope_force_composite` | bool | UserLocal | `Gamescope/ForceComposite` | `false` |  |  |
| 21012 | `gamescope_game_resolution_global` | string | UserLocal | `Gamescope/GameResolutionGlobal` | `'Default'` |  |  |
| 21013 | `gamescope_guide_hotkey` | CMsgHotkey | UserLocal | `Gamescope/GuideKeyboardHotkey` | `'Shift\tKEY_TAB'` |  |  |
| 21014 | `gamescope_qam_hotkey` | CMsgHotkey | UserLocal | `Gamescope/QAMKeyboardHotkey` | `'CTRL\tShift\tKEY_TAB'` |  |  |
| 21015 | `gamescope_hdr_enabled` | bool | Install | `Gamescope/HDREnabled` | `true` | per-display |  |
| 21016 | `gamescope_native_external_res_in_steam` | bool | Install | `Gamescope/EnableSteamNativeExternalResolution` |  |  |  |
| 22000 | `steamos_status_led_brightness` | int32 | UserLocal | `SteamOS/StatusLEDBrightness` | `100` |  |  |
| 22001 | `steamos_tdp_limit_enabled` | bool | Install | `SteamOS/TDPLimitEnabled` | `false` | per-game |  |
| 22002 | `steamos_tdp_limit` | int32 | Install | `SteamOS/TDPLimit` | `0` | per-game |  |
| 22003 | `steamos_cec_enabled` | bool | Install | `SteamOS/CECEnabled` | `true` |  |  |
| 22004 | `steamos_cec_wake_on_resume` | bool | Install | `SteamOS/WakeOnResume` | `true` |  |  |
| 22005 | `steamos_wifi_debug` | bool | Install | `SteamOS/WifiDebug` | `false` |  |  |
| 22006 | `steamos_wifi_force_wpa_supplicant` | bool | Install | `SteamOS/WifiForceWPASupplicant` | `false` |  |  |
| 22007 | `steamos_magnifier_scale` | int32 | UserLocal | `SteamOS/MagnifierScale` | `150` |  |  |
| 22008 | `steamos_manual_gpu_clock_enabled` | bool | Install | `SteamOS/ManualGPUClockEnabled` | `false` | per-game |  |
| 22009 | `steamos_manual_gpu_clock_hz` | int32 | Install | `SteamOS/ManualGPUClockHz` | `1000` | per-game |  |
| 22010 | `steamos_platform_performance_profile` | string | Install | `SteamOS/PerformanceProfile` |  | per-game |  |
| 22011 | `steamos_charge_limit_enabled` | bool | Install | `SteamOS/ChargeLimitEnabled` | `false` |  |  |
| 22012 | `steamos_charge_limit` | int32 | Install | `SteamOS/ChargeLimit` | `80` |  |  |
| 22013 | `steamos_charge_limit_devmode` | bool | Install | `SteamOS/ChargeLimitDevMode` | `false` |  |  |
| 22014 | `steamos_system_tracing_enabled` | bool | UserLocal | `SteamOS/SystemTracingEnabled` | `false` | per-game |  |
| 22015 | `steamos_vrs_enabled` | bool | UserLocal | `SteamOS/VRSEnabled` | `false` | per-game |  |
| 22016 | `steamos_separate_led_colors` | bool | UserLocal | `SteamOS/SeparaeLEDColors` | `false` |  |  |
| 22017 | `steamos_wifi_reload_wifi_driver_on_sleep` | bool | Install | `SteamOS/WifiReloadDriverOnSleep` | `false` |  |  |
| 220018 | `steamos_wifi_power_management_enabled` | bool | Install | `SteamOS/WifiPowerManagement` | `true` |  |  |
| 22019 | `steamos_cec_control` | bool | Install | `SteamOS/CECControl` | `true` |  |  |
| 22020 | `steamos_cec_suspend_tv` | bool | Install | `SteamOS/CECSuspendTV` | `true` |  |  |
| 22021 | `steamos_cec_suspend_device` | bool | Install | `SteamOS/CECSuspendDevice` | `true` |  |  |
| 22022 | `steamos_cec_wake_tv` | bool | Install | `SteamOS/CECWakeTV` | `true` |  |  |
| 22023 | `steamos_cec_wake_device` | bool | Install | `SteamOS/CECWakeDevice` | `true` |  |  |
| 22024 | `steamos_ec_logging_enabled` | bool | Install | `SteamOS/ECLoggingEnabled` | `false` |  |  |
| 23001 | `setting_validation_bool` | bool | Install | `SettingValidation/DummyBool` |  |  |  |
| 23002 | `setting_validation_enum` | EHDRVisualization | Install | `SettingValidation/DummyEnum` |  |  |  |
| 23003 | `setting_validation_int32` | int32 | Install | `SettingValidation/DummyInt32` |  |  |  |
| 23004 | `setting_validation_uint32` | uint32 | Install | `SettingValidation/DummyUInt32` |  |  |  |
| 23005 | `setting_validation_uint64` | uint64 | Install | `SettingValidation/DummyUInt64` |  |  |  |
| 23006 | `setting_validation_float` | float | Install | `SettingValidation/DummyFloat` |  |  |  |
| 23007 | `setting_validation_string` | string | Install | `SettingValidation/DummyString` |  |  |  |
| 23008 | `setting_validation_hotkey` | CMsgHotkey | Install | `SettingValidation/DummyHotkey` |  |  |  |
| 24000 | `system_bluetooth_enabled` | bool | Install | `System/Bluetooth/Enabled` | `false` |  |  |
| 24001 | `hardware_updater_enabled` | bool | Install | `System/HardwareUpdater/Enabled` | `false` |  |  |
| 24003 | `system_idle_suspend_battery_sec` | int32 | Install | `Software\Valve\Steam\System\IdleSuspendBatterySeconds` | `900` |  |  |
| 24004 | `system_idle_suspend_ac_sec` | int32 | Install | `Software\Valve\Steam\System\IdleSuspendACSeconds` | `3600` |  |  |
| 24005 | `system_enable_low_power_downloads` | bool | Install | `Software\Valve\Steam\System\EnableLowPowerDownloads` | `true` |  |  |
| 24006 | `system_allow_battery_low_power_downloads` | bool | Install | `Software\Valve\Steam\System\AllowBatteryLowPowerDownloads` | `false` |  |  |
| 24008 | `system_idle_screensaver_battery_sec` | int32 | Install | `Software\Valve\Steam\System\IdleScreensaverBatterySeconds` | `0` |  |  |
| 24009 | `system_idle_screensaver_ac_sec` | int32 | Install | `Software\Valve\Steam\System\IdleScreensaverACSeconds` | `300` |  |  |
| 25000 | `vr_show_perf_graph_in_hmd` | bool | UserLocal | `VR/ShowPerfGraphInHMD` | `false` |  |  |
| 26000 | `accessibility_debug_visualizer` | bool | UserLocal | `Accessibility/DebugVisualizer` | `false` |  |  |
| 26001 | `accessibility_screen_reader_enabled` | bool | Install | `Accessibility/ScreenReaderEnabled` | `false` |  |  |
| 26002 | `accessibility_screen_reader_rate` | float | UserLocal | `Accessibility/ScreenReaderPitch` | `0.5` |  |  |
| 26003 | `accessibility_screen_reader_pitch` | float | UserLocal | `Accessibility/ScreenReaderRate` | `0.5` |  |  |
| 26004 | `accessibility_screen_reader_volume` | float | UserLocal | `Accessibility/ScreenReaderVolume` | `1` |  |  |
| 26005 | `accessibility_high_contrast_mode` | bool | UserLocal | `Accessibility/HighContrastMode` | `false` |  |  |
| 26006 | `accessibility_reduce_motion` | bool | UserLocal | `Accessibility/ReduceMotion` | `false` |  |  |
| 26008 | `accessibility_minimum_font_size` | uint32 | UserLocal | `Accessibility/MinimumFontSize` | `0` |  |  |
| 26009 | `accessibility_color_filter_name` | string | Install | `Accessibility/ColorFilterName` | `''` |  |  |
| 26010 | `accessibility_desktop_ui_scale` | float | Install | `Accessibility/DesktopUIScale` | `1` |  |  |
| 26011 | `accessibility_screen_reader_locale` | string | Install | `Accessibility/ScreenReaderLocale` | `'auto'` |  |  |
| 26012 | `accessibility_mono_audio` | bool | Install | `Accessibility/MonoAudio` | `false` |  |  |
| 27000 | `remote_play_wifi_ap_enabled` | bool | Install | `streaming_v2\WifiAPEnabled` | `true` |  |  |
| 27001 | `remote_play_wifi_ap_channel_5ghz` | int32 | Install | `streaming_v2\WifiAPChannel5GHz` | `0` |  |  |
| 27002 | `remote_play_wifi_ap_channel_6ghz` | int32 | Install | `streaming_v2\WifiAPChannel6GHz` | `0` |  |  |
| 27003 | `remote_play_wifi_ap_channel_width` | int32 | Install | `streaming_v2\WifiAPChannelWidth` | `0` |  |  |
| 27004 | `remote_play_wifi_ap_hotspot_mode` | bool | Install | `streaming_v2\WifiAPHotspotMode` | `false` |  |  |
| 27005 | `remote_play_wifi_ap_hotspot_ssid` | string | Install | `streaming_v2\WifiAPHotspotSSID` | `''` |  |  |
| 27006 | `remote_play_wifi_ap_hotspot_password` | string | Install | `streaming_v2\WifiAPHotspotPassword` | `''` |  |  |
| 27007 | `remote_play_wifi_ap_hotspot_routing` | string | Install | `streaming_v2\WifiAPHotspotRouting` | `'noroute'` |  |  |
| 27008 | `remote_play_wifi_ap_show_advanced` | bool | UserLocal | `streaming_v2/WifiAPShowAdvanced` | `false` |  |  |
| 27009 | `remote_play_wifi_ap_paired_ssid` | string | Install | `streaming_v2\WifiAPPairedSSID` | `''` |  |  |
| 27010 | `skip_steamframe_pairing_dialog` | bool | UserLocal | `system\SteamFrameWirelessAdapterPairingDialog` |  |  |  |
| 27011 | `skip_steamframe_troubleshooting_dialog` | bool | UserLocal | `system\SteamFrameWirelessAdapterTroubleshootingDialogSkip` |  |  |  |
| 27012 | `skip_steamframe_airplane_dialog` | bool | UserLocal | `system\SteamFrameWirelessAdapterAirplaneDialogSkip` |  |  |  |
| 28001 | `oobe_completed` | bool | CustomFunc |  |  | pre-login | True if OOBE stage 1 has completed or we're on a platform where we don't do OOBE |
| 28002 | `oobe_test_mode_enabled` | bool | CustomFunc |  |  | pre-login, read-only | OOBE test mode is enabled either by passing -testoobe on the command line or setting the force_oobe client setting |
| 28003 | `force_oobe` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\ForceOOBE` |  | pre-login |  |
| 28004 | `oobe_stage_2_completed` | bool | CustomFunc |  |  | pre-login | True if OOBE stage 2 has completed or we're on a platform where we don't do OOBE |
| 28005 | `oobe_stage_2_test_mode_enabled` | bool | CustomFunc |  |  | pre-login, read-only | OOBE test mode is enabled for stage 2 either by passing -testoobe on the command line or setting the force_stage2_oobe client setting |
| 28006 | `force_stage_2_oobe` | bool | Registry | `HKEY_CURRENT_USER\Software\Valve\Steam\ForceOOBEStage2` |  | pre-login |  |
| 29000 | `compat_show_all_tools` | bool | UserLocal | `Compatibility/ShowAllTools` | `false` |  |  |

## Enum types used by settings

### `EBroadcastEncoderSetting`

| Value | Name |
|---|---|
| 0 | `k_EBroadcastEncoderBestQuality` |
| 1 | `k_EBroadcastEncoderBestPerformance` |

### `EBroadcastPermission`

| Value | Name |
|---|---|
| 0 | `k_EBroadcastPermissionDisabled` |
| 1 | `k_EBroadcastPermissionFriendsApprove` |
| 2 | `k_EBroadcastPermissionFriendsAllowed` |
| 3 | `k_EBroadcastPermissionPublic` |
| 4 | `k_EBroadcastPermissionSubscribers` |

### `EExportCodec`

| Value | Name |
|---|---|
| 0 | `k_EExportCodec_Default` |
| 1 | `k_EExportCodec_H264` |
| 2 | `k_EExportCodec_H265` |

### `EGRAudio`

| Value | Name |
|---|---|
| 0 | `k_EGRAudio_Game` |
| 1 | `k_EGRAudio_System` |
| 2 | `k_EGRAudio_Select` |

### `EGRExportLimitType`

| Value | Name |
|---|---|
| 0 | `k_EGRExportLimitType_Native` |
| 1 | `k_EGRExportLimitType_FileSize` |
| 2 | `k_EGRExportLimitType_Advanced` |

### `EGRMode`

| Value | Name |
|---|---|
| 0 | `k_EGRMode_Never` |
| 1 | `k_EGRMode_Always` |
| 2 | `k_EGRMode_Manual` |

### `EHDRVisualization`

| Value | Name |
|---|---|
| 0 | `k_EHDRVisualization_None` |
| 1 | `k_EHDRVisualization_Heatmap` |
| 2 | `k_EHDRVisualization_Analysis` |
| 3 | `k_EHDRVisualization_HeatmapExtended` |
| 4 | `k_EHDRVisualization_HeatmapClassic` |

