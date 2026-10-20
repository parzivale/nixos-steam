# Settings outside CMsgClientSettings' generic stores: the "custom function" settings (mapped to their real keys),
# extra registry/config-store keys, and the Friends & Chat / voice settings (JSON blobs inside VDF values).
{
  config,
  lib,
  ...
}:

let
  inherit (lib) types mkOption mkIf;
  cfg = config.programs.steam.client;

  data = builtins.fromJSON (builtins.readFile ../data/extra-settings.json);
  inGroup = g: lib.filterAttrs (_: d: d.group == g) data;

  confidence = c: lib.optionalString (c != "" && c != "high") " *(${c} confidence)*";

  storeText = {
    install = "`config/config.vdf`";
    local = "`userdata/<id>/config/localconfig.vdf`";
    roaming = "`userdata/<id>/7/remote/sharedconfig.vdf` (cloud-synced)";
    registry = "`~/.steam/registry.vdf`";
    "json:local" = "a JSON object in `userdata/<id>/config/localconfig.vdf`";
    "json:roaming" = "a JSON object in `userdata/<id>/7/remote/sharedconfig.vdf` (cloud-synced)";
  };

  optType =
    d:
    if d.values != null then
      types.enum (builtins.attrNames d.values)
    else if d.type == "bool" then
      types.bool
    else if d.type == "int" then
      types.int
    else if d.type == "float" then
      types.either types.float types.int
    else
      types.str;

  describe =
    d:
    lib.concatStringsSep "\n\n" (
      lib.filter (s: s != "") [
        (d.what + confidence d.confidence)
        (lib.optionalString (d.values != null)
          "Values: ${
            lib.concatStringsSep ", " (lib.mapAttrsToList (n: v: "`${n}` (stored as `${v}`)") d.values)
          }."
        )
        "Stored in ${storeText.${d.store}} at `${
          if d.container != null then "${d.container}` → `${d.key}" else d.key
        }`${lib.optionalString (d.transform == "invert") " (inverted)"}."
        (lib.optionalString (d.default != null) "Steam default: `${builtins.toJSON d.default}`.")
      ]
    );

  mkOpt =
    d:
    mkOption {
      type = types.nullOr (optType d);
      default = null;
      description = describe d;
    };

  # value as written into a VDF string
  vdfValue =
    d: v:
    if d.values != null then
      d.values.${v}
    else if builtins.isBool v then
      (if (d.transform == "invert") != v then "1" else "0")
    else
      toString v;

  # value as written into a JSON blob
  jsonValue =
    d: v:
    builtins.toJSON (
      if d.values != null then
        lib.toInt d.values.${v}
      else if d.transform == "invert" && builtins.isBool v then
        !v
      else
        v
    );

  entries =
    group: values:
    lib.concatLists (
      lib.mapAttrsToList (
        name: v:
        let
          d = data.${name};
        in
        lib.optional (v != null) (
          if d.container != null then
            {
              inherit (d) store container key;
              json = jsonValue d v;
            }
          else
            {
              inherit (d) store key;
              value = vdfValue d v;
            }
        )
      ) (lib.filterAttrs (n: _: data ? ${n} && data.${n}.group == group) values)
    );
in
{
  options.programs.steam.client = {
    # custom-function settings join the regular settings set under their proto field names
    settings = lib.mapAttrs (_: mkOpt) (inGroup "settings");

    extraSettings = lib.mapAttrs (_: mkOpt) (inGroup "extraSettings");

    friends = lib.mapAttrs (_: mkOpt) (inGroup "friends");

    runAtStartup = mkOption {
      type = types.bool;
      default = false;
      description = ''
        Start Steam when a graphical session starts. This installs a system-wide XDG autostart entry, which is
        what the "Run Steam when my computer starts" setting does per user.
      '';
    };
  };

  config = mkIf cfg.enable {
    programs.steam.client.internal.settings =
      entries "settings" cfg.settings
      ++ entries "extraSettings" cfg.extraSettings
      ++ entries "friends" cfg.friends;

    environment.etc."xdg/autostart/steam.desktop" = mkIf cfg.runAtStartup {
      source = "${config.programs.steam.package}/share/applications/steam.desktop";
    };
  };
}
