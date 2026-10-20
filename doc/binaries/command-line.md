# Command-line switches

> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

Every command-line switch the client binaries test for: **253** switches, **148** of which carry a
help string that Valve registered through `SteamStdLib::CCommandLineParam(name, help)`.

You pass these to the `steam` launcher (e.g. `steam -dev -console`). `steam.sh` and the bootstrapper forward
unrecognised arguments to the client. Read-method legend:

* **registered (CCommandLineParam)**: declared with help text. These are the switches Valve formally documents internally.
* **exists / value**: `Plat_CommandLineParamExists` / `Plat_CommandLineParamValue` (tier0). `value` switches take an argument (`-switch <value>`).
* **internal parser**: a private argv parser, e.g. in the `steam` bootstrapper.
* **checked (virtual ICommandLine call, inferred)**: a `"-switch"` literal passed to a virtual `ICommandLine` method (`FindParm`/`ParmValue`). The method is inferred from the call shape.
* **compared against argv (inferred)**: a literal compared with `strcmp`-style functions, typically in argv loops.

The analysis also found these protocol URLs used as launch arguments: `steam://open/bigpicture`, `steambeta://open/bigpicture`.


| Switch | Description (Valve help text) | How it is read | Binaries |
|---|---|---|---|
| `-accesscode` |  | registered (CCommandLineParam) | steamui.so |
| `-all_languages` |  | exists | vgui2_s.so |
| `-allosarches` |  | internal parser | gamelauncher, steam |
| `-allosvers` |  | internal parser | gamelauncher, steam |
| `-allowbrowserviewunderlays` | Allow browser view underlays | registered (CCommandLineParam) | steamwebhelper |
| `-allowremotediscovery` |  | exists | steamclient.so |
| `-alwaysrelaunch` |  | internal parser | gamelauncher, steam |
| `-applaunch` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-arch` |  | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-batterytestmode` | rapidly cycle battery percentages for testing | registered (CCommandLineParam) | steamclient.so |
| `-bigpicture` | Start in Steam Big Picture mode | registered (CCommandLineParam) | steamui.so |
| `-bootreserve` |  | registered (CCommandLineParam) | steamclient.so |
| `-bootreservesizemb` |  | registered (CCommandLineParam) | steamclient.so |
| `-bootstrapperproxy` |  | internal parser | gamelauncher, steam |
| `-buildid` | Build identifier for crash reporting | internal parser | steamsysinfo |
| `-cafeapplaunch` | Launch apps in a cyber cafe context | registered (CCommandLineParam) | steamclient.so |
| `-candidates` | Show libjingle candidates for local connection as they are processed | registered (CCommandLineParam) | steamclient.so |
| `-ccsyntax` | Spew details about the localized strings we load | registered (CCommandLineParam) | vgui2_s.so |
| `-cef-allow-browser-underlays` | Allow webhelper to create BrowserView underlays | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-breakpad` | disables breakpad in crash dumps | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-browser-underlays` | Disables support for BrowserView underlays | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-gpu` | Disable GPU usage in CEF (force software rendering/compositing) | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-gpu-compositing` | Disable GPU accelerated compositing in browsers | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-gpu-sandbox` | disables CEF gpu-process sandbox | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-hang-timeouts` | disables GPU and renderer hang timeouts | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-hevc` | Disables hevc support | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-js-logging` | disables console and log file logging of JS console events | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-logging` | disables logging from CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-occlusion` | disables Chromium window occlusion testing | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-renderer-restart` | Disable auto-restart of renderer process for existing browsers | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-safe-shutdown-workaround` | Disable the usage of the safe browser shutdown workaround for Linux+NV | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-sandbox` | disables sandboxing in CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-seccomp-sandbox` | disables CEF seccomp-bpf sandbox on Linux | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-site-isolation` | disables per-process site-isolation | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-touch-focus-workaround` | Disable touch input browser focus workaround | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-disable-xcomposite-workaround` | Disable the glcomposer workaround applied to some video drivers | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-enable-debugging` | enables Chromium remote debugging, defaulting to localhost:8080 | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-enable-gpu-debugging` | Enable GPU debugging in Chromium, costs a glGetError() call after every command | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-enable-low-delay-live-stream` | Reduce buffering requirements for live video playback | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-enable-vaapi` | Enable VA-API video decoding on Linux | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-accessibility` | Force enable CEF accessibility features | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-browser-underlays` | Force support for BrowserView underlays | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-gpu` | Force enable GPU acceleration | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-gpu-blocklist` | Force enable GPU blocklist | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-hw-video-decode` | Force enable HW accelerated video decoding | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-occlusion` | force enable Chromium window occlusion testing | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-opaque-backgrounds` | Force the usage of opaque backgrounds for CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-force-sandbox` | force sandboxing in CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-full-memory-crash-report` | enables full crash dumps | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-log-sandbox` | Enable sandbox logging in CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-use-vulkan` | Use vulkan ANGLE backend | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-verbose-js-logging` | enables verbose logging of JS console events | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-verbose-logging` | enables verbose logging from CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-cef-verbose-modules` | enables verbose logging for specific CEF modules | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-child-update-ui` |  | internal parser | gamelauncher, steam |
| `-child-update-ui-socket` |  | internal parser | gamelauncher, steam |
| `-chromeos` |  | exists | libtier0_s.so |
| `-chromeosverbose` |  | exists; internal parser | chromehtml.so, crashhandler.so, filesystem_stdio.so, friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, libvstdlib_s.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `-clearbeta` |  | internal parser | gamelauncher, steam |
| `-clientbeta` | Overrides Steam client beta for single session | exists; internal parser | chromehtml.so, crashhandler.so, filesystem_stdio.so, friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, libvstdlib_s.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `-compat` |  | exists | vgui2_s.so |
| `-compat-disable-filtering` | Disable filtering of normally unlisted runtimes. | registered (CCommandLineParam) | steamclient.so |
| `-compat-force-slr` | Force enable/disable using SLR 1.0 by default over legacy LD_* setup. | registered (CCommandLineParam) | steamclient.so |
| `-complete_install_via_http` | Run installation completion over HTTP by default | registered (CCommandLineParam) | steamclient.so |
| `-console` |  | registered (CCommandLineParam) | steamui.so |
| `-controllertypeoverride` |  | registered (CCommandLineParam) | steamclient.so |
| `-debug_steamapi` | enables logging of Steam API functions | registered (CCommandLineParam) | steamclient.so |
| `-debugamf` | Enable AMF video encoding debug log | registered (CCommandLineParam) | steamui.so |
| `-debugbreak` |  | exists; internal parser | crashhandler.so, gamelauncher, libtier0_s.so, libvideo.so, steam, steam_monitor, steamservice.so, steamsysinfo, streaming_client |
| `-debugoutputlogs` |  | internal parser; registered (CCommandLineParam) | chromehtml.so, gamelauncher, gameoverlayui.so, steam, steamclient.so, steamsysinfo, steamui.so, steamwebhelper |
| `-deckard` |  | exists | libtier0_s.so |
| `-delaypageload` |  | registered (CCommandLineParam) | steamwebhelper |
| `-dev` | enables developer spew | exists; internal parser; registered (CCommandLineParam) | chromehtml.so, friendsui.so, gamelauncher, gameoverlayui.so, steam, steamclient.so, steamui.so |
| `-devsites` | Use local dev websites | internal parser; registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamclient.so, steamui.so, steamwebhelper, streaming_client |
| `-devsiteshost` | Pass the hostname, will generate dev site domains like store.{hostname}.steam.dev | internal parser; registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamclient.so, steamui.so, steamwebhelper, streaming_client |
| `-devtools-port` |  | value | chromehtml.so, steamclient.so |
| `-disable-libusb` | Disable support for controllers requiring exclusive USB access | registered (CCommandLineParam) | steamclient.so |
| `-disable-overlay-gpu-pri` | Disables setting webhelper GPU pri high when overlay visible | registered (CCommandLineParam) | steamclient.so |
| `-disable-overlay-wait-for-cef-frame` | Disables waiting for pending CEF frame render when overlay visible. | registered (CCommandLineParam) | steamclient.so |
| `-disable-winh264` | disables loading winh264.dll | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-disable_broadcast_webrtc` |  | exists | steamclient.so |
| `-disable_safe_shutdown_workaround` |  | exists | steamwebhelper |
| `-disablehighdpi` | disables high-DPI support in CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-disablejslogging` | disable file and console logging of JS console events | registered (CCommandLineParam) | steamwebhelper |
| `-disablelauncherservice` | Disable steam-runtime-launcher-service process. | registered (CCommandLineParam) | steamclient.so |
| `-disablepartnerlicenses` | disable automatically granted partner licenses - impacts all web and client sessions, don't try to use with multiple active steam clients! | registered (CCommandLineParam) | steamclient.so |
| `-disablerendererrestart` | disable auto-restarting a renderer for an existing browser | registered (CCommandLineParam) | steamwebhelper |
| `-disabletouchfocusworkaround` | disable touch input browser focus workaround | registered (CCommandLineParam) | steamwebhelper |
| `-disablevulkanlayer` | Prevents loading of Vulkan layer if overlay disabled | registered (CCommandLineParam) | steamclient.so |
| `-display-scale=` |  | value | vgui2_s.so |
| `-download` |  | internal parser | gamelauncher, steam |
| `-drop` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-dumpvideostream` | Dump the game stream as an elementary video file | registered (CCommandLineParam) | steamui.so |
| `-enable-desktop-gl-fallback` |  | registered (CCommandLineParam) | steamui.so |
| `-enable-devkit` | Enable devkit functionality | registered (CCommandLineParam) | steamui.so |
| `-enable-keyring` | enables CEF usage of the Chromium keyring | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-enable-libusb` | Enable support for controllers requiring exclusive USB access | registered (CCommandLineParam) | steamclient.so |
| `-enable-libusb-gamecube` | Enable support for Nintendo GameCube adapters in Wii-U mode | registered (CCommandLineParam) | steamclient.so |
| `-exitsteam` |  | compared against argv (V_strnicmp, inferred); internal parser | gamelauncher, steam, steamui.so |
| `-failsystemcheck` |  | internal parser | gamelauncher, steam |
| `-flushconfig` |  | registered (CCommandLineParam) | steamui.so |
| `-force-no-dbus-simulate-user-activity` |  | registered (CCommandLineParam) | steamclient.so, steamui.so |
| `-force-oobe-stage1` | Force show stage1 oobe | registered (CCommandLineParam) | steamui.so |
| `-force-oobe-stage2` | Force show stage2 oobe | registered (CCommandLineParam) | steamui.so |
| `-forcebrowserviewunderlays` | Force enable browser view underlays | registered (CCommandLineParam) | steamwebhelper |
| `-forcecontrollerappid` | Force a Specific AppID for Steam Controller Config - Prevents context/app switching from changing configuration | registered (CCommandLineParam) | steamui.so |
| `-forcedeckcontroller` |  | exists; registered (CCommandLineParam) | steamclient.so |
| `-forceguiupdater` |  | internal parser | gamelauncher, steam |
| `-forcemanifestsuffix` |  | internal parser | gamelauncher, steam |
| `-forcepackagedownload` |  | internal parser | gamelauncher, steam |
| `-forcesteamupdate` |  | internal parser | gamelauncher, steam |
| `-forceunsupportedos` |  | internal parser | gamelauncher, steam |
| `-foreground` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-friendsui` |  | registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamclient.so, steamui.so |
| `-fs_log` | Log file system accesses | internal parser; registered (CCommandLineParam) | filesystem_stdio.so, gamelauncher, steam |
| `-fs_logbins` | Log the binaries we load during operation | internal parser; registered (CCommandLineParam) | filesystem_stdio.so, gamelauncher, steam |
| `-fs_target` | Set target syntax | internal parser; registered (CCommandLineParam) | filesystem_stdio.so, gamelauncher, steam |
| `-full_memory_dump` |  | internal parser | gamelauncher, steam |
| `-fullscreen` | Set BPM to fullscreen | registered (CCommandLineParam) | steamui.so |
| `-fullscreenopengl` | Use the full screen OpenGL render for the UI | registered (CCommandLineParam) | steamui.so |
| `-gameid` |  | exists | gameoverlayui.so |
| `-gameidlaunch` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-gameinput` | Use Microsoft GameInput for controller support | registered (CCommandLineParam) | steamclient.so |
| `-gamepadui` | Start in gamepadui mode | registered (CCommandLineParam) | steamui.so |
| `-hardware-updater` |  | registered (CCommandLineParam) | steamui.so |
| `-holo` |  | exists | libtier0_s.so |
| `-hometest` |  | exists | steamui.so |
| `-html-enable-tooltips` | Show browser tooltips | registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamui.so |
| `-html-perf-monitor` | Draws html perf data | registered (CCommandLineParam) | chromehtml.so, friendsui.so, gameoverlayui.so, steamclient.so, steamui.so |
| `-ifrunning` |  | compared against argv (V_strnicmp, inferred); internal parser | gamelauncher, steam, steamui.so |
| `-inf` |  | internal parser | chromehtml.so, friendsui.so, gameoverlayui.so, steamclient.so, steamui.so, steamwebhelper |
| `-inhibitbootstrap` |  | internal parser | gamelauncher, steam |
| `-init_universe` |  | registered (CCommandLineParam) | steamclient.so |
| `-install` |  | compared against argv (V_strnicmp, inferred); exists | steamui.so |
| `-installupdate` |  | internal parser | gamelauncher, steam |
| `-language` | Set Steam client UI language | compared against argv (V_strnicmp, inferred); registered (CCommandLineParam) | steamui.so, vgui2_s.so |
| `-led-enumerate-sysfs-all` | Enumerate all sysfs LED devices | registered (CCommandLineParam) | steamui.so |
| `-log_voice` | writes voice chat data to the logs/voice_log.txt file | registered (CCommandLineParam) | steamclient.so |
| `-logdir` | Directory to store logs | internal parser | steamsysinfo |
| `-login` | Automatically logs in user | registered (CCommandLineParam) | steamui.so |
| `-lognetapi` | logs all P2P networking info to log/netapi_log.txt | registered (CCommandLineParam) | steamclient.so |
| `-longestloc` | Use longest string for each localization token | registered (CCommandLineParam) | steamui.so |
| `-ltp` | use legacy token persistence scheme | registered (CCommandLineParam) | steamclient.so |
| `-manuallyclearframes` | Should the overlay be manually clearing frames to black (because the game doesn't clear the entire screen?) | registered (CCommandLineParam) | gameoverlayui.so |
| `-master_ipc_name_override` |  | internal parser; registered (CCommandLineParam) | gamelauncher, steam, steamui.so |
| `-net_fake_state` | Set initial value for net_fake_state | registered (CCommandLineParam) | steamclient.so |
| `-net_start_wifi_disabled` | Set the initial value for wifi enabled to false.  (Useful when emulating SteamDeck) | registered (CCommandLineParam) | steamclient.so |
| `-no-cef-sandbox` | disables sandboxing in CEF | registered (CCommandLineParam) | chromehtml.so, steamclient.so |
| `-no-child-update-ui` |  | internal parser | gamelauncher, steam |
| `-no-dwrite` | forces vgui to use GDI text even if DWrite support is available | registered (CCommandLineParam) | steamclient.so |
| `-no-hardware-updater` |  | registered (CCommandLineParam) | steamui.so |
| `-no-shared-textures` | forces overlay to avoid sharing texture handles with game process | registered (CCommandLineParam) | steamclient.so |
| `-noassert` |  | exists; internal parser | crashhandler.so, gamelauncher, libtier0_s.so, libvideo.so, steam, steam_monitor, steamservice.so, steamsysinfo, streaming_client |
| `-nobigpicture` | Start in regular mode (force Big Picture mode off) | registered (CCommandLineParam) | steamui.so |
| `-nobootstrapperupdate` |  | internal parser | gamelauncher, steam |
| `-noconsole` |  | registered (CCommandLineParam) | steamui.so |
| `-nocrashdialog` |  | exists; internal parser | crashhandler.so, gamelauncher, libtier0_s.so, libvideo.so, steam, steam_monitor, steamservice.so, steamsysinfo, streaming_client |
| `-nocrashmonitor` |  | registered (CCommandLineParam) | steamclient.so |
| `-nodircheck` |  | internal parser | gamelauncher, steam |
| `-nodpiscale` |  | exists | vgui2_s.so |
| `-nofriendsui` |  | registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamclient.so, steamui.so |
| `-noipv6` |  | exists | steamclient.so |
| `-nojoy` | Disable controller support | internal parser; registered (CCommandLineParam) | steamclient.so, streaming_client |
| `-nojsreload` |  | registered (CCommandLineParam) | steamui.so |
| `-nopcshutdown` | Skip PC power operations | registered (CCommandLineParam) | steamui.so |
| `-norepairfiles` |  | internal parser | gamelauncher, steam |
| `-noshaders` | Disable the shader manager | registered (CCommandLineParam) | steamclient.so |
| `-noverifyfiles` |  | internal parser | gamelauncher, steam |
| `-offlinemode` | Always attempt to start in offline mode | registered (CCommandLineParam) | steamui.so |
| `-openalldevtools` | Open Chrome devtools on launch for every HTML window | exists; registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamui.so |
| `-opendevtools` | Open Chrome devtools for shared JS context (offscreen window) on launch | registered (CCommandLineParam) | friendsui.so, steamclient.so, steamui.so |
| `-opengl` | Use the OpenGL render for the UI | registered (CCommandLineParam) | steamui.so |
| `-openoverlaydevtools` | Open Chrome devtools on creation of any overlay browsers | registered (CCommandLineParam) | friendsui.so, steamui.so |
| `-out-file` | Store the response in a file | internal parser | steamsysinfo |
| `-overlay-gpu-pri-delay` | Set ms delay between overlay GPU priority changes | registered (CCommandLineParam) | steamclient.so |
| `-overlaylogging` | Enables logging from overlay renderer | registered (CCommandLineParam) | steamclient.so |
| `-overlaytestmode` | Forces overlay testmode mode for debugging | registered (CCommandLineParam) | steamclient.so |
| `-overrideminos` |  | internal parser | gamelauncher, steam |
| `-pid` | Pid that we should be watching for | registered (CCommandLineParam) | chromehtml.so, gameoverlayui.so, vgui2_s.so |
| `-pipewire` | Enable PipeWire desktop capture | registered (CCommandLineParam) | steamui.so |
| `-pipewire-dmabuf` | Enable PipeWire desktop capture using DMA-BUF | registered (CCommandLineParam) | steamui.so |
| `-pipewire-fresh-start` | Clear all Pipewire capture tokens and re-prompt user for what to capture | registered (CCommandLineParam) | steamui.so |
| `-pipewire-record-deck-ui` | Record Steam UI elements on SteamDeck | registered (CCommandLineParam) | steamui.so |
| `-pretendeol` |  | registered (CCommandLineParam) | steamui.so |
| `-pretendeol32` |  | registered (CCommandLineParam) | steamui.so |
| `-preventsteamdiscovery` |  | exists | steamclient.so |
| `-private_ip_override` |  | registered (CCommandLineParam) | steamclient.so |
| `-profilestartup` |  | compared against argv (V_strnicmp, inferred); registered (CCommandLineParam) | chromehtml.so, steamclient.so, steamui.so |
| `-pyrowavestats` | Log pyrowave encoding performance to streaming_log.txt | registered (CCommandLineParam) | steamui.so |
| `-query` | Value is one of EChildProcessQueryCommand | internal parser | steamsysinfo |
| `-query-arg` | Argument for the query, the meaning depends on the query | internal parser | steamsysinfo |
| `-quicklogin` | Set the base used to construct quick login URLs | internal parser; registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamclient.so, steamui.so, steamwebhelper, streaming_client |
| `-rememberpassword` | If logging in user with credentials specified on the command line, proceed as if 'remember my password' had been enabled | registered (CCommandLineParam) | steamui.so |
| `-set_locale_disable` |  | internal parser | gamelauncher, steam |
| `-setbeta` | Sets Steam client beta branch | internal parser | gamelauncher, steam |
| `-showallbetas` | Disable client beta filtering | registered (CCommandLineParam) | steamui.so |
| `-shutdown` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-silent` | Silent startup mode (tray mode only) | internal parser; registered (CCommandLineParam) | friendsui.so, gamelauncher, steam, steamui.so |
| `-simulatedownloaderrors` |  | internal parser | gamelauncher, steam |
| `-simulatefatalerror` |  | internal parser | gamelauncher, steam |
| `-single_core` | Force Steam to run on your primary CPU only | internal parser; registered (CCommandLineParam) | steamclient.so, steamservice.so |
| `-singleapp` |  | internal parser; value | steam, steamui.so |
| `-sitelicense` |  | exists | steamclient.so |
| `-skipinitialbootstrap` |  | internal parser | gamelauncher, steam |
| `-skipstreamingdrivers` | Skip streaming driver checks | registered (CCommandLineParam) | steamclient.so |
| `-skipsystemcheck` |  | internal parser | gamelauncher, steam |
| `-sls-skip-version-check` | Don't validate the SLS version before starting | registered (CCommandLineParam) | steamui.so |
| `-srt-logger-opened` |  | internal parser | gamelauncher, steam |
| `-stack=` |  | value | libtier0_s.so |
| `-steamchina` |  | internal parser | steam |
| `-steamconsole` |  | exists | steamui.so |
| `-steamdeck` |  | exists | libtier0_s.so |
| `-steamdeckdisplay` |  | internal parser; registered (CCommandLineParam) | chromehtml.so, gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `-steamframe` |  | exists | libtier0_s.so |
| `-steamid` | Steam user identifier | internal parser | steamsysinfo |
| `-steaminstaller` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-steammachinedisplay` |  | internal parser; registered (CCommandLineParam) | chromehtml.so, gamelauncher, gameoverlayui.so, steam, steamclient.so, steamservice.so, steamui.so, steamwebhelper, streaming_client, vgui2_s.so |
| `-steamos` |  | internal parser | gamelauncher, steam |
| `-steamos3` |  | exists | libtier0_s.so |
| `-steampid` | Steam pid that launched us | registered (CCommandLineParam) | gameoverlayui.so |
| `-system-composer` | Force the use of the system browser composer | registered (CCommandLineParam) | steamui.so |
| `-tenfoot` | Start in Steam Big Picture mode | registered (CCommandLineParam) | steamui.so |
| `-tesla` |  | exists | libtier0_s.so |
| `-testled` | Create a test LED device | registered (CCommandLineParam) | steamui.so |
| `-testlongoobeupdater` |  | exists | steamclient.so |
| `-testoobe` |  | exists | chromehtml.so, steamclient.so, steamui.so |
| `-testoobestage2` |  | exists | steamui.so |
| `-testoobeupdater` | Use a dummy updater during oobe | registered (CCommandLineParam) | steamclient.so |
| `-testssa` | force display of SSA | registered (CCommandLineParam) | steamui.so |
| `-teststoragedata` | Enable test storage data | registered (CCommandLineParam) | steamui.so |
| `-testupdater` |  | exists | steamclient.so |
| `-textclient` |  | internal parser | gamelauncher, steam |
| `-toggle-overlay-html-mode` | Disables new faster overlay HTML path (or enables if on a branch it's not on by default for) / Disables new faster overlay HTML path (or enables if on a branch it's not on by default) / Disables new faster overlay HTML path (or enables in branches it's not yet on by default for) | registered (CCommandLineParam) | chromehtml.so, friendsui.so, gameoverlayui.so, steamclient.so, steamui.so |
| `-uninstall` |  | compared against argv (V_strnicmp, inferred) | steamui.so |
| `-use_xcomposite_workaround` |  | exists | steamwebhelper |
| `-usepipewireaudio` | Enabled the pipewire audio backend | registered (CCommandLineParam) | steamclient.so |
| `-userchooser` | Sends the user to the User Chooser even if they have 0 or 1 accounts | registered (CCommandLineParam) | steamui.so |
| `-verbose` |  | exists | steamclient.so |
| `-verbose-computer-activity` | Verbose computer activity detection. | registered (CCommandLineParam) | steamclient.so |
| `-verbosejslogging` | enable verbose logging of JS console events | registered (CCommandLineParam) | steamwebhelper |
| `-verifyfiles` |  | exists; internal parser | gamelauncher, steam, steamclient.so |
| `-vguifocus` | Print out details of which panel has keyboard focus | registered (CCommandLineParam) | vgui2_s.so |
| `-vguimessages` | set to see debug vgiui2 messages | registered (CCommandLineParam) | friendsui.so, gameoverlayui.so, steamui.so, vgui2_s.so |
| `-voicerelay` | Only allow 'relay' connections for voice (testing). | registered (CCommandLineParam) | steamclient.so |
| `-vrdisable` | Disable VR - never even try to load OpenVR DLLs | registered (CCommandLineParam) | steamclient.so |
| `-vrforce` | Always perform Hmd status check even if we crashed the last time we tried | registered (CCommandLineParam) | steamclient.so |
| `-vrlinkforceenable` | Force-enable VR Link capability for testing regardless of platform/encoder | registered (CCommandLineParam) | steamclient.so |
| `-vronly` |  | registered (CCommandLineParam) | steamui.so |
| `-vrskip` | Skip VR initialization entirely no matter who asks for it | registered (CCommandLineParam) | steamclient.so |
| `-vrverbose` | Output additional logging for diagnostics | registered (CCommandLineParam) | steamclient.so |
| `-websocket` | forces connection to Steam backend to be via WebSocket | registered (CCommandLineParam) | steamclient.so |
| `-websocketignorecertissues` | says it's ok to ignore cert validation issues if using WebSocket connections, for dev use only | registered (CCommandLineParam) | steamclient.so |
| `-windowed` | Set BPM to windowed | internal parser; registered (CCommandLineParam) | gamelauncher, steam, steamui.so |
