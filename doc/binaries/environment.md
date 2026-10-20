# Environment variables

> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

**172** environment variables that the client binaries read or set (`getenv`, `secure_getenv`,
`setenv`, the `boolean_env` helper in `steam-launch-wrapper`, the SDR/SteamNetworkingSockets env accessor),
plus **103** variables injected into game processes. Valve ships no descriptions for env vars, so most
have none. The names are usually self-explanatory, and many are also handled in the shell scripts
(see [../launcher/](../launcher/)).

| Variable | Access | Value / default seen at call site | Binaries |
|---|---|---|---|
| `_STEAM_SETENV_MANAGER` | read |  | crashhandler.so, friendsui.so, gamelauncher, steam, steamclient.so, steamservice.so, steamui.so |
| `ALL_PROXY` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `all_proxy` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `BREAKPAD_DUMP_LOCATION` | read; set (CEF crash reporter) |  | chromehtml.so, crashhandler.so, friendsui.so, gamelauncher, steam, steamclient.so, steamservice.so, steamui.so |
| `breakpad_testfile` | read |  | crashhandler.so |
| `breakpad_verbose` | read |  | crashhandler.so |
| `CEF_CRASH_REPORTER_PRODUCT_VERSION` | set (CEF crash reporter) |  | chromehtml.so |
| `CEF_CRASH_REPORTER_SERVER_URL` | set (CEF crash reporter) | `https://crash.steampowered.com/submit` | chromehtml.so |
| `CPU_MHZ` | read |  | gamelauncher, libtier0_s.so, libvideo.so, steam, steamservice.so, streaming_client |
| `DBG_PATHMATCH` | read |  | chromehtml.so, crashhandler.so, filesystem_stdio.so, friendsui.so, gamelauncher, gameoverlayui.so, libtier0_s.so, libvideo.so, libvstdlib_s.so, steam, steam_monitor, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `DEBUG_DRM` | read |  | steamui.so, streaming_client |
| `DISPLAY` | read |  | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `DONT_BREAK_ON_ASSERT` | read |  | crashhandler.so, gamelauncher, libtier0_s.so, libvideo.so, steam, steam_monitor, steamservice.so, steamsysinfo, streaming_client |
| `DXVK_STATE_CACHE_PATH` | read |  | steamclient.so |
| `ENABLE_VULKAN_RENDERDOC_CAPTURE` | set |  | steam-launch-wrapper |
| `EnableConfiguratorSupport` | read |  | steamclient.so |
| `FOSSILIZE_APPLICATION_INFO_FILTER_PATH` | read |  | libVkLayer_steam_fossilize.so |
| `FOSSILIZE_DISABLE_RATE_LIMITER` | read |  | fossilize_replay |
| `FOSSILIZE_DUMP_SYNC` | read |  | libVkLayer_steam_fossilize.so |
| `FOSSILIZE_REPLAY_WRAPPER` | read |  | fossilize_replay |
| `FOSSILIZE_REPLAY_WRAPPER_ORIGINAL_APP` | set |  | fossilize_replay |
| `fs_debug` | read |  | filesystem_stdio.so, gamelauncher, steam |
| `GAMESCOPE_DISPLAY_DISABLED` | read |  | streaming_client |
| `GAMESCOPE_MODE_SAVE_FILE` | read |  | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_WAYLAND_DISPLAY` | read |  | crashhandler.so, gamelauncher, gameoverlayrenderer.so, libtier0_s.so, libvideo.so, steam, steam_monitor, steamclient.so, steamservice.so, steamsysinfo, steamui.so, streaming_client |
| `GDK_SCALE` | read |  | vgui2_s.so |
| `GLIBCXX_TUNABLES` | read |  | chromehtml.so, crashhandler.so, filesystem_stdio.so, fossilize_replay, friendsui.so, gamelauncher, gameoverlayrenderer.so, gameoverlayui.so, libVkLayer_steam_fossilize.so, libtier0_s.so, libvideo.so, libvstdlib_s.so, steam, steam_monitor, steamclient.so, steamoverlayvulkanlayer.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GLOVERLAYCOREPROFILE` | read |  | gameoverlayrenderer.so |
| `HOME` | read |  | chromehtml.so, crashhandler.so, filesystem_stdio.so, friendsui.so, gamelauncher, gameoverlayui.so, libtier0_s.so, libvideo.so, libvstdlib_s.so, steam, steam_monitor, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `HOMETEST_DESKTOP_SESSION` | read |  | steamui.so |
| `HOMETEST_DESKTOP_USER` | read |  | steamui.so |
| `HTTP_PROXY` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `http_proxy` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `HTTPS_PROXY` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `https_proxy` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `IgnoreChildProcesses` | read |  | gameoverlayrenderer.so, gameoverlayui.so |
| `JPEGMEM` | read |  | friendsui.so, gameoverlayui.so, steam, steamclient.so, steamui.so, steamwebhelper, streaming_client |
| `LANG` | read |  | steamclient.so, steamui.so, vgui2_s.so |
| `LC_ALL` | read |  | steamclient.so, steamui.so |
| `MANGOHUD_CONFIGFILE` | read |  | steamclient.so |
| `NO_PROXY` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `no_proxy` | read |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `OBJCOPY` | read |  | steamclient.so, steamservice.so |
| `OPENSSL_ia32cap` | read |  | friendsui.so, gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `PATH` | read; set |  | steam-launch-wrapper |
| `PRESSURE_VESSEL_SYSTEMD_SCOPE` | set | `0` | steam-launch-wrapper |
| `RADV_DEBUG` | read |  | steamclient.so |
| `RADV_FORCE_VRS_CONFIG_FILE` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `SDL_ENABLE_STEAM_CONTROLLER_MOUSE_MODE` | read |  | streaming_client |
| `SDL_GAMECONTROLLER_IGNORE_DEVICES` | read |  | gameoverlayrenderer.so |
| `SDR_CERT` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_CLIENT_PORT` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_DEVTICKET` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_IP` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_IP6` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_LISTEN_PORT` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_NETWORK_CONFIG` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_POPID` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_PRIVATE_KEY` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_PROBE_RELAY_INTERVAL` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SDR_PROBE_RELAY_INTERVAL_BUSY` | read (SteamNetworkingSockets/SDR) |  | steamclient.so |
| `SESSION_MANAGER` | read |  | vgui2_s.so |
| `SITE_SERVER_GUI` | read |  | steamclient.so |
| `SLEEP_BEFORE_ELEVATED_UPDATE` | read |  | gamelauncher, steam |
| `STEAM_ALLOW_DRIVE_ADOPT` | read |  | steamui.so |
| `STEAM_ALLOW_DRIVE_UNMOUNT` | read |  | steamui.so |
| `STEAM_BOOTSTRAP_LOG_VERBOSE` | read |  | gamelauncher, steam |
| `STEAM_BROWSER_RESIZE_WORKAROUND` | read |  | steamwebhelper |
| `STEAM_CEF_GPU_CMD_PREFIX` | read |  | chromehtml.so, steamclient.so |
| `STEAM_CLIENT_CONFIG_FILE` | read |  | gamelauncher, steam, steamclient.so |
| `STEAM_CLIENT_LOG_FOLDER` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamsysinfo, steamui.so, steamwebhelper |
| `STEAM_CLOUD_GAMING_PLATFORM` | read |  | steamclient.so |
| `STEAM_COMPAT_LAUNCHER_SERVICE` | read |  | steamclient.so |
| `STEAM_COMPAT_MOUNTS` | read |  | steamclient.so |
| `STEAM_COMPAT_PROTON` | read |  | steamclient.so |
| `STEAM_COMPAT_PROTON_SUPPRESS` | read |  | steamclient.so |
| `STEAM_COMPAT_TOOL_MAPPINGS` | read |  | steamclient.so |
| `STEAM_DEBUGCEF` | read |  | chromehtml.so, steamclient.so |
| `STEAM_DESKTOP_APP_AFFINITY_LIST` | read |  | crashhandler.so, gamelauncher, gameoverlayrenderer.so, libtier0_s.so, libvideo.so, steam, steam_monitor, steamservice.so, steamsysinfo, streaming_client |
| `STEAM_DISABLE_BROWSER_SHUTDOWN_WORKAROUND` | read |  | steamwebhelper |
| `STEAM_DISABLE_LIBNM_IPV6_WORKAROUND` | read |  | steamclient.so |
| `STEAM_DISABLE_MANGOAPP_ATOM_WORKAROUND` | read |  | steamclient.so |
| `STEAM_DISPLAY_REFRESH_LIMITS` | read |  | steamclient.so |
| `STEAM_ENABLE_AMD_LAYER` | read |  | steamclient.so |
| `STEAM_ENABLE_DYNAMIC_BACKLIGHT` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_ENABLE_FAN_CONTROL` | read |  | steamclient.so |
| `STEAM_ENABLE_SHADER_CACHE_MANAGEMENT` | read |  | steamclient.so |
| `STEAM_ENABLE_VOLUME_HANDLER` | read |  | steamui.so |
| `STEAM_ENABLE_XCOMPOSITE_WORKAROUND` | read |  | steamwebhelper |
| `STEAM_EXTRA_COMPAT_TOOLS_PATHS` | read |  | steamclient.so |
| `STEAM_FOSSILIZE_DUMP_PATH` | read |  | libVkLayer_steam_fossilize.so |
| `STEAM_FOSSILIZE_DUMP_PATH_READ_ONLY` | read |  | libVkLayer_steam_fossilize.so |
| `STEAM_FOSSILIZE_IDENTIFIER_DUMP_PATH` | read |  | libVkLayer_steam_fossilize.so |
| `STEAM_FOSSILIZE_LAST_USE_TAG` | read |  | libVkLayer_steam_fossilize.so |
| `STEAM_FOSSILIZE_PIPELINE_USE_DUMP_PATH` | read |  | libVkLayer_steam_fossilize.so |
| `STEAM_FOSSILIZE_PRECOMPILE_QA` | read |  | libVkLayer_steam_fossilize.so |
| `STEAM_FOSSILIZE_REPLAY_WRAP` | read |  | steamclient.so |
| `STEAM_GAME_LAUNCH_SHELL` | read |  | steamclient.so |
| `STEAM_GAMESCOPE_DYNAMIC_FPSLIMITER` | read |  | steamclient.so |
| `STEAM_GAMESCOPE_DYNAMIC_REFRESH_IN_STEAM_SUPPORTED` | read |  | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_GAMESCOPE_NIS_SUPPORTED` | read |  | steamclient.so |
| `STEAM_GAMESCOPE_VRR_SUPPORTED` | read |  | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_GAMESERVER_A2S_INFO_STRICT_LEGACY_PROTOCOL` | read |  | steamclient.so |
| `STEAM_GAMESERVER_ADVERTISE_SDR_LOCATION` | read |  | steamclient.so |
| `STEAM_GAMESERVER_PACKET_HANDLER_NO_IPC` | read |  | steamclient.so |
| `STEAM_GAMESERVER_RATE_LIMIT_200MS` | read |  | steamclient.so |
| `STEAM_GLCOMPOSER_USE_MAKECURRENT_LEGACY` | read |  | steamwebhelper |
| `STEAM_IGNORE_INDIRECT_RENDERING` | read |  | vgui2_s.so |
| `STEAM_LAUNCH_WRAPPER_DEBUG` | read (bool) | `0` | steam-launch-wrapper |
| `STEAM_LAUNCH_WRAPPER_GAME_BIN` | read (bool) | `1` | steam-launch-wrapper |
| `STEAM_LAUNCH_WRAPPER_JOURNAL` | read (bool) | `0` | steam-launch-wrapper |
| `STEAM_LAUNCH_WRAPPER_SCOPE` | read (bool) | `0` | steam-launch-wrapper |
| `STEAM_MANGOAPP_HORIZONTAL_SUPPORTED` | read |  | steamclient.so |
| `STEAM_MANGOAPP_PRESETS_SUPPORTED` | read |  | steamclient.so |
| `steam_master_ipc_name_override` | read; set |  | steamclient.so, steamui.so |
| `STEAM_MULTIPLE_XWAYLANDS` | read |  | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_NO_FAST_PPT` | read |  | steamclient.so |
| `STEAM_OPENAL_SKIP_CAPTURE` | read |  | steamclient.so |
| `STEAM_OVERLAY_DISABLE_WAIT_FOR_CEF_FRAME` | read |  | gameoverlayrenderer.so |
| `STEAM_OVERLAY_FRAME_TIME_LOGGING` | read |  | gameoverlayrenderer.so |
| `STEAM_OVERLAY_LOGGING` | read |  | gameoverlayrenderer.so |
| `STEAM_OVERLAY_LOGGING_FLUSH` | read |  | gameoverlayrenderer.so |
| `STEAM_OVERLAY_VULKAN_LAYER_FORCE_COMPUTE` | read |  | steamoverlayvulkanlayer.so |
| `STEAM_OVERLAY_WINDOW_BLACKLIST` | read |  | gameoverlayrenderer.so |
| `STEAM_RUNTIME` | read |  | gamelauncher, steam, steam-launch-wrapper, steamui.so |
| `STEAM_RUNTIME_LIBRARY_PATH` | read |  | steamclient.so |
| `STEAM_RUNTIME_LOGGER` | read |  | gamelauncher, steam |
| `STEAM_RUNTIME_STEAMRT` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_SPEW_LEVELS` | read |  | steamclient.so |
| `STEAM_UPDATEUI_PNG_BACKGROUND` | read |  | steam |
| `STEAM_USE_DYNAMIC_VRS` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_USE_MANGOAPP` | read |  | steamclient.so |
| `STEAM_USE_WPASUPPLICANT` | read |  | steamui.so |
| `STEAM_VKOVERLAY_FORCE_YCBCR_SUPPORT` | read |  | steamoverlayvulkanlayer.so |
| `SteamAppId` | read |  | steam-launch-wrapper, steamclient.so |
| `SteamDeck` | read |  | gameoverlayrenderer.so, steamclient.so |
| `SteamDisableOverlayDPIScaling` | read |  | gameoverlayrenderer.so |
| `SteamEnv` | read |  | steamclient.so |
| `SteamGameId` | read |  | gameoverlayrenderer.so |
| `SteamGamepadUI` | read |  | gameoverlayrenderer.so |
| `STEAMNETWORKINGSOCKETS_LOG_FILE` | read |  | steamclient.so, streaming_client |
| `STEAMNETWORKINGSOCKETS_LOG_LEVEL` | read |  | steamclient.so, streaming_client |
| `SteamNoOverlayUIDrawing` | read |  | gameoverlayrenderer.so |
| `SteamOS` | read |  | steamclient.so |
| `STEAMOS_STEAM_REBOOT_SENTINEL` | read |  | steamui.so |
| `STEAMOS_STEAM_SHUTDOWN_SENTINEL` | read |  | steamui.so |
| `SteamOverlayGameId` | read |  | gameoverlayrenderer.so |
| `SteamOverlayUseXFilterEvent` | read |  | gameoverlayrenderer.so |
| `SteamRealm` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so |
| `SteamStreamingAllowGameVsync` | read |  | gameoverlayrenderer.so |
| `SteamStreamingVideo` | read |  | gameoverlayrenderer.so |
| `SteamStreamingVideoDisableVSync` | read |  | gameoverlayrenderer.so |
| `SteamTenfoot` | read |  | steamclient.so |
| `SteamUniverse` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so |
| `STEAMVIDEOTOKEN` | read; set |  | chromehtml.so, crashhandler.so, friendsui.so, gamelauncher, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper |
| `STEAMVIDEOTOKEN2` | set | `7b7fe2a66d548a0daf01c44056f5` | steamwebhelper |
| `StreamForOpenVR` | read |  | gameoverlayrenderer.so |
| `SUPPRESS_STEAM_OVERLAY` | read |  | steamclient.so |
| `SYSTEM_LD_LIBRARY_PATH` | read |  | steamclient.so |
| `SYSTEM_PATH` | read |  | steamclient.so |
| `TMPDIR` | read |  | chromehtml.so, crashhandler.so, filesystem_stdio.so, friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, libvstdlib_s.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `TZDIR` | read |  | steamui.so |
| `USER` | read |  | crashhandler.so, gamelauncher, gameoverlayrenderer.so, libtier0_s.so, libvideo.so, steam, steam_monitor, steamclient.so, steamservice.so, steamsysinfo, streaming_client |
| `VR_CONFIG_PATH` | read |  | steamclient.so, steamui.so |
| `VR_LOG_PATH` | read |  | steamclient.so, steamui.so |
| `VR_OVERRIDE` | read |  | steamclient.so, steamui.so |
| `WAYLAND_DISPLAY` | read |  | steamui.so, streaming_client |
| `WSL_DISTRO_NAME` | read |  | crashhandler.so, gamelauncher, libtier0_s.so, libvideo.so, steam, steam_monitor, steamservice.so, steamsysinfo, streaming_client |
| `XDG_CONFIG_HOME` | read |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `XDG_DATA_HOME` | read |  | steamclient.so, steamui.so |
| `XDG_RUNTIME_DIR` | read |  | steam-launch-wrapper |
| `XDG_SESSION_TYPE` | read |  | gameoverlayrenderer.so, steamui.so |

## Environment Steam sets for launched games

Steam builds a launch environment for every game process (`steamclient.so`). The table lists every variable
name passed to that setter. An empty value means the client computes it at runtime (paths, app IDs and so on).
Games, Proton, pressure-vessel and the overlay read these. On NixOS they matter for FHS/steam-run wrappers.

| Variable | Value written (if constant) |
|---|---|
| `__GL_SHADER_DISK_CACHE_APP_NAME` | `steamapp_shader_cache` |
| `__GL_SHADER_DISK_CACHE_PATH` |  |
| `__GL_SHADER_DISK_CACHE_READ_ONLY_APP_NAME` | `steam_shader_cache;steamapp_merged_shader_cache` |
| `__GL_SHADER_DISK_CACHE_SKIP_CLEANUP` | `1` |
| `AMD_VK_PIPELINE_CACHE_FILENAME` | `steamapp_shader_cache` |
| `AMD_VK_PIPELINE_CACHE_PATH` |  |
| `AMD_VK_USE_PIPELINE_CACHE` | `1` |
| `BREAKPAD_DUMP_LOCATION` |  |
| `CEF_CRASH_REPORTER_PRODUCT_VERSION` |  |
| `CEF_CRASH_REPORTER_SERVER_URL` | `https://crash.steampowered.com/submit` |
| `DISABLE_LAYER_AMD_SWITCHABLE_GRAPHICS_1` | `1` |
| `DISPLAY` |  |
| `ENABLE_VK_LAYER_VALVE_steam_fossilize_1` | `1` |
| `ENABLE_VK_LAYER_VALVE_steam_overlay_1` | `1` |
| `EnableConfiguratorSupport` |  |
| `FOSSILIZE_APPLICATION_INFO_FILTER_PATH` |  |
| `GameOverlay_BlockOculusSDK` |  |
| `GameOverlay_CompatMode` |  |
| `GameOverlay_TestMode` | `1` |
| `HOST_LC_ALL` |  |
| `http_proxy` |  |
| `https_proxy` |  |
| `IgnoreChildProcesses` | `1` |
| `LC_ALL` | `C` |
| `MESA_DISK_CACHE_READ_ONLY_FOZ_DBS` |  |
| `MESA_DISK_CACHE_SINGLE_FILE` | `1` |
| `MESA_GLSL_CACHE_DIR` |  |
| `MESA_GLSL_CACHE_MAX_SIZE` | `5G` |
| `MESA_SHADER_CACHE_DIR` |  |
| `MESA_SHADER_CACHE_MAX_SIZE` | `5G` |
| `MESA_VK_TRACE` | `rgp` |
| `MESA_VK_TRACE_TRIGGER` | `/tmp/rgp.trigger` |
| `no_proxy` | `localhost,127.0.0.0/8` |
| `PATH` |  |
| `PRESSURE_VESSEL_BATCH` | `1` |
| `PROTON_CRASH_REPORT_DIR` | `/tmp/proton_crashreports` |
| `PROTON_HIDE_PROCESS_WINDOW` | `1` |
| `PROTON_REMOTE_DEBUG_CMD` |  |
| `PROTON_WAIT_ATTACH` |  |
| `RADV_DEBUG` |  |
| `SDL_ENABLE_STEAM_SCREEN_KEYBOARD` | `1` |
| `SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD` | `1` |
| `SDL_GAMECONTROLLER_IGNORE_DEVICES` |  |
| `SDL_GAMECONTROLLER_USE_BUTTON_LABELS` |  |
| `SDL_JOYSTICK_HIDAPI_STEAMXBOX` | `0` |
| `STEAM_CLIENT_CONFIG_FILE` |  |
| `STEAM_COMPAT_APP_ID` | `0` |
| `STEAM_COMPAT_CLIENT_INSTALL_PATH` |  |
| `STEAM_COMPAT_CONFIG` |  |
| `STEAM_COMPAT_DATA_PATH` |  |
| `STEAM_COMPAT_FLAGS` | `search-cwd` |
| `STEAM_COMPAT_INSTALL_PATH` |  |
| `STEAM_COMPAT_LAUNCHER_SERVICE` |  |
| `STEAM_COMPAT_LIBRARY_PATHS` |  |
| `STEAM_COMPAT_MEDIA_PATH` |  |
| `STEAM_COMPAT_MOUNTS` |  |
| `STEAM_COMPAT_PROTON` | `1` |
| `STEAM_COMPAT_SHADER_PATH` |  |
| `STEAM_COMPAT_TOOL_PATHS` |  |
| `STEAM_COMPAT_TRACING` | `1` |
| `STEAM_COMPAT_TRANSCODED_MEDIA_PATH` |  |
| `STEAM_FOSSILIZE_DUMP_PATH` |  |
| `STEAM_FOSSILIZE_DUMP_PATH_READ_ONLY` |  |
| `STEAM_GAME_PIDS` |  |
| `STEAM_LAUNCH_WRAPPER_SCOPE` | `1` |
| `STEAM_OVERLAY_DISABLE_WAIT_FOR_CEF_FRAME` | `1` |
| `STEAM_OVERLAY_LOGGING_FLUSH` | `1` |
| `STEAM_OVERLAY_WINDOW_BLACKLIST` |  |
| `SteamAppId` |  |
| `SteamAppUser` |  |
| `SteamClientLaunch` | `1` |
| `SteamDeck` | `1` |
| `SteamDisableOverlayDPIScaling` | `1` |
| `SteamEnv` | `1` |
| `SteamGameId` |  |
| `SteamGamepadUI` | `1` |
| `SteamGenericControllers` |  |
| `SteamNoOverlayUI` | `1` |
| `SteamOS` | `1` |
| `SteamOverlayGameId` |  |
| `SteamRealm` |  |
| `SteamStreaming` | `1` |
| `SteamStreamingAllowGameVsync` |  |
| `SteamStreamingAudio` |  |
| `SteamStreamingForceWindowedD3D9` |  |
| `SteamStreamingInput` |  |
| `SteamStreamingMaximumResolution` | `0x0` |
| `SteamStreamingVideo` | `1` |
| `SteamStreamingVideoDisableVSync` |  |
| `SteamStreamingVRPairedInvite` |  |
| `SteamStreamingVRTransitionInvite` |  |
| `SteamTenfoot` | `1` |
| `SteamTraceEnter` |  |
| `SteamTraceExit` |  |
| `SteamTraceModule` |  |
| `SteamUniverse` |  |
| `SteamUserDataFolder` |  |
| `STEAMVIDEOTOKEN` |  |
| `SteamVirtualGamepadInfo` |  |
| `SteamVirtualGamepadInfo_Proton` |  |
| `StreamForOpenVR` |  |
| `StreamingTargetAudioChannels` |  |
| `XR_RUNTIME_JSON` |  |
