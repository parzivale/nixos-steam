# steamui: client settings read and written by the JS UI

Source: `root/steamui/*.js` from the Linux client, manifest 1791918634. Almost all of it is in `sp.js` (16 MB, the main SharedJSContext bundle) and `library.js`. English labels come from `root/steamui/localization/*_english-json.js`.

## How settings flow between the C++ client and the JS UI

The settings store is webpack module `39828` in `sp.js`. It is exported as `window.settingsStore`.

| Mechanism | Direction | Notes |
|---|---|---|
| `SteamClient.Settings.RegisterForSettingsArrayChanges(cb)` | client -> JS | `cb` receives a serialized **`CMsgClientSettings`** protobuf. It is decoded with `deserializeBinary().toObject()` and merged into `settingsStore.clientSettings` (snake_case field names). |
| `SteamClient.Settings.SetSetting(base64)` | JS -> client | The JS builds a `CMsgClientSettings` that contains only the one changed field, serializes it and base64-encodes it. Every toggle, slider and dropdown that declares `setting:"<field>"` goes through this path. |
| `SteamClient.Settings.RegisterForSettingsChanges(cb)` | client -> JS | Older settings object with Hungarian-notation names (`bIsValveEmail`, `flCurrentDisplayScaleFactor`, ...). Stored as `settingsStore.settings`. See "Legacy settings object" below. |
| Hooks in module 39828 | — | `VI(name)` returns `[value, setter, isDeferred, setDeferred]`. `hX(name)` is read-only. `qt(name, value)` is a direct setter. `rV.GetClientSetting(name)` serves class components. `e_(name)` is for friend settings, `I5(name)` for community preferences, `sE(type)` for notification preferences. |
| Settings UI components | — | Toggles, sliders and dropdowns take a `setting:"<field>"` prop, plus `label`, `description`, `feature` (a Family View / parental feature gate) and `bRequiresRestart`. |

The table below lists every field of the `CMsgClientSettings` message definition embedded in `sp.js`. Column meanings:

- **Field number and type** come straight from the embedded protobuf descriptor.
- **Label** is the localization key of the UI control bound to the field, with its English text.
- **UI section** is inferred, mostly from the localization key prefix or the settings page that contains the control.
- **JS access** shows how the UI reaches the field: `setting-prop` means a generic settings control, `VI`, `hX` and `qt` are the hooks, and `GetClientSetting` is the class-component accessor.
- Notes marked "inf:" are guesses based on the field name only.

Defaults are not visible in JS. The proto descriptor carries no default values, so the defaults come from the C++ client.

## CMsgClientSettings fields (270)

| # | Field | Type | UI section (inferred) | UI label / description (English loc) | Notes | JS access | Flags |
|---|---|---|---|---|---|---|---|
| 1 | `no_save_personal_info` | Bool | — |  | inf: do not persist personal info on this machine (only referenced by the proto definition) | — |  |
| 5 | `preferred_monitor` | String | Display > Preferred monitor (via SteamClient.Settings.SetPreferredMonitor) |  | Written through a dedicated API, not SetSetting | — | no JS reference besides proto |
| 6 | `steam_cef_gpu_blocklist_disabled` | Bool | Interface (advanced) | `#Settings_CEFDisableGPUBlocklist`: Disable GPU Blocklist |  | setting-prop | requires restart |
| 7 | `bigpicture_windowed` | Bool | Display > Big Picture windowed (SteamClient.Settings.SetWindowed) |  | Written through dedicated API; mirrored in legacy settings | — | no JS reference besides proto |
| 8 | `display_name` | String | — |  | Display name of current monitor (read via legacy settings object strDisplayName) | — |  |
| 9 | `is_external_display` | Bool | — |  | Read-only state; JS reads legacy bDisplayIsExternal | — | no JS reference besides proto |
| 10 | `steam_os_underscan_level` | Float | Display > Underscan |  | JS reads legacy flCurrentUnderscanLevel | — | no JS reference besides proto |
| 11 | `steam_os_underscan_enabled` | Bool | Display > Underscan |  | JS reads legacy bUnderscanEnabled | — | no JS reference besides proto |
| 12 | `min_scale_factor` | Float | Display > Scaling |  | JS reads legacy flMinDisplayScaleFactor | — | no JS reference besides proto |
| 13 | `max_scale_factor` | Float | Display > Scaling |  | JS reads legacy flMaxDisplayScaleFactor | — | no JS reference besides proto |
| 14 | `auto_scale_factor` | Float | Display > Scaling |  | JS reads legacy flAutoDisplayScaleFactor | — | no JS reference besides proto |
| 16 | `small_mode` | Bool | Library (View > Small Mode) |  | Desktop small-mode library | GetClientSetting,VI |  |
| 19 | `skip_steamvr_install_dialog` | Bool | Dialog suppression | `#SteamVRInstall_DontShowAgain`: Don't Show this dialog again | #SteamVRInstall_DontShowAgain | VI |  |
| 20 | `always_show_user_chooser` | Bool | Interface | `#ChangeUser_ShouldShowUserChooser`: Ask which account to use each time Steam starts |  | setting-prop,VI |  |
| 21 | `os_version_unsupported` | Bool | — |  | inf: client flags OS as unsupported; no JS reference | — | no JS reference besides proto |
| 3000 | `show_family_sharing_notifications` | Bool | — |  | inf: no JS reference in this build | — | no JS reference besides proto |
| 3001 | `show_copy_count_in_library` | Bool | Library | `#Settings_Library_Show_Copy_Count`: Show number of copies in Steam Family library |  | setting-prop,VI |  |
| 4000 | `overlay_fps_counter_corner` | Int32 | In Game | `#Settings_InGame_PerformanceMonitor`: Show performance monitor |  | setting-prop,VI |  |
| 4001 | `overlay_fps_counter_high_contrast` | Bool | QAM Performance > FPS high contrast |  | Label #QuickAccess_Tab_Perf_FPS_Contrast (FPS High Contrast) | VI |  |
| 4002 | `overlay_key` | CMsgHotkey (message) | In Game | `#Settings_InGame_Overlay`: The Steam Overlay |  | VI |  |
| 4003 | `screenshot_key` | CMsgHotkey (message) | In Game > Screenshot hotkey (CMsgHotkey) |  |  | VI |  |
| 4004 | `enable_overlay` | Bool | In Game | `#Settings_InGame_EnableOverlay`: Enable the Steam Overlay while in-game |  | setting-prop,VI |  |
| 4006 | `enable_screenshot_notification` | Bool | In Game | `#Settings_InGame_ScreenshotNotify`: When a screenshot is taken, display a notification |  | setting-prop |  |
| 4007 | `enable_screenshot_sound` | Bool | In Game | `#Settings_InGame_ScreenshotSound`: When a screenshot is taken, play a sound |  | setting-prop |  |
| 4008 | `save_uncompressed_screenshots` | Bool | In Game | `#Settings_InGame_ScreenshotUncompressed`: Save an external copy of my screenshots |  | setting-prop,VI |  |
| 4009 | `screenshots_path` | String | In Game | `#Settings_InGame_Screenshots`: Screenshots |  | VI |  |
| 4010 | `default_ping_rate` | Int32 | In Game > Server browser pings (read-only hook) | `#ServerPing_Auto`: Automatic (%1$s) |  | hX |  |
| 4011 | `server_ping_rate` | Int32 | In Game | `#Settings_InGame_ServerBrowserPings`: Server browser pings/minute<br>desc: Connection problems while browsing game servers? Try lowering this value. |  | setting-prop |  |
| 4012 | `steam_networking_share_ip` | Int32 | In Game | `#Settings_InGame_SteamNetworking`: Steam Networking<br>desc: Allow games using <1>Steam Networking</1> to share my IP address for a faster connection |  | setting-prop |  |
| 4013 | `web_browser_home` | String | In Game | `#Settings_InGame_WebBrowserHome`: Web browser home page |  | setting-prop,VI |  |
| 4014 | `voice_mic_device_name` | String | In Game | `#Settings_InGame_Voice_MicDeviceName`: Current Mic Name | #Settings_InGame_Voice_MicDeviceName | VI |  |
| 4015 | `voice_mic_input_gain` | Float | In-Game Voice | `#VoiceInputGain`: Input volume/gain | #VoiceInputGain | VI |  |
| 4016 | `voice_speaker_output_gain` | Float | In-Game Voice | `#VoiceOutputGain`: Output volume/gain | #VoiceOutputGain | VI |  |
| 4017 | `voice_push_to_talk_setting` | Int32 | — |  | inf: in-game voice push-to-talk mode; no JS reference found | — | no JS reference besides proto |
| 4018 | `voice_push_to_talk_key` | CMsgHotkey (message) | — |  | inf: in-game voice push-to-talk hotkey; no JS reference found | — | no JS reference besides proto |
| 4019 | `overlay_toolbar_list_view` | Bool | In Game | `#Settings_InGame_Overlay_ToolBar_ListView`: Show toolbar as list view |  | setting-prop,GetClientSetting,VI |  |
| 4020 | `always_use_gamepadui_overlay` | Bool | In Game | `#Settings_InGame_UseGamepadOverlay`: Use the Big Picture Overlay when using a controller |  | setting-prop,GetClientSetting |  |
| 4021 | `overlay_tabs` | String | In-game overlay toolbar |  | JSON string array of {window, visible} entries describing overlay toolbar tabs | VI |  |
| 4022 | `overlay_scale_interface` | Bool | In Game | `#Settings_InGame_ScaleInterface`: Scale Steam Overlay text and icons to match monitor settings |  | setting-prop |  |
| 4023 | `overlay_restore_browser_tabs` | Bool | In Game | `#Settings_InGame_Overlay_Restore_Browser_Tabs`: Restore my previous browser tabs when starting a game |  | setting-prop |  |
| 4024 | `enable_avif_screenshots` | Bool | In Game | `#Settings_InGame_ScreenshotUncompressedAVIF`: Save external HDR screenshots as AVIF |  | setting-prop |  |
| 4025 | `overlay_fps_counter_detail_level` | Int32 | In Game | `#Settings_InGame_PerfOverlayDetailLevel`: Performance detail level |  | setting-prop,VI |  |
| 4026 | `overlay_fps_counter_saturation_factor` | Float | In Game | `#Settings_InGame_PerfOverlay_Saturation`: Text contrast/saturation |  | setting-prop |  |
| 4027 | `overlay_fps_counter_bgopacity` | Float | In Game | `#Settings_InGame_PerfOverlay_BGOpacity`: Background opacity |  | setting-prop |  |
| 4028 | `overlay_fps_counter_scale_factor` | Float | In Game | `#Settings_InGame_PerfOverlay_TextSize`: Text size scaling |  | setting-prop |  |
| 4029 | `overlay_fps_counter_key` | CMsgHotkey (message) | In Game | `#Settings_InGame_Overlay_PerformanceMonitor`: Overlay Performance Monitor |  | VI |  |
| 4030 | `overlay_fps_counter_fps_graph` | Bool | In Game | `#Settings_InGame_PerfOverlayShowFPSGraph`: Show FPS Avg/Min Graph |  | setting-prop |  |
| 4031 | `overlay_fps_counter_cpu_graph` | Bool | In Game | `#Settings_InGame_PerfOverlayShowCPUGraph`: Show CPU Utilization Per-Core Graph |  | setting-prop |  |
| 4032 | `overlay_fps_counter_allow_km_driver` | Bool | In Game | `#Settings_InGame_PerfOverlayAllowKMDriver`: Enable kernel driver based metrics (CPU Temperature) |  | setting-prop |  |
| 4033 | `achievement_notification_toast` | Bool | Notifications |  | #NotificationsSettings_Notification_UnlockAchievement (toast) | — |  |
| 4034 | `achievement_notification_sound` | Bool | Notifications |  | #NotificationsSettings_Notification_UnlockAchievement (sound) | — |  |
| 4035 | `controllerconnect_notification_toast` | Bool | Notifications |  | #NotificationsSettings_Notification_ControllerConnect (toast) | — |  |
| 4036 | `controllerconnect_notification_sound` | Bool | Notifications |  | #NotificationsSettings_Notification_ControllerConnect (sound) | — |  |
| 4037 | `controller_low_battery_notification_toast` | Bool | Notifications |  | #NotificationsSettings_Notification_ControllerLowBattery (toast) | — |  |
| 4038 | `controller_low_battery_notification_sound` | Bool | Notifications |  | #NotificationsSettings_Notification_ControllerLowBattery (sound) | — |  |
| 4039 | `logged_in_as_user_notification_toast` | Bool | Notifications |  | #NotificationsSettings_Notification_LoggedInAsUser (toast) | — |  |
| 4040 | `logged_in_as_user_notification_sound` | Bool | Notifications |  | #NotificationsSettings_Notification_LoggedInAsUser (sound) | — |  |
| 5000 | `smooth_scroll_webviews` | Bool | Interface | `#Settings_Interface_EnableSmoothScrolling`: Enable smooth scrolling in web views (requires restart) |  | setting-prop | requires restart |
| 5001 | `enable_gpu_accelerated_webviews` | Bool | Interface | `#Settings_Interface_EnableGPURendering`: Enable GPU accelerated rendering in web views (requires restart) |  | setting-prop,VI | requires restart |
| 5003 | `enable_hardware_video_decoding` | Bool | Interface | `#Settings_Interface_EnableHardwareDecoding`: Enable hardware video decoding, if supported (requires restart) |  | setting-prop,VI | requires restart |
| 5004 | `run_at_startup` | Bool | Interface | `#Settings_Interface_RunAtStartup`: Run Steam when my computer starts |  | setting-prop |  |
| 5005 | `enable_dpi_scaling` | Bool | Interface | `#Settings_Interface_ScaleText`: Scale text and icons to match monitor settings (requires restart) |  | setting-prop | requires restart |
| 5006 | `enable_marketing_messages` | Bool | Interface | `#Settings_Interface_ShowMarketingMessages`: Notify me about additions or changes to my games, new releases, and upcoming releases |  | setting-prop |  |
| 5007 | `start_in_big_picture_mode` | Bool | Interface |  | #Settings_Interface_StartInBigPicture / _SteamOS | setting-prop |  |
| 5008 | `jumplist_flags` | Uint32 | Interface > Taskbar preferences (Windows) | `#TaskbarOptions_Online`: Task bar - Select player status options to display | #TaskbarOptions_*; bitmask | VI |  |
| 5009 | `enable_ui_sounds` | Bool | Audio | `#Audio_Setting_Enable_UI_Sounds`: Enable UI sounds |  | setting-prop |  |
| 5010 | `enable_gamescope_composer` | Bool | Developer | `#Settings_Developer_EnableGamescopeComposer`: Enable gamescope browser composer |  | setting-prop | requires restart |
| 5011 | `enable_gamescope_composer_vr` | Bool | Developer | `#Settings_Developer_EnableGamescopeVRComposer`: Enable gamescope VR browser composer |  | setting-prop | requires restart |
| 5012 | `show_switch_to_desktop_at_login` | Bool | Interface | `#Settings_Interface_ShowSwitchToDesktopAtLoginScreen`: Show Switch To Desktop option when not logged in |  | setting-prop,VI |  |
| 5013 | `enable_steamrt64_client` | Bool | Interface | `#Settings_Interface_SteamRTClient`: Use experimental SteamRT3 Steam Client |  | setting-prop | requires restart |
| 6000 | `disable_all_toasts` | Bool | Notifications | `#NotificationsSettings_ShowAlways`: Anytime | Show-notifications policy (Anytime / never ...) | VI |  |
| 6001 | `disable_toasts_in_game` | Bool | Notifications | `#NotificationsSettings_ShowAlways`: Anytime | Show-notifications policy while in game | VI |  |
| 6002 | `play_sound_on_toast` | Bool | Notifications | `#NotificationsSettings_PlaySoundOnToast`: Play a sound when a notification toast is displayed |  | setting-prop,VI |  |
| 7000 | `library_display_size` | Int32 | Library > #Settings_Library_DisplaySize |  |  | GetClientSetting,VI |  |
| 7001 | `library_whats_new_show_only_product_updates` | Bool | Home | `#HomeSettings_WhatsNewUpdatesOnly`: Only show product updates in What's New | #HomeSettings_WhatsNewUpdatesOnly | setting-prop,GetClientSetting |  |
| 7002 | `show_store_content_on_home` | Bool | Home | `#HomeSettings_ShowStoreContent`: Show personalized store content on my Home |  | setting-prop,VI |  |
| 7003 | `start_page` | String | Interface | `#Settings_Interface_StartPage`: Start Up Location<br>desc: Select your default Steam window |  | setting-prop,GetClientSetting,VI |  |
| 7004 | `library_low_bandwidth_mode` | Bool | Library | `#Settings_Library_LowBandwidthMode`: Low Bandwidth Mode<br>desc: Reduces bandwidth use by disabling features like auto-load of community content |  | setting-prop,GetClientSetting,VI |  |
| 7005 | `library_low_perf_mode` | Bool | Library | `#Settings_Library_LowPerfMode`: Low Performance Mode<br>desc: Improves library performance by disabling certain graphical improvements and transitions |  | setting-prop,GetClientSetting |  |
| 7006 | `library_disable_community_content` | Bool | Library | `#Settings_Library_DisableCommunityContent`: Disable Community Content<br>desc: Prevents the automatic load of community content when viewing game details |  | setting-prop,GetClientSetting |  |
| 7007 | `library_display_icon_in_game_list` | Bool | Library | `#Settings_Library_ShowGameIcons`: Show game icons in the left column |  | setting-prop,VI |  |
| 7008 | `ready_to_play_includes_streaming` | Bool | Library | `#Settings_Library_ReadyToPlayIncludesStreaming`: Ready to Play should include streamable games<br>desc: Should the library include streamable games that aren't installed locally in Ready to Play and also show streaming by default for those games? |  | setting-prop,GetClientSetting,VI |  |
| 7009 | `show_steam_deck_info` | Bool | Library | `#Settings_Library_Show_SteamDeck_Info`: Show Steam Deck compatibility information in library |  | setting-prop,VI |  |
| 7010 | `library_home_big_art` | Bool | Customization | `#Settings_Customization_HomeScreen_BigArt`: Big Art Mode<br>desc: Turns on an alternate layout for the home screen that highlights background art for the selected title in Recent Games. |  | setting-prop,VI |  |
| 8000 | `enable_shader_precache` | Bool | Downloads | `#DownloadSettings_PreShaderEnable`: Enable Shader Pre-caching (%1$s MB pre-cached)<br>desc: If enabled, Steam will collect shaders from your system when needed. Enabling this feature may slightly increase disk and bandwidth usage. |  | setting-prop,VI |  |
| 8001 | `enable_shader_background_processing` | Bool | Downloads | `#DownloadSettings_PreShaderBackgroundProcessing`: Allow background processing of Vulkan shaders |  | setting-prop |  |
| 8002 | `shader_precached_size` | Uint64String | Downloads | `#DownloadSettings_PreShaderEnable`: Enable Shader Pre-caching (%1$s MB pre-cached) |  | hX |  |
| 8003 | `needs_steam_service_repair` | Bool | — |  | inf: Windows Steam Service repair flag; no JS reference | — | no JS reference besides proto |
| 8004 | `download_peer_content` | Int32 | Downloads | `#DownloadSettings_PeerContentSameUser`: Only me | #DownloadSettings_PeerContent* (enum: off/only me/friends/anyone - inferred) | VI |  |
| 8005 | `download_rate_bits_per_s` | Bool | Downloads | `#DownloadSettings_DisplayInBitsPerSecond`: Display download rates in bits per second |  | setting-prop,GetClientSetting,VI |  |
| 8006 | `restrict_auto_updates` | Bool | Downloads | `#DownloadSettings_ScheduleAutoUpdates`: Schedule auto-updates |  | setting-prop,VI |  |
| 8007 | `restrict_auto_updates_start` | Int32 | Downloads | `#DownloadSettings_ScheduleAutoUpdates`: Schedule auto-updates | Start hour | VI |  |
| 8008 | `restrict_auto_updates_end` | Int32 | Downloads | `#DownloadSettings_ScheduleAutoUpdates`: Schedule auto-updates | End hour | VI |  |
| 8009 | `download_region` | Int32 | Downloads | `#DownloadSettings_SelectRegion`: Download region |  | setting-prop |  |
| 8010 | `download_while_app_running` | Bool | Downloads | `#DownloadSettings_AllowDownloadDuringGameplay`: Allow downloads during gameplay |  | setting-prop,VI |  |
| 8011 | `download_throttle_while_streaming` | Bool | Downloads | `#DownloadSettings_ThrottleDuringStreaming`: Throttle downloads while streaming<br>desc: If this is enabled, Steam will limit download speed to maintain a high quality Steam Remote Play experience. |  | setting-prop |  |
| 8012 | `download_throttle_rate` | Int32 | Downloads | `#DownloadSettings_BandwidthLimit`: Limit download speed |  | VI |  |
| 8013 | `default_app_update_behavior` | Int32 | Interface/In Game | `#AppProperties_AutoUpdateSection`: Automatic Updates | Default automatic update behavior | GetClientSetting,VI |  |
| 10000 | `cloud_enabled` | Bool | Cloud | `#CloudSettings_CloudEnabled`: Enable Steam Cloud<br>desc: Enable Steam Cloud synchronization for applications which support it |  | setting-prop,VI |  |
| 10001 | `show_screenshot_manager` | Bool | Cloud | `#CloudSettings_ShowScreenshotManager`: Screenshot Management<br>desc: Open the Screenshot Manager after closing a game if screenshots were taken |  | setting-prop |  |
| 11000 | `music_volume` | Int32 | Music | `#Settings_Music_Volume`: Volume |  | VI |  |
| 11001 | `music_pause_on_app_start` | Bool | Music | `#Settings_Music_PauseMusic_StartApp`: Pause music when starting an application |  | setting-prop |  |
| 11002 | `music_pause_on_voice_chat` | Bool | Music | `#Settings_Music_PauseMusic_VoiceChat`: Pause music when voice chatting |  | setting-prop |  |
| 11003 | `music_download_high_quality` | Bool | Music | `#Settings_Music_DownloadHighQuality`: Download high quality audio files |  | setting-prop |  |
| 12000 | `broadcast_permissions` | Enum | Broadcast | `#Settings_Broadcast_Privacy`: Privacy setting |  | setting-prop,GetClientSetting,VI |  |
| 12001 | `broadcast_output_width` | Int32 | Broadcast > #Settings_Broadcast_VideoDimensions |  | Paired with broadcast_output_height | VI |  |
| 12002 | `broadcast_output_height` | Int32 | Broadcast | `#Settings_Broadcast_VideoDimensions`: Video Dimensions |  | setting-prop |  |
| 12003 | `broadcast_bitrate` | Int32 | Broadcast | `#Settings_Broadcast_MaxBitRate`: Maximum Bitrate |  | setting-prop |  |
| 12004 | `broadcast_encoding_option` | Enum | Broadcast | `#Settings_Broadcast_OptimizeEncoding`: Optimize encoding for |  | setting-prop |  |
| 12005 | `broadcast_record_all_video` | Bool | Broadcast | `#Settings_Broadcast_RecordAllVideo`: Record video from all applications on this machine |  | setting-prop |  |
| 12006 | `broadcast_record_all_audio` | Bool | Broadcast | `#Settings_Broadcast_RecordAllAudio`: Record audio from all applications on this machine |  | setting-prop |  |
| 12007 | `broadcast_record_microphone` | Bool | Broadcast | `#Settings_Broadcast_RecordMicrophone`: Record my microphone   <1>Configure microphone</1> |  | setting-prop |  |
| 12008 | `broadcast_show_upload_stats` | Bool | Broadcast | `#Settings_Broadcast_ShowUploadStats`: Show upload stats |  | setting-prop,VI |  |
| 12009 | `broadcast_show_live_reminder` | Bool | Broadcast | `#Settings_Broadcast_AlwaysShowLive`: Always show Live status |  | setting-prop,VI |  |
| 12010 | `broadcast_chat_corner` | Int32 | Broadcast | `#Settings_Broadcast_ShowChat`: Show viewers' chat in game |  | setting-prop |  |
| 13000 | `gamestream_hardware_video_encode` | Bool | Game Recording | `#Settings_GameRecording_VideoHardwareEncoding`: Enable GPU hardware encoding |  | setting-prop,VI |  |
| 13001 | `gamestream_enable_video_h265` | Bool | Game Recording | `#Settings_GameRecording_VideoEnableH265`: Enable HEVC (H.265) video codec |  | VI |  |
| 14001 | `steam_input_configurator_error_msg_enable` | Bool | Developer > Steam Input |  | #Settings_Developer_SteamInputDev | VI |  |
| 14002 | `controller_guide_button_focus_steam` | Bool | Controller | `#Settings_Controller_GuideButtonFocus`: Guide button focuses Steam |  | setting-prop |  |
| 14003 | `controller_ps_support` | Int32 | Controller |  | PlayStation controller support (enum) | GetClientSetting,VI |  |
| 14004 | `controller_xbox_support` | Bool | Controller |  | Xbox controller Steam Input support | GetClientSetting,VI |  |
| 14005 | `controller_xbox_driver` | Bool | — |  | inf: Xbox extended driver toggle; no JS reference | — | no JS reference besides proto |
| 14006 | `controller_switch_support` | Bool | Controller |  | Switch controller Steam Input support | GetClientSetting,VI |  |
| 14007 | `controller_generic_support` | Bool | Controller |  | Generic controller Steam Input support | GetClientSetting,VI |  |
| 14008 | `controller_power_off_timeout` | Int32 | Controller | `#ControllerSettings_TurnOffTimeout_Never`: Never | Turn-off timeout (#ControllerSettings_TurnOffTimeout_*) | VI |  |
| 14009 | `turn_off_controller_on_exit` | Bool | Controller | `#Settings_Controller_TurnOffOnExit`: Turn off controllers when exiting Big Picture Mode |  | setting-prop |  |
| 14010 | `controller_combine_nintendo_joycons` | Bool | Controller / QAM | `#QuickAccess_Tab_ControllerSettings_Section_CombinedJoycon`: Combine Joy-Con Pairs | #QuickAccess_Tab_ControllerSettings_Section_CombinedJoycon | VI |  |
| 140011 | `controller_enable_chord` | Bool | Controller | `#Settings_Controller_ChordConfigEnable`: Enable Guide Button Chords for controllers |  | setting-prop |  |
| 140012 | `controller_poll_rate` | Bool | — |  | inf: controller polling-rate toggle; no JS reference | — | no JS reference besides proto |
| 140013 | `controller_siapi_config_author_mode` | Bool | Developer | `#Settings_Developer_SteamInputConfigAuthor`: Steam Input API Config Author Mode | #Settings_Developer_SteamInputConfigAuthor | VI |  |
| 140014 | `controller_show_ibex_tour` | Bool | Developer > Miscellaneous | `#ControllerWelcome_Setting_Label`: Show Steam Controller Tour | #ControllerWelcome_Setting_Label (Show Steam Controller Tour) | setting-prop,VI |  |
| 140030 | `controller_chat_radial_menu_option_0` | String |  |  |  | — |  |
| 140031 | `controller_chat_radial_menu_option_1` | String |  |  |  | — |  |
| 140032 | `controller_chat_radial_menu_option_2` | String |  |  |  | — |  |
| 140033 | `controller_chat_radial_menu_option_3` | String |  |  |  | — |  |
| 140034 | `controller_chat_radial_menu_option_4` | String |  |  |  | — |  |
| 140035 | `controller_chat_radial_menu_option_5` | String |  |  |  | — |  |
| 140036 | `controller_chat_radial_menu_option_6` | String |  |  |  | — |  |
| 140037 | `controller_chat_radial_menu_option_7` | String |  |  |  | — |  |
| 16000 | `startup_movie_id` | Uint64String | Customization > Startup movie |  | Set together with startup_movie_local_path when a startup movie is equipped | VI,qt |  |
| 16001 | `startup_movie_local_path` | String | Customization > Startup movie |  |  | VI,qt |  |
| 16002 | `startup_movie_shuffle` | Bool | Customization | `#Settings_Customization_StartupVideo_Shuffle`: Shuffle Startup Movie |  | VI |  |
| 16003 | `startup_movie_used_for_resume` | Bool | Customization > Startup movie |  | Use startup movie on resume (inferred) | VI |  |
| 16004 | `screensaver_current_id` | String | Customization | `#Settings_Customization_Screensaver_Screenshots_All`: All Games |  | VI |  |
| 16005 | `screensaver_settings` | String | Customization > Screensaver |  | Opaque string (screensaver-specific settings) | VI |  |
| 16006 | `screensaver_while_ingame` | Bool | Customization | `#Settings_Customization_Screensaver_WhileInGame`: Show screensavers when playing a game |  | setting-prop |  |
| 17001 | `game_notes_enable_spellcheck` | Bool | Game Notes |  | Spellcheck toggle in the notes editor | VI |  |
| 18000 | `screenshot_items_per_row` | Int32 | — |  | inf: screenshot manager grid density; no JS reference | — | no JS reference besides proto |
| 18201 | `gamerecording_background_path` | String | Game Recording > Recordings folder |  |  | VI |  |
| 18202 | `gamerecording_background_max_keep` | String | Game Recording > Background recording max length/size |  |  | VI |  |
| 18203 | `gamerecording_background_time_resolution` | Int32 | — |  | inf: background recording timeline granularity; no JS reference | — | no JS reference besides proto |
| 18207 | `gamerecording_background_mk` | CMsgHotkey (message) | Game Recording > Shortcut keys (inf: mark/bookmark key) |  |  | VI |  |
| 18208 | `gamerecording_background_tg` | CMsgHotkey (message) | Game Recording > Shortcut keys (inf: toggle recording key) |  |  | VI |  |
| 18209 | `gamerecording_background_a_m` | Bool | Game Recording | `#Settings_GameRecording_AudioRecording_Mic`: Record Microphone<br>desc: Enables recording of your system microphone input along with gameplay audio. |  | setting-prop,VI |  |
| 18210 | `gamerecording_video_bitrate` | String | Game Recording | `#Settings_GameRecording_RecordingQuality`: Recording Quality |  | VI |  |
| 18212 | `gamerecording_background_mode` | Enum | Game Recording > mode (off / background / manual) | `#QuickAccess_Tab_GameRecording_ManualRecordingToggle`: Game recording |  | VI |  |
| 18213 | `gamerecording_background_audio` | Enum | Game Recording | `#Settings_GameRecording_AudioSelection_GameOnly`: Game Audio Only | #Settings_GameRecording_AudioSelection_* | VI |  |
| 18214 | `gamerecording_max_fps` | Int32 | Game Recording | `#Settings_GameRecording_MaxFrameRate`: Maximum frame rate |  | setting-prop,VI |  |
| 18215 | `gamerecording_hotkey_ic` | CMsgHotkey (message) | Game Recording | `#Settings_GameRecording_Shortcut_Title`: Shortcut Keys |  | VI |  |
| 18216 | `gamerecording_ic_seconds` | Float | Game Recording | `#Settings_GameRecording_InstantClipDropdown_Label`: Clip duration |  | setting-prop,VI |  |
| 18217 | `gamerecording_export_limit_type` | Enum | Game Recording > Export limits |  |  | VI |  |
| 18218 | `gamerecording_export_limit_size_mb` | Int32 |  |  |  | VI |  |
| 18219 | `gamerecording_export_limit_bitrate` | Int32 |  |  |  | VI |  |
| 18220 | `gamerecording_export_limit_width` | Int32 |  |  |  | VI |  |
| 18221 | `gamerecording_export_limit_height` | Int32 |  |  |  | VI |  |
| 18222 | `gamerecording_export_limit_frame_rate` | Int32 |  |  |  | VI |  |
| 18223 | `gamerecording_export_directory` | String | Game Recording > Export |  | Clip export directory | VI |  |
| 18224 | `gamerecording_export_codec` | Enum |  |  |  | VI |  |
| 18225 | `gamerecording_video_maxheight` | Int32 | Game Recording | `#Settings_GameRecording_VideoMaxHeight`: Maximum video height<br>desc: Width will be automatically set to preserve the game's aspect ratio |  | setting-prop,VI |  |
| 18226 | `gamerecording_force_mic_mono` | Bool | Game Recording | `#Settings_GameRecording_AudioRecording_MicMono`: Force Microphone to Mono<br>desc: Select if you hear your microphone only in one channel during playback. |  | setting-prop |  |
| 18227 | `gamerecording_automatic_gain_control` | Bool | Game Recording | `#Settings_GameRecording_AudioRecording_AGC`: Automatic Gain Control<br>desc: Automatically adjusts microphone recording level for consistent volume and clarity. |  | setting-prop |  |
| 20000 | `show_timestamps_in_console` | Bool | Developer > Miscellaneous | `#Settings_Developer_ShowTimestampsInConsole`: Show timestamps in Steam console | #Settings_Developer_ShowTimestampsInConsole | setting-prop,VI |  |
| 20002 | `override_browser_composer_mode` | Int32 | Developer | `#Settings_Developer_ForceSystemComposer`: Force system browser composer | #Settings_Developer_ForceSystemComposer; toggles between two composer modes then prompts restart | VI |  |
| 20003 | `cef_remote_debugging_enabled` | Bool | Developer | `#Settings_Developer_CefRemoteDebugging`: CEF Remote Debugging<br>desc: Toggle to auto-enable CEF remote debugging at startup |  | setting-prop | requires restart |
| 20004 | `force_deck_perf_tab` | Bool | Developer (hidden: rendered behind `!1&&`, i.e. compiled out) |  | Literal label 'Force QAM perf tab to show all deck settings' | setting-prop,VI |  |
| 20005 | `force_fake_mandatory_update` | Bool | Hidden (no UI toggle seen) |  | When true, UI shows a mandatory-update gate; applying it clears the flag (debug) | VI |  |
| 20006 | `hdr_compat_testing` | Bool | Developer | `#Settings_Developer_HDRCompatTesting`: HDR Compatibility Testing<br>desc: Ignore previously published per-app HDR compatibility information |  | setting-prop,VI |  |
| 20007 | `developer_mode_enabled` | Bool | System > #Settings_System_EnableDeveloperMode (Enable Developer Mode) |  | Unlocks the Developer settings page (also unlocked by Config.DEV_MODE). Also pushed to VR via path property | VI |  |
| 20008 | `show_advanced_update_channels` | Bool | Developer > #Settings_Developer_ShowAdvancedOSBranches |  | Show Advanced Update Channels (SteamOS) | VI |  |
| 20009 | `browserview_underlays_allowed` | Bool | Developer > Miscellaneous |  | Literal: 'Enable browserview underlays' - Allow browserview underlays to be used if hardware requirements are met. Requires restart | setting-prop | requires restart |
| 21001 | `gamescope_hdr_visualization` | Enum | Developer > Miscellaneous (#Settings_HDRVisualization_Label) |  | Enum: None/Heatmap/Heatmap Extended/Heatmap Classic/Analysis (inferred from zoo labels) | setting-prop |  |
| 21002 | `gamescope_app_target_framerate` | Int32 | QAM > Performance | `#QuickAccess_Tab_Perf_AppRefreshRate`: Frame Limit |  | setting-prop,VI |  |
| 21003 | `gamescope_enable_app_target_framerate` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_AppRefreshRateEnable`: Enable Unified Frame Limit Management |  | setting-prop,VI |  |
| 21004 | `gamescope_disable_framelimit` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_DisableFrameLimit`: Disable Frame Limit |  | setting-prop,VI |  |
| 21005 | `gamescope_display_refresh_rate` | Int32 | QAM > Performance | `#QuickAccess_Tab_Perf_GamescopeRefreshRate`: Refresh Rate |  | setting-prop |  |
| 21006 | `gamescope_use_game_refresh_rate_in_steam` | Bool | Valve Internal > Display | `#Settings_Developer_UseGameRefreshRateInSteam`: Use game display refresh rate in Steam | #Settings_Developer_UseGameRefreshRateInSteam | setting-prop |  |
| 21007 | `gamescope_disable_mura_correction` | Bool | Display | `#Settings_Display_MuraCorrectionDisabled_Label`: Disable Mura Compensation |  | setting-prop |  |
| 21008 | `gamescope_include_steamui_in_screenshots` | Bool | In Game | `#Settings_InGame_ScreenshotShowSteamUI`: Include Steam UI elements in screenshots |  | setting-prop |  |
| 21009 | `gamescope_allow_tearing` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_EnableTearing`: Allow Tearing |  | setting-prop |  |
| 21010 | `gamescope_composite_debug` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_EnableCompositeDebug`: Composite Debug |  | setting-prop |  |
| 21011 | `gamescope_force_composite` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_ForceComposite`: Force Composite |  | setting-prop |  |
| 21012 | `gamescope_game_resolution_global` | String | Display | `#Settings_Display_GameResolution`: Maximum Game Resolution | Maximum Game Resolution (global default) | VI |  |
| 21013 | `gamescope_guide_hotkey` | CMsgHotkey (message) | In Game | `#Settings_InGame_Hotkey_MainMenu`: Main Menu shortcut key(s) |  | setting-prop,VI |  |
| 21014 | `gamescope_qam_hotkey` | CMsgHotkey (message) | In Game | `#Settings_InGame_Hotkey_QuickAccess`: Quick Access Menu shortcut key(s) |  | setting-prop,VI |  |
| 21015 | `gamescope_hdr_enabled` | Bool | Display | `#Settings_HDR_Enable`: Enable HDR |  | setting-prop |  |
| 21016 | `gamescope_native_external_res_in_steam` | Bool | Valve Internal (gamescope only) |  | Literal: 'Enable Native Resolution on External Displays' | setting-prop,VI |  |
| 22000 | `steamos_status_led_brightness` | Int32 | Display | `#Settings_Display_StatusLEDBrightness`: Status LED Brightness |  | setting-prop |  |
| 22001 | `steamos_tdp_limit_enabled` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_TDPLimitEnabled`: TDP Limit |  | setting-prop,VI |  |
| 22002 | `steamos_tdp_limit` | Int32 | QAM Performance > TDP limit value |  |  | setting-prop |  |
| 22003 | `steamos_cec_enabled` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_Enabled`: Enable HDMI CEC Support |  | setting-prop,VI |  |
| 22004 | `steamos_cec_wake_on_resume` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_WakeOnResume`: Wake TV when device resumes from sleep |  | setting-prop |  |
| 22005 | `steamos_wifi_debug` | Bool | Developer/Internet (SteamOS Wi-Fi) | `#Settings_SteamOS_WifiDebug`: Enable Wi-Fi debug data collection |  | setting-prop |  |
| 22006 | `steamos_wifi_force_wpa_supplicant` | Bool | Developer/Internet (SteamOS Wi-Fi) | `#Settings_SteamOS_ForceWPASupplicant`: Force WPA Supplicant Wi-Fi backend |  | setting-prop |  |
| 22007 | `steamos_magnifier_scale` | Int32 | Display | `#Settings_Display_Mangifier_Scale`: Magnifier Scale |  | setting-prop |  |
| 22008 | `steamos_manual_gpu_clock_enabled` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_GPUClockControl`: Manual GPU Clock |  | setting-prop,VI |  |
| 22009 | `steamos_manual_gpu_clock_hz` | Int32 | QAM Performance > Manual GPU clock value |  |  | setting-prop |  |
| 22010 | `steamos_platform_performance_profile` | String | QAM > Performance | `#PlatformPerformanceProfile_Label`: Performance Profile |  | setting-prop,VI |  |
| 22011 | `steamos_charge_limit_enabled` | Bool | Power | `#Settings_Battery_ChargeLimitEnable`: Enable battery charging limit |  | setting-prop,VI |  |
| 22012 | `steamos_charge_limit` | Int32 | Power | `#Settings_Battery_ChargeLimitValue`: Battery charging limit |  | setting-prop |  |
| 22013 | `steamos_charge_limit_devmode` | Bool | Power | `#Settings_Battery_ChargeLimitDevMode`: Allow battery limit full range |  | setting-prop,VI |  |
| 22014 | `steamos_system_tracing_enabled` | Bool | Developer/System | `#Settings_Tracing`: Enable System Tracing<br>desc: Toggle background tracing of CPU/GPU events |  | setting-prop |  |
| 22015 | `steamos_vrs_enabled` | Bool | QAM > Performance | `#QuickAccess_Tab_Perf_VariableResolution`: Half Rate Shading |  | setting-prop |  |
| 22016 | `steamos_separate_led_colors` | Bool | Display/LED | `#Settings_LED_SeparateColors`: Control LED strip colors individually |  | setting-prop,VI |  |
| 22017 | `steamos_wifi_reload_wifi_driver_on_sleep` | Bool | Developer/Internet (SteamOS Wi-Fi) | `#Settings_SteamOS_ReloadWifiDriverOnSleep`: Reload Wi-Fi driver on sleep |  | setting-prop |  |
| 220018 | `steamos_wifi_power_management_enabled` | Bool | Developer | `#Settings_Developer_WifiPowersave`: Enable Wi-Fi Power Management<br>desc: Disabling power management may increase connection reliability on 5GHz networks |  | setting-prop |  |
| 22019 | `steamos_cec_control` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_Control`: Enable remote control input |  | setting-prop |  |
| 22020 | `steamos_cec_suspend_tv` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_SuspendTV`: Turn off TV when going to sleep |  | setting-prop |  |
| 22021 | `steamos_cec_suspend_device` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_SuspendDevice`: Sleep when turning off the TV |  | setting-prop |  |
| 22022 | `steamos_cec_wake_tv` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_WakeTV`: Turn on TV when resuming from sleep |  | setting-prop |  |
| 22023 | `steamos_cec_wake_device` | Bool | Display/System > HDMI-CEC | `#Settings_CEC_WakeDevice`: Resume from sleep when turning on the TV |  | setting-prop |  |
| 22024 | `steamos_ec_logging_enabled` | Bool | Developer | `#Settings_Developer_EnableECLog`: Enable EC logging<br>desc: Output the EC firmware log to the system journal |  | setting-prop |  |
| 23001 | `setting_validation_bool` | Bool | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23002 | `setting_validation_enum` | Enum | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23003 | `setting_validation_int32` | Int32 | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23004 | `setting_validation_uint32` | Uint32 | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23005 | `setting_validation_uint64` | Uint64String | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23006 | `setting_validation_float` | Float | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23007 | `setting_validation_string` | String | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 23008 | `setting_validation_hotkey` | CMsgHotkey (message) | GamepadUI Settings Zoo > ClientSettings (/zoo/clientsettings) |  | Test-only field used to exercise each setting type in the zoo | setting-prop |  |
| 24000 | `system_bluetooth_enabled` | Bool | Bluetooth (QAM / settings) |  |  | setting-prop,VI |  |
| 24001 | `hardware_updater_enabled` | Bool | Valve Internal > Miscellaneous |  | Literal: 'Enable Hardware Updater'. Requires restart | setting-prop | requires restart |
| 24003 | `system_idle_suspend_battery_sec` | Int32 | Power > #Settings_System_Idle_Sleep_Label |  | Battery variant | — |  |
| 24004 | `system_idle_suspend_ac_sec` | Int32 | Power > #Settings_System_Idle_Sleep_Label |  | AC variant | — |  |
| 24005 | `system_enable_low_power_downloads` | Bool | Power | `#Settings_LowPowerDownloads_Enable`: Finish downloads with display off before sleeping<br>desc: If your device enters sleep mode, your games will continue downloading in a low-power, display-off state. |  | setting-prop |  |
| 24006 | `system_allow_battery_low_power_downloads` | Bool | Power | `#Settings_LowPowerDownloads_AllowBattery`: Enable display-off downloads on battery power<br>desc: If your battery level falls below 20% while downloading with the display-off, your device will go to sleep. |  | setting-prop |  |
| 24008 | `system_idle_screensaver_battery_sec` | Int32 | Power > idle screensaver |  | Battery variant | — |  |
| 24009 | `system_idle_screensaver_ac_sec` | Int32 | Power > idle screensaver |  | AC variant | — |  |
| 25000 | `vr_show_perf_graph_in_hmd` | Bool | — |  | inf: SteamVR perf graph in headset; no JS reference | — | no JS reference besides proto |
| 26000 | `accessibility_debug_visualizer` | Bool | Valve Internal > Accessibility |  | Literal: 'Enable Accessibility Debug Visualizer' | setting-prop,VI |  |
| 26001 | `accessibility_screen_reader_enabled` | Bool | Accessibility | `#Settings_ScreenReader_Enabled`: Enable Screen Reader |  | setting-prop,VI |  |
| 26002 | `accessibility_screen_reader_rate` | Float | Accessibility | `#Settings_ScreenReader_Rate`: Reader Rate |  | setting-prop |  |
| 26003 | `accessibility_screen_reader_pitch` | Float | Accessibility | `#Settings_ScreenReader_Pitch`: Reader Pitch |  | setting-prop |  |
| 26004 | `accessibility_screen_reader_volume` | Float | Accessibility | `#Settings_ScreenReader_Volume`: Reader Volume |  | setting-prop |  |
| 26005 | `accessibility_high_contrast_mode` | Bool | Accessibility | `#Settings_HighContrastMode`: High Contrast Mode<br>desc: Make Steam text, buttons and icons more distinct from the background. |  | setting-prop |  |
| 26006 | `accessibility_reduce_motion` | Bool | Accessibility | `#Settings_ReduceMotion`: Reduce Motion<br>desc: Disable certain Steam animations, effects and transitions to reduce on-screen movement. |  | setting-prop,GetClientSetting,VI |  |
| 26008 | `accessibility_minimum_font_size` | Uint32 |  |  |  | setting-prop |  |
| 26009 | `accessibility_color_filter_name` | String | Accessibility | `#Settings_ColorFilter`: Color Filter<br>desc: Modify display colors, both in-game and in Steam. |  | setting-prop |  |
| 26010 | `accessibility_desktop_ui_scale` | Float | Display | `#Settings_Display_DisplayScaling_Slider_Label`: UI Scale |  | setting-prop |  |
| 26011 | `accessibility_screen_reader_locale` | String | Accessibility | `#Settings_ScreenReader_Locale`: Reader Language |  | setting-prop |  |
| 26012 | `accessibility_mono_audio` | Bool | — |  | inf: mono audio accessibility; no JS reference in this build | — | no JS reference besides proto |
| 27000 | `remote_play_wifi_ap_enabled` | Bool | Remote Play > Wi-Fi AP |  | Steam Frame / wireless adapter AP (inferred) | VI |  |
| 27001 | `remote_play_wifi_ap_channel_5ghz` | Int32 | Remote Play | `#Settings_RemotePlay_WifiAPChannel5`: Channel (for 5GHz operation) |  | setting-prop,VI |  |
| 27002 | `remote_play_wifi_ap_channel_6ghz` | Int32 | Remote Play | `#Settings_RemotePlay_WifiAPChannel6`: Channel (for 6GHz operation) |  | setting-prop,VI |  |
| 27003 | `remote_play_wifi_ap_channel_width` | Int32 | Remote Play | `#Settings_RemotePlay_WifiAPChannelWidth`: Channel Width |  | setting-prop,VI |  |
| 27004 | `remote_play_wifi_ap_hotspot_mode` | Bool | Remote Play | `#Settings_RemotePlay_ConnectionManagement`: Connection Management |  | setting-prop,VI |  |
| 27005 | `remote_play_wifi_ap_hotspot_ssid` | String | Remote Play | `#Settings_RemotePlay_WifiAPHotspotSSID`: Hotspot SSID |  | setting-prop |  |
| 27006 | `remote_play_wifi_ap_hotspot_password` | String | Remote Play | `#Settings_RemotePlay_WifiAPHotspotPassword`: Hotspot Password |  | setting-prop |  |
| 27007 | `remote_play_wifi_ap_hotspot_routing` | String | Remote Play | `#Settings_RemotePlay_WifiAPHotspotRouting`: Hotspot Client Internet |  | setting-prop |  |
| 27008 | `remote_play_wifi_ap_show_advanced` | Bool | Remote Play > Wi-Fi AP |  | Show advanced AP options | VI |  |
| 27009 | `remote_play_wifi_ap_paired_ssid` | String | Remote Play > Wi-Fi AP |  | Paired SSID | VI |  |
| 27010 | `skip_steamframe_pairing_dialog` | Bool | Dialog suppression |  | inf: don't show Steam Frame pairing dialog again | VI |  |
| 27011 | `skip_steamframe_troubleshooting_dialog` | Bool | Dialog suppression | `#SteamFrameWirelessAdapterTroubleshootingDialog_DontShowAgain`: Don't show this dialog again | Don't show again (Steam Frame wireless adapter troubleshooting) | VI |  |
| 27012 | `skip_steamframe_airplane_dialog` | Bool | Dialog suppression | `#SteamFrameWirelessAdapterTroubleshootingDialog_DontShowAgain`: Don't show this dialog again | Don't show again (Steam Frame airplane-mode dialog) | VI |  |
| 28001 | `oobe_completed` | Bool | OOBE state |  | Set when first-run (out-of-box) flow completes | GetClientSetting,VI |  |
| 28002 | `oobe_test_mode_enabled` | Bool | OOBE state (read-only in JS) |  | When set, OOBE completion is tracked in memory only (test mode) | GetClientSetting,hX |  |
| 28003 | `force_oobe` | Bool | Valve Internal > OOBE | `#Settings_ForceOOBE`: Force OOBE<br>desc: Forces out of box experience on every device start | #Settings_ForceOOBE | setting-prop,qt |  |
| 28004 | `oobe_stage_2_completed` | Bool | OOBE state |  | Stage-2 OOBE completion | GetClientSetting,VI |  |
| 28005 | `oobe_stage_2_test_mode_enabled` | Bool | OOBE state (read-only in JS) |  | Stage-2 OOBE test mode | GetClientSetting,hX |  |
| 28006 | `force_stage_2_oobe` | Bool | Valve Internal > OOBE |  | Literal: 'Force OOBE Stage 2' - Forces out of box experience (stage 2) on every device start | setting-prop |  |
| 29000 | `compat_show_all_tools` | Bool | Compatibility | `#Settings_SteamPlay_ShowAll`: Show all compatibility tools |  | setting-prop,VI |  |

Gaps in the field numbering (2–4, 15, 17, 18, 4005, 5002, 14000, 16007+, 18001–18200, 18204–18206, 18211, 20001, 24002, 24007, 26007) are probably retired fields.

Two field numbers look odd: `controller_enable_chord`..`controller_chat_radial_menu_option_7` use 140011–140037, and `steamos_wifi_power_management_enabled` uses 220018. These look like typos in Valve's proto (14001x and 22018 would be the expected values). The JS ignores the numbers because it addresses fields by name.

## Legacy settings object (`settingsStore.settings`, from `SteamClient.Settings.RegisterForSettingsChanges`)

These are the properties the JS reads. The full object comes from C++, so it may hold more.

| Property | Type | Use |
|---|---|---|
| `bIsValveEmail` | bool | Account has a Valve e-mail address. Together with developer mode it unlocks the **Valve Internal** settings page and other internal UI. |
| `bIsSteamSideload` | bool | Running a sideloaded Steam client. Shown in the Valve Internal page, which offers "Set system/sideload Steam as default" (`SteamClient.Settings.ToggleSteamInstall`). |
| `bIsInClientBeta`, `nSelectedBetaID`, `vecAvailableClientBetas`, `bChangeBetaEnabled` | bool/int/array/bool | Client beta participation picker (`SteamClient.Settings.SelectClientBeta`, `AddClientBeta`). |
| `bCompatEnabled` | bool | Steam Play for all titles enabled (Compatibility page). |
| `bEnableSoftProcessKill` | bool | Valve Internal toggle "Enable Soft Process Kill" (`SteamClient.Settings.SetEnableSoftProcessKill`). |
| `bDisplayIsExternal`, `bDisplayIsUsingAutoScale`, `flCurrentDisplayScaleFactor`, `flMinDisplayScaleFactor`, `flMaxDisplayScaleFactor`, `flAutoDisplayScaleFactor` | bool/float | Display scaling page and dialog. |
| `bUnderscanEnabled`, `flCurrentUnderscanLevel` | bool/float | Underscan (SteamOS). |
| `strDisplayName` | string | Current display name. |

## Friends settings (`SteamClient.FriendSettings`, JSON)

These are read through `RegisterForSettingsChanges` and written with `SetFriendSettings(JSON)`. Defaults come from module `uL()` in `sp.js`:

| Key | Default |
|---|---|
| `bNotifications_ShowIngame` | true |
| `bNotifications_ShowOnline` | false |
| `bNotifications_ShowMessage` | true |
| `bNotifications_EventsAndAnnouncements` | true |
| `bSounds_PlayIngame` | false |
| `bSounds_PlayOnline` | false |
| `bSounds_PlayMessage` | true |
| `bSounds_EventsAndAnnouncements` | false |
| `bAlwaysNewChatWindow` | false |
| `bForceAlphabeticFriendSorting` | false |
| `nChatFlashMode` | constant (0 = always, inferred) |
| `bRememberOpenChats` | true |
| `bCompactQuickAccess` | false |
| `bCompactFriendsList` | false |
| `bNotifications_ShowChatRoomNotification` | true |
| `bSounds_PlayChatRoomNotification` | true |
| `bHideOfflineFriendsInTagGroups` | false |
| `bHideCategorizedFriends` | false |
| `bCategorizeInGameFriendsByGame` | true |
| `nChatFontSize` | 2 |
| `b24HourClock` | false |
| `bDoNotDisturbMode` | false |
| `bDisableEmbedInlining` | false |
| `bSignIntoFriends` | true |
| `bDisableSpellcheck` | false |
| `bDisableRoomEffects` | false |
| `bAnimatedAvatars` | true |
| `featuresEnabled` | {} |

`bSingleWindowMode` is also read and written ("Dock chats to the friends list"). `SteamClient.FriendSettings.GetEnabledFeatures` returns the friends-UI feature flags.

## Server-side preferences cached by the settings store

| Object | Keys (JS) | Persistence |
|---|---|---|
| Community preferences (`Player.GetCommunityPreferences` / `SetCommunityPreferences`) | `bParenthesizeNicknames`, `eTextFilterSetting` (Chat Filtering), `bTextFilterIgnoreFriends`, `content_descriptor_preferences.content_descriptors_to_exclude[]` | Cached in user local storage key `CachedCommunityPreferences` |
| Store preferences (`StoreService` GetStorePreferences, read-only in the client UI) | `eReviewScorePreference`, `content_descriptor_preferences`, `provide_deck_feedback`, `game_frame_rate_reporting`, `primary_language`, `secondary_languages`, `additional_languages` | `CachedStorePreferences` |
| Notification preferences (`SteamNotification.GetPreferences` / `SetPreferences`) | array of `{notification_type, notification_targets}` (bitmask) | `CachedNotificationPreferences` |
| Battery preferences (local only) | `bShowBatteryPercentage` (default false) | `CachedBatteryPreferences` |
| Time zone | `SteamClient.Settings.Get/SetTimeZone`, `RegisterForTimeZoneChange` | client |
| Language | `SteamClient.Settings.Get/SetCurrentLanguage`, `GetAvailableLanguages` | client |

## Other settings-like protobufs exchanged with the client

**`CMsgSystemManagerSettings`** is written with `SteamClient.System.UpdateSettings` and read with `RegisterForSettingsChanges`. It covers the display, night mode, fan and brightness settings on SteamOS. Fields: idle_backlight_dim_battery_seconds, idle_backlight_dim_ac_seconds, is_adaptive_brightness_available, display_adaptive_brightness_enabled, display_nightmode_enabled, display_nightmode_tintstrength, display_nightmode_maxhue, display_nightmode_maxsat, display_nightmode_uiexp, display_nightmode_blend, display_nightmode_reset, display_nightmode_schedule_enabled, display_nightmode_schedule_starttime, display_nightmode_schedule_endtime, display_diagnostics_enabled, als_lux_primary, als_lux_median, display_backlight_raw, display_brightness_adaptivemin, display_brightness_adaptivemax, is_fan_control_available, fan_control_mode, is_display_brightness_available, is_display_colormanagement_available, display_colorgamut, als_lux_alternate, is_display_colortemp_available, display_colortemp, display_colortemp_default, display_colortemp_enabled, display_colorgamut_labelset, display_brightness_overdrive_hdr_split.

**`CMsgSystemPerfSettings`** is written with `SteamClient.System.Perf.UpdateSettings` (a `CMsgSystemPerfUpdateSettings`: gameid, reset_to_default, settings_delta, skip_storage_update). It backs the Quick Access Menu performance tab.
- *Global*: diagnostic_update_rate, graphics_profiling_service_state, perf_overlay_service_state, perf_overlay_level, is_show_perf_overlay_over_steam_enabled, is_advanced_settings_enabled, allow_external_display_refresh_control, hdr_on_sdr_tonemap_operator, is_hdr_debug_heatmap_enabled, force_hdr_wide_gammut_for_sdr, sdr_to_hdr_brightness, is_color_management_enabled.
- *Per-app*: fps_limit, is_variable_resolution_enabled, is_dynamic_refresh_rate_enabled, tdp_limit, cpu_governor, cpu_governor_manual_mhz, scaling_filter, fsr_sharpness, is_fps_limit_enabled, is_tdp_limit_enabled, is_low_latency_mode_enabled, display_refresh_manual_hz, is_game_perf_profile_enabled, display_external_refresh_manual_hz, fps_limit_external, is_tearing_enabled, is_vrr_enabled, use_dynamic_refresh_rate_in_steam, split_scaling_filter, split_scaling_scaler.

**`CStreamingClientConfig`** is written with `SteamClient.RemotePlay.SetStreamingClientConfig` / `SetStreamingClientConfigEnabled`. Fields: quality, desired_resolution_x/y, desired_framerate_numerator/denominator, desired_bitrate_kbps, enable_hardware_decoding, enable_performance_overlay, enable_video_streaming, enable_audio_streaming, enable_input_streaming, audio_channels, enable_video_hevc, enable_performance_icons, enable_microphone_streaming, controller_overlay_hotkey, p2p_scope, enable_audio_uncompressed, display_limit, quality_limit, runtime_limit, decoder_limit[], enable_unreliable_fec, enable_video_av1, windowed, window_pixel_density, window_width/height, window_position_x/y, window_frame_offset_x/y, enable_video_pyrowave, pyrowave_quality_modifier, pyrowave_yuv444, pyrowave_bitrate_kbps, plus the `*_OBSOLETE` fields.

**`CStreamingServerConfig`** is written with `SetStreamingServerConfig` / `SetStreamingServerConfigEnabled`. Fields: host_play_audio, custom_display_device, display_resolution_setting, custom_display_resolution_x/y, display_refresh_rate_setting, custom_display_refresh_rate, display_hdr_setting, custom_display_hdr, enable_capture_nvfbc, enable_hardware_encoding, software_encoding_threads, enable_traffic_priority.

**`CGameRecording_PerGameSettings`** holds the per-game recording overrides: gameid, enabled, minutes, bitrate, infinite.

**Controller personalization** is written with `SteamClient.Input.SetControllerPersonalizationSetting(key, int)` and `...Float(key, float)`. String keys seen: bHaptics, bIMUOneEuroFilter, bLeftStickTouchDisablesLeftTrackPad, bRightStickTouchDisablesRightTrackPad, bSWAntiDrift, bUseSWBiases, ePlayerSlotLEDSetting, eRumbleIntensity, eRumblePreference, flAccelerometerStationaryTolerance, flGyroStationaryTolerance, nAuxCapSenseHysteresis, nAuxCapSenseThreshold, nLHapticStrength, nRHapticStrength, nLStickDeadzone, nRStickDeadzone, nTritonGyroHWCalValue, nTurnOffSound, nTurnOnSound. A few more calls pass the key as a variable.

**VR path properties** are sent with `SetProtoPathProperty` to SteamVR: `CVRGamepadUIShared_PathProperty_ClientSettings` {enable_ui_sounds} and `..._ClientUserInfo` {logged_in, valve_email, developer_mode_enabled}. String paths: `/steam/scene_app_input_preference/app_id`, `/steam/scene_app_input_preference/prefers_steam_input`.

**Parental settings** (`ParentalSettings`, read through `SteamClient.Parental.RegisterForParentalSettingsChanges`): steamid, applist_base_id, applist_base_description, applist_base, applist_custom, passwordhashtype, salt, passwordhash, is_enabled, enabled_features, recovery_email, is_site_license_lock, temporary_enabled_features, rtime_temporary_feature_expiration, playtime_restrictions, temporary_playtime_restrictions, excluded_store_content_descriptors (and further fields).
