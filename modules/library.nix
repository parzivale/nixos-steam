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
      type = types.listOf (
        types.submodule {
          options = {
            appName = mkOption {
              type = types.str;
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
          };
        }
      );
      default = [ ];
      example = lib.literalExpression ''
        [ { appName = "RetroArch"; exe = "''${pkgs.retroarch}/bin/retroarch"; } ]
      '';
      description = ''
        Non-Steam games ("Add a Non-Steam Game") written to `userdata/<id>/config/shortcuts.vdf`. A shortcut is
        identified by its generated app ID, a CRC of the exe path and name, exactly as Steam computes it. So editing
        one in the UI is overwritten on the next launch, while shortcuts you added yourself are kept. Removing an
        entry from this list does not delete it from Steam.
      '';
    };
  };

  config = mkIf cfg.enable {
    programs.steam.client.internal = {
      libraryFolders = map (f: { inherit (f) path label; }) cfg.libraryFolders;
      shortcuts = map (s: {
        inherit (s)
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
