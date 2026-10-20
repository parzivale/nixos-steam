# SDL hints

> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

**50** SDL3 hints that Steam sets or reads internally (`SDL_SetHint` and wrappers). Every SDL hint can
also be overridden with an environment variable of the same name, which makes them user-configurable.

| Hint | Access | Value set | Binaries |
|---|---|---|---|
| `SDL_APP_NAME` | set; set (wrapper) | `Steam` | steamui.so, streaming_client |
| `SDL_AUDIO_DEVICE_SAMPLE_FRAMES` | set |  | streaming_client |
| `SDL_AUDIO_DEVICE_STREAM_NAME` | set | `Audio recorder` / `Game streaming client (microphone)` / `Game streaming client (playback)` | steamui.so, streaming_client |
| `SDL_AUDIO_DEVICE_STREAM_ROLE` | set | `Game` / `GameChat` | steamui.so, streaming_client |
| `SDL_ENABLE_GTK` | set | `0` | steamui.so |
| `SDL_GAMECONTROLLERCONFIG` | read; set |  | steamui.so |
| `SDL_JOYSTICK_GAMEINPUT` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI` | set | `1` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_COMBINE_JOY_CONS` | set |  | steamui.so |
| `SDL_JOYSTICK_HIDAPI_GAMECUBE` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_JOYCON_HOME_LED` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_PS4` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_PS5` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_STEAM` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_STEAMXBOX` | set | `1` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_SWITCH` | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_XBOX` | set | `0` | streaming_client |
| `SDL_KMSDRM_REQUIRE_DRM_MASTER` | set | `0` | streaming_client |
| `SDL_MAC_REGISTER_ACTIVATION_HANDLERS` | set | `0` | steamwebhelper |
| `SDL_MOUSE_AUTO_CAPTURE` | set | `0` | steamwebhelper |
| `SDL_MOUSE_NORMAL_SPEED_SCALE` | set |  | streaming_client |
| `SDL_MOUSE_RELATIVE_SPEED_SCALE` | set |  | streaming_client |
| `SDL_MOUSE_TOUCH_EVENTS` | set | `0` | streaming_client |
| `SDL_NO_SIGNAL_HANDLERS` | set | `1` | steamui.so |
| `SDL_OPENVR_CURSOR_WIDTH` | set | `0.06` | streaming_client |
| `SDL_OPENVR_INPUT_PROFILE` | set |  | streaming_client |
| `SDL_OPENVR_LIBRARY` | set | `libopenvr_api.so` | streaming_client |
| `SDL_OPENVR_OVERLAY_FLAGS` | set |  | streaming_client |
| `SDL_OPENVR_OVERLAY_NAME` | set | `steamlink_openvr` | streaming_client |
| `SDL_OPENVR_OVERLAY_PANEL_WIDTH` | set | `2.75` | streaming_client |
| `SDL_OPENVR_WINDOW_ICON_OVERRIDE` | set | `false` | streaming_client |
| `SDL_PEN_MOUSE_EVENTS` | set | `0` | streaming_client |
| `SDL_PEN_TOUCH_EVENTS` | set | `0` | streaming_client |
| `SDL_RENDER_DRIVER` | read; set | `vulkan` / `opengles2` / `opengl` / `direct3d11` / `direct3d` | streaming_client |
| `SDL_RENDER_OPENGL_NV12_RG_SHADER` | set | `1` / `0` | streaming_client |
| `SDL_SCREENSAVER_INHIBIT_ACTIVITY_NAME` | set; set (wrapper) | `Downloading` / `Game streaming (server)` / `Game streaming client` | steamui.so, streaming_client |
| `SDL_TIMER_RESOLUTION` | set | `0` | steamui.so, steamwebhelper |
| `SDL_TOUCH_MOUSE_EVENTS` | set | `0` | streaming_client |
| `SDL_TV_REMOTE_AS_JOYSTICK` | set | `0` | streaming_client |
| `SDL_VIDEO_ALLOW_SCREENSAVER` | set | `1` | gldriverquery, steamui.so, steamwebhelper |
| `SDL_VIDEO_DRIVER` | set | `x11` / `wayland` / `openvr` | streaming_client |
| `SDL_VIDEO_FORCE_EGL` | read; set | `1` / `0` | streaming_client |
| `SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS` | set | `0` | steamwebhelper |
| `SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR` | set; set (wrapper) | `0` | steamui.so, steamwebhelper |
| `SDL_VIDEO_X11_SCALING_FACTOR` | set | `1.0` | steamui.so, steamwebhelper |
| `SDL_VIDEO_X11_WINDOW_VISUALID` | set; set (wrapper) |  | steamwebhelper, streaming_client |
| `SDL_WINDOW_ACTIVATE_WHEN_SHOWN` | set (wrapper) | `0` | steamwebhelper |
| `SDL_WINDOW_RETAIN_CONTENT` | set (wrapper) | `1` | steamwebhelper |
| `SDL_WINDOWS_DETECT_DEVICE_HOTPLUG` | set; set (wrapper) | `0` | steamui.so, steamwebhelper |
| `SDL_WINDOWS_ERASE_BACKGROUND_MODE` | set (wrapper) |  | steamwebhelper |
