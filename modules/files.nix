# File-based switches in the Steam install root, client beta, steam_dev.cfg, and raw VDF escape hatches.
{
  config,
  lib,
  ...
}:

let
  inherit (lib) types mkOption mkIf;
  cfg = config.programs.steam.client;

  # nested attrset -> [ { key = "a\\b\\c"; value = "v"; } ]
  flatten =
    prefix: attrs:
    lib.concatLists (
      lib.mapAttrsToList (
        k: v:
        let
          key = if prefix == "" then k else "${prefix}\\${k}";
        in
        if builtins.isAttrs v then
          flatten key v
        else
          [
            {
              inherit key;
              value = if builtins.isBool v then (if v then "1" else "0") else toString v;
            }
          ]
      ) attrs
    );

  vdfType =
    let
      leaf = types.oneOf [
        types.bool
        types.int
        types.float
        types.str
      ];
    in
    types.attrsOf (types.either leaf (types.attrsOf types.anything));

  vdfOption =
    file:
    mkOption {
      type = vdfType;
      default = { };
      description = ''
        Raw keys merged into ${file}, as a nested attrset below the file's root block. Use it for keys that
        have no dedicated option. `true`/`false` become `1`/`0`.
      '';
    };
in
{
  options.programs.steam.client = {
    clientBeta = mkOption {
      type = types.nullOr types.str;
      default = null;
      example = "publicbeta";
      description = ''
        Steam client beta to opt into, written to `<steam root>/package/beta` (Settings > Interface >
        Client Beta Participation). Use `""` to manage the file and stay on the stable client. `null` leaves it alone.
        The bootstrapper logs "Opted in to client beta '%s' via beta file".
      '';
    };

    client64 = mkOption {
      type = types.nullOr types.bool;
      default = null;
      description = ''
        Select the 64-bit SteamRT3 client (`steamrt64/steam`, `true`) or the legacy 32-bit client (`ubuntu12_32/steam`, `false`).
        This manages the `.steam-enable-steamrt64-client` marker file that `steam.sh` checks. It is the persistent
        form of `STEAM_FORCE_CLIENT`.
      '';
    };

    cefRemoteDebugging = mkOption {
      type = types.bool;
      default = false;
      description = ''
        Create `.cef-enable-remote-debugging` in the Steam root. It enables steamwebhelper's Chrome DevTools
        port (`localhost:8080`, or `-devtools-port`) for inspecting and debugging the Steam UI.
      '';
    };

    forceUpdate = mkOption {
      type = types.bool;
      default = false;
      description = ''
        Keep a `.forceupdate` marker in the Steam root, so the bootstrapper re-applies the client package on
        every start. This is the file-based equivalent of `-forcesteamupdate` *(inferred)*. Only useful for repairing an install.
      '';
    };

    devConfig = mkOption {
      type = types.nullOr (
        types.attrsOf (
          types.oneOf [
            types.bool
            types.int
            types.float
            types.str
          ]
        )
      );
      default = null;
      example = {
        "@AllowSkipGameUpdate" = 1;
      };
      description = ''
        Write `<steam root>/steam_dev.cfg` with one `name value` line per entry. This is the classic way to
        override `@` client-config convars persistently. **It also puts the install into development mode**:
        `~/.steam/steam` is not created, `--reset` refuses to run and the bootstrap is not reinstalled. Prefer
        {option}`programs.steam.client.convars` unless you need that.
      '';
    };

    extraFiles = mkOption {
      type = types.attrsOf types.str;
      default = { };
      example = {
        "config/mangohud.conf" = "fps_limit=60\n";
      };
      description = ''
        Arbitrary files, relative to the Steam root, kept with exactly this content. Files created this way are
        removed when dropped from the option. Existing files not created by this module are never overwritten.
      '';
    };

    vdf = {
      install = vdfOption "`config/config.vdf` (`InstallConfigStore`)";
      local = vdfOption "`userdata/<id>/config/localconfig.vdf` (`UserLocalConfigStore`) for every managed account";
      roaming = vdfOption "`userdata/<id>/7/remote/sharedconfig.vdf` (`UserRoamingConfigStore`) for every managed account";
      registry = vdfOption "`~/.steam/registry.vdf` (`Registry`, e.g. `HKCU.Software.Valve.Steam.AutoLoginUser`)";
    };
  };

  config = mkIf cfg.enable {
    programs.steam.client.internal = {
      files =
        lib.optionalAttrs (cfg.clientBeta != null) { "package/beta" = cfg.clientBeta; }
        // lib.optionalAttrs (cfg.client64 == true) { ".steam-enable-steamrt64-client" = ""; }
        // lib.optionalAttrs cfg.cefRemoteDebugging { ".cef-enable-remote-debugging" = ""; }
        // lib.optionalAttrs cfg.forceUpdate { ".forceupdate" = ""; }
        // lib.optionalAttrs (cfg.devConfig != null) {
          "steam_dev.cfg" = lib.concatStrings (
            lib.mapAttrsToList (
              n: v: "${n} ${if builtins.isBool v then (if v then "1" else "0") else toString v}\n"
            ) cfg.devConfig
          );
        }
        // cfg.extraFiles;
      environment = lib.optionalAttrs (cfg.client64 == false) { STEAM_FORCE_CLIENT = "ubuntu12_32"; };
      settings = lib.concatLists (
        lib.mapAttrsToList (store: attrs: map (e: e // { inherit store; }) (flatten "" attrs)) cfg.vdf
      );
    };
  };
}
