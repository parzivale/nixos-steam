# Library folders and non-Steam game shortcuts.
{
  config,
  lib,
  ...
}:

let
  inherit (lib) types mkOption mkIf;
  cfg = config.programs.steam.client;
in
{
  options.programs.steam.client = {
    libraryFolders = mkOption {
      type = types.listOf (
        types.coercedTo types.str (path: { inherit path; }) (
          types.submodule {
            options = {
              path = mkOption {
                type = types.str;
                description = "Absolute path of the library folder (Steam creates `steamapps/` inside it).";
              };
              label = mkOption {
                type = types.nullOr types.str;
                default = null;
                description = "Label shown in Settings > Storage.";
              };
            };
          }
        )
      );
      default = [ ];
      example = [
        "/mnt/games/SteamLibrary"
        {
          path = "/mnt/fast/SteamLibrary";
          label = "NVMe";
        }
      ];
      description = ''
        Extra Steam library folders that are always registered in `steamapps/libraryfolders.vdf` (Settings > Storage).
        Folders added in the UI are kept. Removing a folder from this list does not unregister it, because
        Steam tracks installed games per folder. Each folder must already exist and be writable by the user. Its
        `libraryfolder.vdf` marker and `steamapps/` directory are created if missing.
      '';
    };

    shortcuts = mkOption {
      type = types.attrsOf (
        types.submodule (
          { name, ... }:
          {
            options = {
              appName = mkOption {
                type = types.str;
                default = name;
                defaultText = lib.literalMD "the attribute name";
                description = "Name shown in the library.";
              };
              exe = mkOption {
                type = types.str;
                description = "Absolute path of the program (e.g. a Nix store path or `/run/current-system/sw/bin/...`).";
              };
              startDir = mkOption {
                type = types.nullOr types.str;
                default = null;
                description = "Working directory; defaults to the directory of {option}`exe`.";
              };
              launchOptions = mkOption {
                type = types.str;
                default = "";
                description = "Arguments, as in the shortcut's Launch Options (supports `%command%`).";
              };
              icon = mkOption {
                type = types.nullOr types.str;
                default = null;
                description = "Path of an icon image.";
              };
              hidden = mkOption {
                type = types.bool;
                default = false;
                description = "Hide the shortcut in the library.";
              };
              allowOverlay = mkOption {
                type = types.bool;
                default = true;
                description = "Enable the Steam Overlay for this shortcut.";
              };
              allowDesktopConfig = mkOption {
                type = types.bool;
                default = true;
                description = "Use the Steam Input desktop configuration in the launcher.";
              };
              openVR = mkOption {
                type = types.bool;
                default = false;
                description = "Mark the shortcut as a VR application (library \"VR\" filter, launch in SteamVR).";
              };
              tags = mkOption {
                type = types.listOf types.str;
                default = [ ];
                description = "Library tags (legacy categories).";
              };
              compatTool = mkOption {
                type = types.nullOr types.str;
                default = null;
                example = "proton_experimental";
                description = ''
                  Run this shortcut with a compatibility tool, e.g. Proton for a Windows `.exe` (Properties >
                  Compatibility). Same names as {option}`programs.steam.client.defaultCompatTool`.
                '';
              };
              compatToolConfig = mkOption {
                type = types.str;
                default = "";
                description = "Extra tool configuration string stored next to {option}`compatTool` (usually empty).";
              };
              artwork = lib.genAttrs [ "grid" "wide" "hero" "logo" "icon" ] (
                kind:
                mkOption {
                  type = types.nullOr types.path;
                  default = null;
                  description = ''
                    Custom ${kind} image (`grid` is the vertical library capsule, `wide` the horizontal one), copied to
                    `userdata/<id>/config/grid/<appid>...` under the shortcut's computed app ID.
                  '';
                }
              );
            };
          }
        )
      );
      default = { };
      example = lib.literalExpression ''
        {
          retroarch.exe = "''${pkgs.retroarch}/bin/retroarch";
          "Some Windows Game" = {
            exe = "/mnt/games/SomeGame/Game.exe";
            compatTool = "proton_experimental";
            artwork.grid = ./some-game-capsule.png;
          };
        }
      '';
      description = ''
        Non-Steam games ("Add a Non-Steam Game") written to `userdata/<id>/config/shortcuts.vdf`, keyed by a stable
        name. Steam derives a shortcut's app ID from its exe path and name (a CRC), and Proton settings and artwork
        follow that ID. When the path changes, for example a new Nix store path after an update, the module replaces
        the old entry together with its Proton mapping and artwork, so you don't get duplicates. Removing an entry
        from this set removes it from Steam on the next launch. Shortcuts you added in Steam yourself are never
        touched. Editing a managed shortcut in the UI is reverted on the next launch.
      '';
    };
  };

  config = mkIf cfg.enable {
    programs.steam.client.internal = {
      libraryFolders = map (f: { inherit (f) path label; }) cfg.libraryFolders;
      shortcuts = lib.mapAttrsToList (key: s: {
        inherit key;
        artwork = lib.mapAttrs (_: v: if v == null then null else "${v}") s.artwork;
        inherit (s)
          compatTool
          compatToolConfig
          appName
          exe
          startDir
          launchOptions
          icon
          hidden
          allowOverlay
          allowDesktopConfig
          openVR
          tags
          ;
      }) cfg.shortcuts;
    };
  };
}
