# programs.steam.client: declarative configuration for every option of the Steam client.
#
# Option sets are generated from ../data/*.json (see ../tools/gen-options.py and ../doc/). Every option
# defaults to null, which means "not managed": Steam's own default or the user's choice is left alone.
{
  config,
  lib,
  pkgs,
  ...
}:

let
  inherit (lib)
    types
    mkOption
    mkIf
    mapAttrs
    mapAttrs'
    nameValuePair
    filterAttrs
    concatStringsSep
    optionalString
    ;

  cfg = config.programs.steam.client;

  readData = name: builtins.fromJSON (builtins.readFile (../data + "/${name}.json"));
  settingsData = readData "settings";
  switchesData = readData "switches";
  convarsData = readData "convars";
  envData = readData "environment";

  confidence = c: optionalString (c != "" && c != "high") " *(${c} confidence)*";
  fmt = v: if builtins.isBool v then (if v then "true" else "false") else builtins.toJSON v;

  # ------------------------------------------------------------------ client settings
  storeText = {
    install = "`<steam root>/config/config.vdf` (InstallConfigStore)";
    local = "`userdata/<id>/config/localconfig.vdf` (UserLocalConfigStore)";
    roaming = "`userdata/<id>/7/remote/sharedconfig.vdf` (UserRoamingConfigStore, cloud-synced)";
    registry = "`~/.steam/registry.vdf` (Registry)";
  };

  settingType =
    d:
    if d.type == "bool" then
      types.bool
    else if d.type == "int" then
      (
        if d.clampMin != null && d.clampMax != null then
          types.ints.between d.clampMin d.clampMax
        else
          types.int
      )
    else if d.type == "float" then
      types.either types.float types.int
    else if d.type == "enum" then
      types.either (types.enum (builtins.attrNames d.enum)) types.int
    else
      types.str; # string, hotkey

  settingDescription =
    name: d:
    concatStringsSep "\n\n" (
      lib.filter (s: s != "") [
        (d.what + confidence d.confidence)
        (optionalString (d.ui != "") "UI: ${d.ui}")
        (optionalString (d.valveDescription != "") "Valve: ${d.valveDescription}")
        (optionalString (d.type == "enum")
          "Values: ${concatStringsSep ", " (lib.mapAttrsToList (n: v: "`${n}` (${toString v})") d.enum)}."
        )
        (optionalString (
          d.type == "hotkey"
        ) "Hotkey string as Steam stores it, e.g. `Shift\\tKEY_TAB` (modifiers then key, tab-separated).")
        "Stored in ${storeText.${d.store}} at `${d.key}`."
        (optionalString (d.default != null) "Steam default: `${fmt d.default}`.")
        (optionalString d.perProfile "Steam can also store this per game / per display; this sets the base value.")
        (optionalString (
          d.store == "roaming"
        ) "Steam Cloud may sync a different value back from another machine.")
      ]
    );

  settingValue =
    d: v:
    if builtins.isBool v then
      (if v then "1" else "0")
    else if d.type == "enum" && builtins.isString v then
      toString d.enum.${v}
    else
      toString v;

  # ------------------------------------------------------------------ switches
  switchAttr = name: lib.removeSuffix "=" (lib.removePrefix "-" name);

  switchDescription =
    name: d:
    concatStringsSep "\n\n" (
      lib.filter (s: s != "") [
        ((if d.what != "" then d.what else d.help) + confidence d.confidence)
        (optionalString (d.help != "") "Valve: ${d.help}")
        (
          if d.arg then
            "Passed as `${name}${optionalString (!lib.hasSuffix "=" name) " "}<value>`."
          else
            "Passed as `${name}` when `true`."
        )
      ]
    );

  switchArgs = lib.flatten (
    lib.mapAttrsToList (
      name: d:
      let
        v = cfg.switches.${switchAttr name};
      in
      if v == null || v == false then
        [ ]
      else if !d.arg then
        [ name ]
      else if lib.hasSuffix "=" name then
        [ "${name}${toString v}" ]
      else
        [
          name
          (toString v)
        ]
    ) switchesData
  );

  # ------------------------------------------------------------------ convars
  convarType = {
    bool = types.bool;
    int = types.int;
    float = types.either types.float types.int;
    string = types.str;
    any = types.oneOf [
      types.bool
      types.int
      types.float
      types.str
    ];
  };

  convarDescription =
    name: d:
    concatStringsSep "\n\n" (
      lib.filter (s: s != "") [
        ((if d.what != "" then d.what else d.help) + confidence d.confidence)
        (optionalString (d.help != "") "Valve: ${d.help}")
        (optionalString (d.default != null) "Compile-time default: `${d.default}`.")
        (optionalString (lib.hasPrefix "@" name) "`@` convars can also be overridden by Steam's server-side client config.")
        "Passed on the command line as `+${name} <value>`."
      ]
    );

  convarValue = v: if builtins.isBool v then (if v then "1" else "0") else toString v;

  convarArgs = lib.flatten (
    lib.mapAttrsToList (
      name: v:
      lib.optionals (v != null) [
        "+${name}"
        (convarValue v)
      ]
    ) cfg.convars
  );

  # ------------------------------------------------------------------ environment
  envDescription =
    name: d:
    concatStringsSep "\n\n" (
      lib.filter (s: s != "") [
        (d.what + confidence d.confidence)
        (optionalString (
          d.kind == "sdl-hint"
        ) "SDL hint; an environment variable of the same name overrides it.")
        "Read by: ${concatStringsSep ", " d.binaries} (${concatStringsSep "; " d.access})."
        "`true`/`false` are passed as `1`/`0`."
      ]
    );

  envValue = v: if builtins.isBool v then (if v then "1" else "0") else toString v;

  # ------------------------------------------------------------------ apply
  managedSettings = filterAttrs (_: v: v != null) cfg.settings;
  steamCfg = filterAttrs (_: v: v != null) cfg.steamCfg;

  applyData = {
    inherit (cfg) steamRoot userIds;
    settings = lib.mapAttrsToList (name: v: {
      inherit (settingsData.${name}) store key;
      value = settingValue settingsData.${name} v;
    }) managedSettings;
    steamCfg =
      if steamCfg == { } && !cfg.manageSteamCfg then null else lib.mapAttrs (_: toString) steamCfg;
  };
  applyConfig = pkgs.writeText "nixos-steam-client.json" (builtins.toJSON applyData);

  allArgs = switchArgs ++ convarArgs ++ cfg.extraArgs;
  env = mapAttrs (_: envValue) (filterAttrs (_: v: v != null) cfg.environment);
in
{
  options.programs.steam.client = {
    enable = lib.mkEnableOption ''
      declarative Steam client configuration. Wraps {option}`programs.steam.package` so that the options
      below are applied every time Steam starts
    '';

    package = mkOption {
      type = types.package;
      default = pkgs.steam;
      defaultText = lib.literalExpression "pkgs.steam";
      description = ''
        Base Steam package. The configured package (with switches, convars, environment and the settings
        hook applied) is assigned to {option}`programs.steam.package`. Customise Steam here rather than in
        {option}`programs.steam.package` when this module is enabled.
      '';
    };

    applyPackage = mkOption {
      type = types.package;
      default = pkgs.callPackage ../pkgs/steam-config-apply { };
      defaultText = lib.literalExpression "pkgs.callPackage ./pkgs/steam-config-apply { }";
      description = "Tool that merges {option}`programs.steam.client.settings` into Steam's VDF files.";
    };

    steamRoot = mkOption {
      type = types.nullOr types.str;
      default = null;
      example = "/home/alice/.local/share/Steam";
      description = "Steam install root. `null` means `~/.steam/steam` if present, else `~/.local/share/Steam`.";
    };

    userIds = mkOption {
      type = types.nullOr (types.listOf types.str);
      default = null;
      example = [ "12345678" ];
      description = ''
        Steam account IDs (directory names under `userdata/`) that per-user settings are written to.
        `null` means every account that has logged in on this machine.
      '';
    };

    settings = mapAttrs (
      name: d:
      mkOption {
        type = types.nullOr (settingType d);
        default = null;
        description = settingDescription name d;
      }
    ) settingsData;

    switches = mapAttrs' (
      name: d:
      nameValuePair (switchAttr name) (mkOption {
        type =
          if d.arg then
            types.nullOr (
              types.oneOf [
                types.str
                types.int
              ]
            )
          else
            types.nullOr types.bool;
        default = null;
        description = switchDescription name d;
      })
    ) switchesData;

    convars = mapAttrs (
      name: d:
      mkOption {
        type = types.nullOr convarType.${d.type};
        default = null;
        description = convarDescription name d;
      }
    ) convarsData;

    environment = mapAttrs (
      name: d:
      mkOption {
        type = types.nullOr (
          types.oneOf [
            types.bool
            types.int
            types.str
          ]
        );
        default = null;
        description = envDescription name d;
      }
    ) envData;

    manageSteamCfg = mkOption {
      type = types.bool;
      default = false;
      description = ''
        Remove a `steam.cfg` previously written by this module when no {option}`programs.steam.client.steamCfg`
        key is set. A `steam.cfg` written by anything else is never touched.
      '';
    };

    steamCfg =
      let
        flag =
          desc:
          mkOption {
            type = types.nullOr (
              types.enum [
                "enable"
                "disable"
              ]
            );
            default = null;
            description = desc;
          };
        str =
          desc:
          mkOption {
            type = types.nullOr types.str;
            default = null;
            description = desc;
          };
      in
      {
        BootStrapperInhibitAll = flag "Disable all bootstrapper update activity (no client update check or download). Pin the client.";
        BootStrapperInhibitUpdateOnLaunch = flag "Skip only the update check at launch. *(inferred)*";
        BootStrapperInhibitClientChecksum = flag "Skip checksum verification of client files so local modifications survive. *(inferred)*";
        BootStrapperInhibitBootstrapperChecksum = flag "Skip checksum verification of the bootstrapper itself. *(inferred)*";
        ClientDownloadHost = str "Hostname that replaces the client-update CDN host.";
        Universe = str "Steam universe (`Public` default; `Beta` switches the data link to `~/.steam/steambeta`). Non-public universes are Valve-internal.";
        CMForce = str "Force a specific Connection Manager server (`host:port`). *(inferred)*";
        DisableDownloads = str "`1` disables content downloads. *(inferred)*";
      };

    finalConfig = mkOption {
      type = types.attrs;
      readOnly = true;
      description = "The generated launch arguments, environment and settings file data (for inspection).";
    };

    extraArgs = mkOption {
      type = types.listOf types.str;
      default = [ ];
      example = [
        "-silent"
        "+open"
        "steam://open/library"
      ];
      description = "Extra raw arguments passed to Steam after the generated switches and convars.";
    };
  };

  config = mkIf cfg.enable {
    programs.steam.client.finalConfig = {
      args = allArgs;
      environment = env;
      apply = applyData;
    };
    programs.steam.package = cfg.package.override (prev: {
      extraArgs = concatStringsSep " " (
        lib.filter (s: s != "") [
          (prev.extraArgs or "")
          (lib.escapeShellArgs allArgs)
        ]
      );
      extraEnv = (prev.extraEnv or { }) // env;
      extraProfile = ''
        ${prev.extraProfile or ""}
        ${lib.getExe cfg.applyPackage} ${applyConfig} || echo "nixos-steam: applying Steam settings failed" >&2
      '';
    });
  };
}
