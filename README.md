# nixos-steam

Declarative configuration for the Steam client on NixOS. It covers every option the client has, public and
hidden, recovered by analysing the client itself (see [doc/](doc/README.md)).

## Usage

```nix
{
  inputs.nixos-steam.url = "github:parzivale/nixos-steam";

  outputs = { nixpkgs, nixos-steam, ... }: {
    nixosConfigurations.myhost = nixpkgs.lib.nixosSystem {
      modules = [
        nixos-steam.nixosModules.default
        {
          programs.steam.enable = true;
          programs.steam.client = {
            enable = true;

            # client settings (written into Steam's VDF config files at every launch)
            settings.enable_overlay = false;
            settings.enable_shader_background_processing = false;
            settings.run_at_startup = false;

            # command-line switches
            switches.silent = true;
            switches.disablelauncherservice = true;
            switches.language = "english";

            # console variables (passed as +name value)
            convars.nPeerContentDefaultMode = 0;

            # drop Steam's background helpers
            presets.noBackgroundServices = true;

            # compatibility tools, libraries, non-Steam games
            defaultCompatTool = "proton_experimental";
            libraryFolders = [ "/mnt/games/SteamLibrary" ];
            shortcuts = [ { appName = "RetroArch"; exe = "${pkgs.retroarch}/bin/retroarch"; } ];

            # environment variables and SDL hints
            environment.STEAM_SPEW_LEVELS = "Overlay=4,4";

            # steam.cfg in the install root
            steamCfg.BootStrapperInhibitAll = "enable";

            # environment for every game (overrides what Steam sets)
            gameEnvironment = {
              MESA_SHADER_CACHE_MAX_SIZE = "20G";
              MANGOHUD = true;
            };

            # per game, by app ID
            games."570" = {
              launchOptions = "-novid %command%";
              environment.DXVK_HUD = "fps";
              compatTool = "proton_9";
              overlay = false;
              autoUpdate = "onLaunch";
              steamInput = "enable";
            };
          };
        }
      ];
    };
  };
}
```

## Option sets

| Option | Count | Applied as |
|---|---|---|
| `settings.<name>` | 226 | Merged into Steam's own config store for that setting (`config.vdf`, `localconfig.vdf`, `sharedconfig.vdf`, `registry.vdf`) by `steam-config-apply` before every launch. |
| `switches.<name>` | 252 | Command-line switches. Session-only, internal and test-hook switches are flagged in their descriptions. |
| `convars.<name>` | 449 | `+name value` on the command line. |
| `environment.<NAME>` | 249 | Steam process environment: client variables, SDL hints and typed launcher/runtime variables. |
| `gameEnvironment.<NAME>` | 157 declared, plus any name | Environment of every game, applied after Steam builds it, so it overrides Steam's values. |
| `games.<appid>.*` | 24 per game | `launchOptions`, `environment`, `compatTool`, `artwork.*`, and 19 properties from the game's Properties dialog (overlay, auto-update, cloud, Steam Input, resolution, language, beta, DLC, ...). |
| `defaultCompatTool` | 1 | Global compatibility tool (`CompatToolMapping/0`). |
| `libraryFolders` | list | Registered in `steamapps/libraryfolders.vdf`. |
| `shortcuts` | list | Non-Steam games in `shortcuts.vdf`. |
| `clientBeta`, `client64`, `cefRemoteDebugging`, `forceUpdate`, `devConfig`, `extraFiles` | | Files in the Steam root (`package/beta`, marker files, `steam_dev.cfg`, ...). |
| `steamCfg.<Key>` | 8 | `<steam root>/steam.cfg` (bootstrapper / updater control). |
| `vdf.{install,local,roaming,registry}` | any | Raw keys for anything without a dedicated option. |
| `presets.noBackgroundServices` | 1 | Turns off helper processes and listeners (launcher service, crash monitor, hardware updater, LAN discovery, background recording, ...). |

All options live under `programs.steam.client`. Every option defaults to `null`, which means "not managed": Steam's own default, or whatever the user picked in
the UI, is left alone. Each option's description says what it does (inferred from how the client uses it, with a
confidence tag where inferred), where Steam stores it, and Steam's default.

Not exposed yet, or not possible to set:
* 44 settings that have no on-disk key (computed in code) or are read-only. Their storage is still being researched;
* per-game data stored on Valve's servers (collections, hidden games, beta passwords), and the encoded per-game
  performance profiles;
* console commands, because they are actions, not configuration;
* gamescope X11 atoms, because Steam sets these at runtime.

Use `extraArgs` for anything else.

## How game variables are applied

Steam builds each game's environment and then runs `$STEAM_GAME_LAUNCH_SHELL -c "<command line>"`, with
`/bin/sh` as the default. This sequence was recovered from `steamclient.so`; see
[doc/binaries/environment.md](doc/binaries/environment.md). When `gameEnvironment` or `games.*.environment` is
set, the module points `STEAM_GAME_LAUNCH_SHELL` at a generated script. The script exports your variables,
adds the per-game ones by matching `$SteamAppId`, and then `exec`s the real shell. Steam, Proton,
pressure-vessel and non-Steam shortcuts are unaffected apart from the extra variables. If you also set
`environment.STEAM_GAME_LAUNCH_SHELL`, the generated script hands over to your shell instead of `/bin/sh`.

## Notes

* The module sets `programs.steam.package` from `programs.steam.client.package` (default `pkgs.steam`).
  Customise Steam there instead of in `programs.steam.package`.
* The first modification of each VDF file keeps a `*.nixos-steam.bak` copy next to it.
* Per-user settings apply to every account under `userdata/` (or only `programs.steam.client.userIds`), and only
  after that account has logged in once. They take effect from the next launch after that.
* Settings in the roaming store are synced by Steam Cloud, so another machine can sync a different value back.
* `programs.steam.client.finalConfig` (read-only) shows the generated arguments, environment and settings data.
* The option data is generated by [tools/gen-options.py](tools/gen-options.py) from the extraction pipeline in
  [doc/_tools](doc/_tools/README.md). Regenerate it after Steam updates.
