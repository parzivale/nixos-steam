# Shipped JSON/VDF/CFG config files: fossilize_engine_filters.json and friends

Steam Linux client, manifest `1791918634`.

## Method and sources

* I read every non-binary config file in the extracted packages: `*.json`, `*.vdf`, `*.cfg`, `*.ini`. The files under `controller_base/` were summarised with a small key-path collector, `launcher_tools/vdfkeys.py`.
* Which binary consumes each key comes from the `strings` dumps.
* The JSON schema strings for fossilize come from `libVkLayer_steam_fossilize.so`. Their meanings follow from the error and info strings quoted below and from upstream Fossilize (`fossilize_application_filter.cpp`). Anything not backed by either is marked **(inferred)**.

The files covered:

| File | Package | Consumer |
|---|---|---|
| `fossilize_engine_filters.json` | `bins_*` | `libVkLayer_steam_fossilize.so` (via `FOSSILIZE_APPLICATION_INFO_FILTER_PATH`, set by steamclient) |
| `bin/hardwareupdater/hardwareupdater.cfg` | `bins_hardware` | `hardwareupdater` |
| `controller_base/*.vdf` (28) + `controller_base/templates/*.vdf` (54) | `resources`/`public` | Steam Input (`steamclient.so`) |
| `resource/registrykeys.vdf` | `resources_all` | Install-script / registry emulation (`legacycompat`) |
| `steam/games/PlatformMenu.vdf` | `resources_all` | Legacy VGUI platform menu |
| `ubuntu12_64/vk_swiftshader_icd.json` | `webkit_ubuntu12` | Vulkan loader (CEF software fallback) |
| `public/steamvr_action_manifest.json` | `public_all` | SteamVR input |
| `public/steambootstrapper_<lang>.txt` | `public_all` | Bootstrapper UI strings |
| `manifest.vdf` (downloaded client manifest) | CDN | Bootstrapper |

---

## 1. `fossilize_engine_filters.json`

### What it is for

Steam's Vulkan shader pre-caching works like this:

1. The implicit Vulkan layer `VK_LAYER_VALVE_steam_fossilize` records pipeline state into `.foz` databases while a game runs.
2. Steam uploads those databases and later replays them with `fossilize_replay`.

This JSON is an **application-info filter**. Based on the `VkApplicationInfo` of the game (`pEngineName`, engine version, API version), it decides whether recording happens at all, and how the recorded data is split into **buckets**, i.e. separate caches keyed by GPU and driver features.

How it is wired up, from the ordered steamclient strings in `shadercacheimplfossilize.cpp`:

* steamclient exports `STEAM_FOSSILIZE_DUMP_PATH`, `STEAM_FOSSILIZE_DUMP_PATH_READ_ONLY`, `FOSSILIZE_APPLICATION_INFO_FILTER_PATH` (the path to this file) and `ENABLE_VK_LAYER_VALVE_steam_fossilize_1`.
* The read-only dump path default is `$bucketdir/steam_pipeline_cache.foz;$bucketdir/steamapp_pipeline_cache.foz`.

### Content shipped in this build

```json
{ "asset": "FossilizeApplicationInfoFilter", "version": 1,
  "engineFilters": {
    "DXVK":  { "minimumEngineVersion": 4222979,
               "bucketVariantDependencies": ["EngineName","EngineVersionMajor"],
               "engineVersionBucketDeltas": [8417280],
               "recordImmutableSamplers": false,
               "bucketVariantFeatureDependencies": ["DescriptorBuffer","DescriptorHeap"] },
    "vkd3d": { "minimumEngineVersion": 8392704,
               "blacklistedEnvironments": {
                   "VKD3D_CONFIG": {"contains":"qa_checks"},
                   "VKD3D_SHADER_OVERRIDE": {"nonnull":true},
                   "VKD3D_DISABLE_EXTENSIONS": {"nonnull":true} },
               "bucketVariantDependencies": ["BindlessUBO","VendorID","MutableDescriptorType",
                   "BufferDeviceAddress","EngineName","EngineVersionMajor","EngineVersionMinor"],
               "bucketVariantFeatureDependencies": ["DescriptorBuffer","DescriptorHeap"] } } }
```

Versions are encoded with `VK_MAKE_VERSION` (`major<<22 | minor<<12 | patch`):

| Value | Decoded | Meaning |
|---|---|---|
| `4222979` | 1.7.3 | Minimum DXVK version that gets recorded. |
| `8417280` | 2.7.0 | DXVK bucket delta. **(inferred)** Splits the DXVK buckets at 2.7.0. |
| `8392704` | 2.1.0 | Minimum vkd3d-proton version that gets recorded. |

### Schema: every key the layer recognises

**Top level:**

| Key | Type | Meaning |
|---|---|---|
| `asset` | string | Must be `"FossilizeApplicationInfoFilter"`. |
| `version` | int | Schema version. A mismatch gives "Fossilize ERROR: JSON version mismatches." and recording is then **not** filtered: "Failed to parse ApplicationInfoFilter, letting recording go through." This build ships `1`. |
| `blacklistedApplicationNames` | string[] | `pApplicationName` values that are never recorded: "pApplicationName %s is blacklisted for recording. Skipping." |
| `blacklistedEngineNames` | string[] | `pEngineName` values that are never recorded. |
| `applicationFilters` | object, keyed by `pApplicationName` | Per-application rules. Same keys as the per-filter table below, using `minimumApplicationVersion` and `applicationVersionBucketDeltas`. |
| `engineFilters` | object, keyed by `pEngineName` | Per-engine rules. This build has `DXVK` and `vkd3d`. |
| `defaultBucketVariantDependencies` | string[] | Bucket dependencies for apps or engines with no matching filter. |
| `defaultBucketVariantFeatureDependencies` | string[] | Same, for feature dependencies. |

**Per-filter** (the value under `applicationFilters.<name>` or `engineFilters.<name>`):

| Key | Type | Meaning |
|---|---|---|
| `minimumApiVersion` | uint (`VK_MAKE_VERSION`) | Skip recording if the app's `apiVersion` is lower: "apiVersion %u is too low for pEngineName %s. Skipping." |
| `minimumApplicationVersion` | uint | Skip recording if `applicationVersion` is lower. Application filters only. |
| `minimumEngineVersion` | uint | Skip recording if `engineVersion` is lower. Engine filters only. |
| `blacklistedEnvironments` | object `{ ENV_VAR: rule }` | Skip recording when the rule matches: "Skipping recording due to environment rule for: %s". Must be an object, and each element must be an object. |
| ↳ rule `contains` | string | Matches when the env var's value contains this substring. |
| ↳ rule `equals` | string | Matches on exact equality. |
| ↳ rule `nonnull` | bool | Matches when the variable is set at all. |
| `bucketVariantDependencies` | string[] (must be an array) | Inputs hashed into the bucket name, so differing values get separate caches. Allowed tokens: `VendorID`, `EngineName`, `EngineVersion`, `EngineVersionMajor`, `EngineVersionMinor`, `EngineVersionPatch`, `ApplicationName`, `ApplicationVersion`, `ApplicationVersionMajor`, `ApplicationVersionMinor`, `ApplicationVersionPatch`, `BindlessUBO`, `MutableDescriptorType`, `BufferDeviceAddress`. The last three are device features or extension usage. |
| `bucketVariantFeatureDependencies` | string[] | Feature-based bucket split. Tokens seen: `DescriptorBuffer`, `DescriptorHeap`, i.e. `VK_EXT_descriptor_buffer` / descriptor-heap usage. |
| `engineVersionBucketDeltas` / `applicationVersionBucketDeltas` | uint[] (must be an array: "*VersionBucketDeltas must be an array") | **(inferred)** Version thresholds that start a new bucket, used with the `*VersionMajor/Minor` dependencies. |
| `recordImmutableSamplers` | bool | Whether immutable samplers in descriptor-set layouts are recorded. DXVK sets `false`. |

### Environment variables used by the fossilize layer and replayer

Taken from `libVkLayer_steam_fossilize.so` and `fossilize_replay` strings, plus steamclient.

| Variable | Set by | Meaning |
|---|---|---|
| `ENABLE_VK_LAYER_VALVE_steam_fossilize_1` | steamclient | Enables the implicit layer for a game. |
| `STEAM_FOSSILIZE_DUMP_PATH` | steamclient | Where recordings for this app are written. |
| `STEAM_FOSSILIZE_DUMP_PATH_READ_ONLY` | steamclient | `;`-separated existing databases. Pipelines already in them are not re-recorded. |
| `FOSSILIZE_APPLICATION_INFO_FILTER_PATH` | steamclient | Path to this JSON. |
| `STEAM_FOSSILIZE_IDENTIFIER_DUMP_PATH`, `STEAM_FOSSILIZE_PIPELINE_USE_DUMP_PATH`, `STEAM_FOSSILIZE_LAST_USE_TAG` | — | Usage tracking: which pipelines are actually used, so caches can be pruned. **(inferred)** |
| `STEAM_FOSSILIZE_PRECOMPILE_QA` | — | QA mode for precompiled caches. **(inferred)** |
| `STEAM_FOSSILIZE_REPLAY_WRAP` | steamclient | Wrapper command for `fossilize_replay` (`%s%s/../ubuntu12_%s/fossilize_replay`). |
| `FOSSILIZE_REPLAY_WRAPPER`, `FOSSILIZE_REPLAY_WRAPPER_ORIGINAL_APP` | fossilize_replay | Internal re-exec of a wrapper. |
| `FOSSILIZE_DUMP_SYNC` | layer | Write synchronously (debug). |
| `FOSSILIZE_DISABLE_RATE_LIMITER` | fossilize_replay | Don't throttle background replay. |
| `RADV_DEBUG` | steamclient | `nomemorycache` is appended during replay. |
| `MESA_GLSL_CACHE_DIR`, `MESA_GLSL_CACHE_MAX_SIZE`, `__GL_SHADER_DISK_CACHE_PATH` | steamclient | OpenGL shader cache redirection (`steamapp_shader_cache`, `mesa_shader_cache`). |

Database file names (from steamclient): `steam_pipeline_cache.foz`, `steamapp_pipeline_cache.foz`, `steam_pipeline_cache_whitelist`, `replay_cache.*.foz`, `steamapprun_pipeline_cache.*`, `fozpipelinesv<N>`, `VulkanPipelinesV<N>_<x>`, `TOUCH`.

Client-side settings that control shader pre-caching are covered in on-disk-config-files.md §1a (`ShaderCacheManager\…`) and the convar list. Examples: `bShaderAllowReplay`, `bShaderAllowReplayOnNVIDIA`, `unShaderBackgroundProcessingThreads`, and `-noshaders` ("Disable the shader manager").

---

## 2. `ubuntu12_64/vk_swiftshader_icd.json`

```json
{"file_format_version": "1.0.0", "ICD": {"library_path": "./libvk_swiftshader.so", "api_version": "1.0.5"}}
```

This is a standard Vulkan loader ICD manifest pointing at the bundled SwiftShader software Vulkan driver. CEF uses it for its software and GPU-less fallback (cf. `-cef-disable-gpu`).

| Key | Meaning |
|---|---|
| `file_format_version` | ICD manifest format version. |
| `ICD.library_path` | Driver library. A relative path is resolved from the manifest's directory. |
| `ICD.api_version` | Vulkan version the driver advertises. |

---

## 3. `bin/hardwareupdater/hardwareupdater.cfg`

```
MUST_UPDATE_TRITON_FW_TS:6A18D057
MUST_UPDATE_PROTEUS_FW_TS:6A18D053
TRITON_FW_TS:6AC686B3
PROTEUS_FW_TS:6AC6869B
```

The format is `KEY:hex-unix-timestamp`. The hex values are firmware build timestamps, in 2026.

| Key | Meaning |
|---|---|
| `<DEVICE>_FW_TS` | Timestamp of the firmware bundled for that controller family. A device whose firmware is older is offered an update. **(inferred)** |
| `MUST_UPDATE_<DEVICE>_FW_TS` | Minimum required firmware. Anything older gets a forced update. **(inferred)** |

The codenames are Valve hardware: **Triton** is the new Steam Controller and **Proteus** is likely its puck/dongle. Both are **(inferred)**; `chord_triton.vdf` exists in `controller_base`.

---

## 4. `controller_base/*.vdf` and `controller_base/templates/*.vdf` (Steam Input configurations)

There are 82 files in total. Each is a Steam Input configuration in the same schema the client writes for user configs (`%llu_controller_config.vdf`, `controller_config/game_actions_<appid>.vdf`). I collected key paths and occurrence counts across all of them:

| Key path | Count | Meaning / sample values |
|---|---|---|
| `controller_mappings/version` | 49 | Config format version: `2`, `3`. |
| `controller_mappings/revision` | 14 | Edit revision. |
| `controller_mappings/title`, `/description` | 46 | Localization tokens (`#…`) or literal text. |
| `controller_mappings/creator` | 23 | SteamID64 of the author, or `-1`. |
| `controller_mappings/controller_type` | 41 | Target controller type. All values seen: `controller_neptune` (Steam Deck), `controller_triton`, `controller_steamcontroller_gordon`, `controller_ps3`, `controller_ps4`, `controller_ps5`, `controller_xbox360`, `controller_xboxone`, `controller_switch_pro`, `controller_switch_joycon_left`, `controller_switch_joycon_right`, `controller_legion_go_s`, `controller_android`, `controller_apple`, `controller_mobile_touch`, `controller_generic`. |
| `controller_mappings/game` | 22 | Template name, e.g. "Gamepad with Mouse". |
| `controller_mappings/localization/<language>/{title,description}` | ~40 per language | Localized names for 28 languages. |
| `actions/<set>/…`, `gameactions/<set>` | 37 | Action-set definitions, e.g. the `WebBrowser` set with `Cursor`, `Scroll`, `zoom`. `Button/A` = `#Action_Confirm`, and so on. |
| `group/id`, `group/mode` | 993 | Input source groups. Modes seen, with counts: `dpad` 190, `trigger` 186, `joystick_move` 150, `four_buttons` 95, `absolute_mouse` 90, `switches` 87, `flickstick` 68, `joystick_mouse` 60, `single_button` 34, `scrollwheel` 10, `disabled` 8, `gyro_to_mouse` 7, `mouse_joystick` 4, `joystick_camera` 4. |
| `group/name`, `group/description` | 68 | |
| `group/inputs/<input>/activators/<Full_Press\|Long_Press\|…>/bindings/binding` | 1988 | Binding strings. Verbs seen, with counts: `xinput_button` 844, `key_press` 417, `game_action <set> <action>` 359, `controller_action <CMD>` 190 (e.g. `SHOW_KEYBOARD`), `mouse_button` 116, `mouse_wheel` 58, `mode_shift` 4. |
| `…/bindings/click` | 40 | Click binding for trackpads and sticks. |
| `…/settings/*` | — | Per-group and per-activator tuning. Keys: `haptic_intensity` (829), `repeat_rate` (201), `output_trigger`, `requires_click`, `left_trackpad_mode`, `right_trackpad_mode`, `sensitivity`, `output_joystick`, `layer`, `virtual_mode`, `deadzone`, `layout`, `hold_repeats`, `edge_binding_radius`, `doubetap_max_duration` (sic), `interruptable` (sic), … |
| `preset/id`, `preset/name`, `preset/group_source_bindings/<groupid>` | 89 / 952 | Presets (action sets or layers) mapping group IDs to physical sources: `button_diamond active`, `right_joystick inactive`, `right_trackpad …`, `left_trigger`, `gyro`, `dpad`, … |
| `settings/left_trackpad_mode`, `settings/right_trackpad_mode` | 68 | Top-level settings. |

Example files and roles:

* `desktop_*.vdf`: desktop configurations per controller.
* `chord_*.vdf`: Guide-button chord configurations.
* `basicui*.vdf`: Big Picture.
* `launcher*.vdf`: game launchers.
* `videoplayer.vdf`, `screenreader.vdf`, `steamdesktop.vdf`, `streaming_steamdesktop.vdf`: special modes.
* `empty.vdf`: no bindings.
* `templates/controller_<type>_{gamepad_fps,gamepad_joystick,wasd,…}.vdf`: the templates offered in the configurator.

`controller_base/d0ggle.bin` is binary data, not a config file.

---

## 5. `resource/registrykeys.vdf`

```
"InstallScript" { "Registry" { "HKEY_LOCAL_MACHINE\\Software\\<Publisher>" { } … } }
"kvsignatures" { "InstallScript" "<1024-bit hex signature>" }
```

This is a signed **install script**, in the same schema as per-game `installscript.vdf`. It lists 65 `HKLM\Software\<publisher>` registry keys (Activision … Vigil). **(inferred)** These keys are created or virtualised in the emulated registry so legacy installers and games find their parent keys. `kvsignatures` holds the Valve signature over the `InstallScript` block; strings such as `CAPIJobCheckFileSignature` show that signatures are checked.

| Key | Meaning |
|---|---|
| `InstallScript/Registry/<hive\path>/{ <value> <data> }` | Registry keys and values to create. These are empty here, so only the keys themselves are created. |
| `kvsignatures/InstallScript` | Hex RSA signature over the `InstallScript` subtree. |

---

## 6. `steam/games/PlatformMenu.vdf`

```
"Platform" { "Menu" {
  "Games"   { "dll" "steamui"        "interface" "SteamUIGames001"     "MenuName" "#Steam_Games" "SteamApp" "1" }
  "Friends" { "dll" "bin/friendsui"  "interface" "VGuiModuleTracker001" "MenuName" "#App_Friends" } } }
```

This defines the legacy VGUI platform menu modules.

| Key | Meaning |
|---|---|
| `dll` | Module to load (`steamui.so`, `bin/friendsui.so`). |
| `interface` | Factory interface name. |
| `MenuName` | Localization token for the menu label. |
| `SteamApp` | Marks the module as part of the Steam app. |

---

## 7. `public/steamvr_action_manifest.json`

```json
{"actions":[{"name":"/actions/haptics/out/haptic","type":"vibration"}],
 "action_sets":[{"name":"/actions/haptics","usage":"single"}]}
```

This is a SteamVR Input action manifest. Steam registers a single vibration output action so it can drive VR controller haptics.

| Key | Meaning |
|---|---|
| `actions[].name` | Action path. |
| `actions[].type` | Action type, here `vibration`. |
| `action_sets[].name` | Action-set path. |
| `action_sets[].usage` | Set usage, here `single`. |

There is no `default_bindings` section.

---

## 8. `public/steambootstrapper_<language>.txt`

These are KeyValues localization files: `"Language" "<lang>"`, then `"Tokens" { … }`. There are 44 tokens:

* `SteamBootstrapper_*`, covering:
  * updating, checking, downloading, extracting, installing and verifying
  * disk-space, mkdir and not-writeable failures
  * read-only install
  * manifest load/verify/OS-type/save failures
  * corrupt package and unzip failure
  * no network
  * already running
  * `MoveContentDir_*`
  * `OperatingSystemNoLongerSupported(OnBeta)`
* `SteamCmd_OperatingSystemNoLongerSupported`, which is the only place `-overrideminos` is documented.

The bootstrapper loads the file via `public/steambootstrapper_%language%.txt`, picked by `-language` or the system locale.

---

## 9. `manifest.vdf` (client package manifest, downloaded by the bootstrapper)

Structure: `"<platform>" { "version" "<n>" "<package>" { … } … }`. The platform is `ubuntu12` here.

| Key | Meaning |
|---|---|
| `version` | Client build (`1791918634`). |
| `<package>/file` | `<package>.zip.<sha1>` on `client-update.steamstatic.com`. |
| `<package>/size` | Zip size in bytes. |
| `<package>/sha2` | SHA-256 of the zip. |
| `<package>/zipvz`, `<package>/sha2vz` | Valve "VZ" (LZMA) compressed alternative and its SHA-256. |

This build has 28 packages:

* `bins_*` and `bins_*_steamrt_*`
* `webkit_*`
* `steamui_websrc_*`, `steamui_websrc_sounds_*`, `steamui_websrc_movies_*`
* `resources_*`, `public_all`, `strings_*`, `tenfoot_images_all`
* `sdl3_*`, `miles_*`, `steam_*`
* `runtime_scout_ubuntu12`, `runtime_steamrt_ubuntu12`

The bootstrapper's own fields on top of this:

* It downloads `steam_client_<platform>[ _<beta> ]` (from `package/beta`).
* It honours `-forcemanifestsuffix`.
* OS gating uses `oslist`, `osarch` and `OSVER`. A mismatch gives "System OS is not compatible with manifest OS type".
