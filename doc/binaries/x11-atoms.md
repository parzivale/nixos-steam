# X11 atoms and gamescope properties

> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

**60** `STEAM_*`/`GAMESCOPE_*` X11 atoms that the client interns or sets. These are how Steam talks to
gamescope (Steam Deck / SteamOS game mode) and to the window manager: frame limits, VRR, HDR, blur,
ReShade effects and so on. Values are set at runtime.

| Atom / property | Binaries |
|---|---|
| `GAMESCOPE_ALLOW_TEARING` | steamui.so |
| `GAMESCOPE_BLUR_FADE_DURATION` | steamui.so |
| `GAMESCOPE_BLUR_MODE` | steamui.so |
| `GAMESCOPE_BLUR_RADIUS` | steamui.so |
| `GAMESCOPE_COLOR_APP_WANTS_HDR_FEEDBACK` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_COLOR_MANAGEMENT_DISABLE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_COLOR_MURA_CORRECTION_DISABLED` | steamui.so |
| `GAMESCOPE_COLOR_NIGHT_MODE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_COLOR_SDR_GAMUT_WIDENESS` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_COMPOSITE_DEBUG` | steamui.so |
| `GAMESCOPE_COMPOSITE_FORCE` | steamui.so |
| `GAMESCOPE_CURSOR_VISIBLE_FEEDBACK` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DEBUG_HDR_HEATMAP` | steamui.so |
| `GAMESCOPE_DISPLAY_DYNAMIC_REFRESH_BASED_ON_GAME_PRESENCE` | steamui.so |
| `GAMESCOPE_DISPLAY_FORCE_INTERNAL` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DISPLAY_HDR_ENABLED` | steamui.so |
| `GAMESCOPE_DISPLAY_IS_EXTERNAL` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DISPLAY_MODE_LIST_EXTERNAL` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DISPLAY_MODE_NUDGE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DISPLAY_SUPPORTS_HDR` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DISPLAY_VIRTUAL_WHITE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DYNAMIC_REFRESH` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DYNAMIC_REFRESH_EXTERNAL` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_DYNAMIC_REFRESH_IN_STEAM` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_FOCUSABLE_APPS` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_FOCUSABLE_WINDOWS` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_FOCUSED_APP` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_FOCUSED_WINDOW` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_FPS_LIMIT` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_FSR_SHARPNESS` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_HDR_INPUT_GAIN` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_HDR_ON_SDR_TONEMAP_OPERATOR` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_HDR_OUTPUT_FEEDBACK` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_INPUT_COUNTER` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_INTERNAL_DISPLAY_BRIGHTNESS` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_NEW_SCALING_FILTER` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_NEW_SCALING_SCALER` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_PID` | steamwebhelper |
| `GAMESCOPE_RESHADE_EFFECT` | steamui.so |
| `GAMESCOPE_RESHADE_TECHNIQUE_IDX` | steamui.so |
| `GAMESCOPE_SDR_INPUT_GAIN` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_SDR_ON_HDR_CONTENT_BRIGHTNESS` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_VIEWPORT_SUPPORTED` | steamui.so |
| `GAMESCOPE_VROVERLAY_FORWARDING` | steamui.so |
| `GAMESCOPE_VRR_CAPABLE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_VRR_ENABLED` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_VRR_FEEDBACK` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPE_XWAYLAND_MODE_CONTROL` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `GAMESCOPECTRL_REQUEST_SCREENSHOT` | steamui.so |
| `STEAM_GAME` | steamwebhelper, streaming_client |
| `STEAM_GAMES_RUNNING` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_GAMESCOPE_VIEWPORT` | steamwebhelper |
| `STEAM_GAMESCOPE_VIEWPORT_TARGET` | steamwebhelper |
| `STEAM_GAMESCOPE_VROVERLAY_TARGET` | steamwebhelper |
| `STEAM_INPUT_FOCUS` | steamwebhelper, vgui2_s.so |
| `STEAM_NOTIFICATION` | steamwebhelper |
| `STEAM_OVERLAY` | steamwebhelper, vgui2_s.so |
| `STEAM_SCREEN_MAGNIFICATION` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_SCREEN_SCALE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `STEAM_TOUCH_CLICK_MODE` | steamclient.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
