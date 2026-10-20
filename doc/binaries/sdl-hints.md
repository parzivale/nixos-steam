# SDL hints

> **What it does** is written from how the option is used in the code (strings and log messages near each
> read site, related options, Valve help). The confidence tag *(high/medium/low)* follows each inferred description.
> Untagged descriptions restate Valve's own help text.
>
> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

**50** SDL3 hints that Steam sets or reads internally (`SDL_SetHint` and wrappers). Every SDL hint can
also be overridden with an environment variable of the same name, which makes them user-configurable.

| Hint | What it does | Access | Value set | Binaries |
|---|---|---|---|---|
| `SDL_APP_NAME` | Steam sets it to 'Steam' (or the streaming client's name). SDL uses it as the application name that the audio server (PulseAudio/PipeWire) and the screensaver inhibitor show. *(high)* | set; set (wrapper) | `Steam` | steamui.so, streaming_client |
| `SDL_AUDIO_DEVICE_SAMPLE_FRAMES` | The streaming client sets this hint to request an audio buffer size in sample frames, to keep Remote Play audio latency low. *(medium)* | set |  | streaming_client |
| `SDL_AUDIO_DEVICE_STREAM_NAME` | Name given to each audio stream in the sound server's mixer: 'Game streaming client (playback)' and '(microphone)' in the streaming client, and 'Audio recorder' for the recording or voice capture in steamui. *(high)* | set | `Audio recorder` / `Game streaming client (microphone)` / `Game streaming client (playback)` | steamui.so, streaming_client |
| `SDL_AUDIO_DEVICE_STREAM_ROLE` | Media role given to Steam's audio streams. 'Game' is used for streamed game audio and 'GameChat' for microphone/voice, so PipeWire/PulseAudio policies can route or duck them. *(high)* | set | `Game` / `GameChat` | steamui.so, streaming_client |
| `SDL_ENABLE_GTK` | steamui sets it to 0 before SDL_Init so SDL3 does not load or initialize GTK (used for tray/menu integration) inside the Steam process. *(high)* | set | `0` | steamui.so |
| `SDL_GAMECONTROLLERCONFIG` | SDL controller mapping database string. steamui reads and sets it to add Steam's own mappings (entries with crc and sdl://<index> identifiers) for controllers it hands to SDL. *(medium)* | read; set |  | steamui.so |
| `SDL_JOYSTICK_GAMEINPUT` | The streaming client sets it to 0, disabling SDL's Windows GameInput joystick backend. This only matters on Windows builds. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI` | The streaming client sets it to 1 so SDL uses its HIDAPI drivers to read controllers directly for Remote Play input. *(high)* | set | `1` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_COMBINE_JOY_CONS` | steamui sets it from the user's controller setting controller_combine_nintendo_joycons, to choose whether a left and right Joy-Con pair act as one controller. *(high)* | set |  | steamui.so |
| `SDL_JOYSTICK_HIDAPI_GAMECUBE` | The streaming client sets it to 0 when streaming support for GameCube adapters is turned off ("Turning off streaming support for GameCube controllers"); the device is then shared over USB instead. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_JOYCON_HOME_LED` | The streaming client sets it to 0 so SDL does not turn on the Joy-Con Home-button LED. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_PS4` | The streaming client sets it to 0 when HIDAPI support for PS4 controllers is turned off for streaming, for example when the device is passed through via USB sharing instead. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_PS5` | The streaming client sets it to 0 when HIDAPI support for PS5 controllers is turned off for streaming, for example when the controller is shared over USB instead. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_STEAM` | The streaming client sets it to 0 so SDL's HIDAPI Steam Controller driver is not used. Steam itself owns Steam Controllers. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_STEAMXBOX` | The streaming client sets it to 1, enabling SDL's HIDAPI driver for Steam's virtual Xbox-style controllers in the streaming client. *(medium)* | set | `1` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_SWITCH` | The streaming client sets it to 0 when HIDAPI support for Nintendo Switch controllers is turned off for streaming, for example when they are shared over USB instead. *(high)* | set | `0` | streaming_client |
| `SDL_JOYSTICK_HIDAPI_XBOX` | The streaming client sets it to 0 when HIDAPI support for Xbox controllers is turned off for streaming, for example when they are shared over USB instead. *(high)* | set | `0` | streaming_client |
| `SDL_KMSDRM_REQUIRE_DRM_MASTER` | The streaming client sets it to 0 so SDL's KMSDRM video backend can start without DRM master. This lets it run on a console/VT, for example a Steam Link-style device, while another process owns the display. *(high)* | set | `0` | streaming_client |
| `SDL_MAC_REGISTER_ACTIVATION_HANDLERS` | steamwebhelper sets it to 0 so SDL does not register macOS app-activation handlers. This has no effect on Linux; the code is shared with macOS. *(high)* | set | `0` | steamwebhelper |
| `SDL_MOUSE_AUTO_CAPTURE` | steamwebhelper sets it to 0 so SDL does not grab the mouse automatically while a button is held over a browser window, which avoids stuck pointer grabs in Steam UI windows and context menus. *(high)* | set | `0` | steamwebhelper |
| `SDL_MOUSE_NORMAL_SPEED_SCALE` | The streaming client sets it, as a float formatted %.2f, to scale absolute mouse motion according to the user's streaming mouse-speed setting. *(medium)* | set |  | streaming_client |
| `SDL_MOUSE_RELATIVE_SPEED_SCALE` | The streaming client sets it, as a float formatted %.2f, to scale relative (captured) mouse motion sent to the streamed game. *(medium)* | set |  | streaming_client |
| `SDL_MOUSE_TOUCH_EVENTS` | The streaming client sets it to 0 so SDL does not generate synthetic touch events from the mouse. Each input type is forwarded to the host as itself. *(high)* | set | `0` | streaming_client |
| `SDL_NO_SIGNAL_HANDLERS` | steamui sets it to 1 so SDL does not install SIGINT/SIGTERM handlers; Steam handles signals itself. *(high)* | set | `1` | steamui.so |
| `SDL_OPENVR_CURSOR_WIDTH` | The streaming client's OpenVR video mode sets it to 0.06, the size of the cursor drawn on the VR overlay panel. *(medium)* | set | `0.06` | streaming_client |
| `SDL_OPENVR_INPUT_PROFILE` | The streaming client's OpenVR mode sets it to its action manifest, resource/streaming_client/sdloverlay_actions.json, so VR controller input maps to the streaming overlay. *(high)* | set |  | streaming_client |
| `SDL_OPENVR_LIBRARY` | In --openvr mode the streaming client sets it to libopenvr_api.so, the OpenVR library that SDL's OpenVR video driver loads. *(high)* | set | `libopenvr_api.so` | streaming_client |
| `SDL_OPENVR_OVERLAY_FLAGS` | The streaming client's OpenVR mode sets it to the flags SDL applies to the VR overlay it creates for the stream. The value is not visible. *(low)* | set |  | streaming_client |
| `SDL_OPENVR_OVERLAY_NAME` | The streaming client sets it to 'steamlink_openvr', the OpenVR overlay key/name for streaming a desktop or game into VR. *(high)* | set | `steamlink_openvr` | streaming_client |
| `SDL_OPENVR_OVERLAY_PANEL_WIDTH` | The streaming client sets it to 2.75, the width in meters of the VR overlay panel that shows the stream. *(high)* | set | `2.75` | streaming_client |
| `SDL_OPENVR_WINDOW_ICON_OVERRIDE` | The streaming client sets it to false, so SDL's OpenVR driver keeps the default overlay thumbnail/icon instead of using the window icon. *(medium)* | set | `false` | streaming_client |
| `SDL_PEN_MOUSE_EVENTS` | The streaming client sets it to 0 so pen input does not also produce synthetic mouse events. *(high)* | set | `0` | streaming_client |
| `SDL_PEN_TOUCH_EVENTS` | The streaming client sets it to 0 so pen input does not also produce synthetic touch events. *(high)* | set | `0` | streaming_client |
| `SDL_RENDER_DRIVER` | The streaming client sets the SDL renderer from its options (--opengl, --opengles2, --d3d9 or --d3d11, defaulting to vulkan; opengles2 for OpenVR). Users can also set it to force a renderer. HDR output requires the Vulkan renderer. *(high)* | read; set | `vulkan` / `opengles2` / `opengl` / `direct3d11` / `direct3d` | streaming_client |
| `SDL_RENDER_OPENGL_NV12_RG_SHADER` | The streaming client sets it to 1 or 0 to choose the SDL GL shader path for NV12 video textures: an RG-format UV plane versus separate textures, depending on the EGL/dmabuf frame import. *(medium)* | set | `1` / `0` | streaming_client |
| `SDL_SCREENSAVER_INHIBIT_ACTIVITY_NAME` | Reason string SDL passes when it inhibits the screensaver (D-Bus inhibit). Steam uses 'Downloading', 'Game streaming (server)' or 'Game streaming client', so desktop power or idle UIs show why Steam keeps the screen awake. *(high)* | set; set (wrapper) | `Downloading` / `Game streaming (server)` / `Game streaming client` | steamui.so, streaming_client |
| `SDL_TIMER_RESOLUTION` | steamui and steamwebhelper set it to 0 so SDL does not raise the system timer resolution. This is Windows-only and has no effect on Linux. *(high)* | set | `0` | steamui.so, steamwebhelper |
| `SDL_TOUCH_MOUSE_EVENTS` | The streaming client sets it to 0 so touches do not also generate synthetic mouse events; touch is forwarded to the host as touch. *(high)* | set | `0` | streaming_client |
| `SDL_TV_REMOTE_AS_JOYSTICK` | The streaming client sets it to 0 so TV remotes (Android TV builds) are not exposed as joysticks. *(high)* | set | `0` | streaming_client |
| `SDL_VIDEO_ALLOW_SCREENSAVER` | steamui, steamwebhelper and gldriverquery set it to 1 so opening SDL windows does not disable the screensaver. Steam inhibits it explicitly only when needed, for example while downloading or streaming. *(high)* | set | `1` | gldriverquery, steamui.so, steamwebhelper |
| `SDL_VIDEO_DRIVER` | The streaming client sets the SDL video backend to x11, wayland, or openvr in --openvr mode. Users can set it in the environment to force a backend; steam.sh rewrites a plain 'wayland' to 'wayland,x11'. *(high)* | set | `x11` / `wayland` / `openvr` | streaming_client |
| `SDL_VIDEO_FORCE_EGL` | The streaming client sets it to 1 or 0, choosing EGL instead of GLX on X11 for its OpenGL renderers. EGL is needed for dmabuf/EGLImage zero-copy video frames. *(high)* | read; set | `1` / `0` | streaming_client |
| `SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS` | steamwebhelper sets it to 0 so fullscreen Steam windows, such as Big Picture, are not minimized when they lose focus. *(high)* | set | `0` | steamwebhelper |
| `SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR` | steamui and steamwebhelper set it to 0 so SDL does not ask the X compositor to unredirect Steam windows (_NET_WM_BYPASS_COMPOSITOR), which keeps transparency and compositing working. *(high)* | set; set (wrapper) | `0` | steamui.so, steamwebhelper |
| `SDL_VIDEO_X11_SCALING_FACTOR` | Set to 1.0 by steamui and steamwebhelper so SDL itself does no X11 content scaling; Steam/CEF handle DPI scaling themselves. *(high)* | set | `1.0` | steamui.so, steamwebhelper |
| `SDL_VIDEO_X11_WINDOW_VISUALID` | Set to a specific X visual ID (%lu) before window creation, so SDL creates the webhelper composer or streaming window with a visual that matches the GL/EGL config, for example an ARGB visual for transparency. *(high)* | set; set (wrapper) |  | steamwebhelper, streaming_client |
| `SDL_WINDOW_ACTIVATE_WHEN_SHOWN` | steamwebhelper sets it to 0 so showing a Steam window does not steal focus. With multiple Xwaylands, Steam manages focus itself through XSetInputFocus. *(high)* | set (wrapper) | `0` | steamwebhelper |
| `SDL_WINDOW_RETAIN_CONTENT` | steamwebhelper sets it to 1, a hint to keep window contents across hide and show or resize. It is related to the composer mode (OpenGL/Gamescope). *(medium)* | set (wrapper) | `1` | steamwebhelper |
| `SDL_WINDOWS_DETECT_DEVICE_HOTPLUG` | Set to 0 by steamui and steamwebhelper, which stops SDL's Windows device-hotplug window. This is Windows-only and has no effect on Linux. *(high)* | set; set (wrapper) | `0` | steamui.so, steamwebhelper |
| `SDL_WINDOWS_ERASE_BACKGROUND_MODE` | steamwebhelper sets it to always or never, controlling whether SDL erases a new window's background on Windows. This is Windows-only and has no effect on Linux. *(high)* | set (wrapper) |  | steamwebhelper |
