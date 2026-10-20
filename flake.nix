{
  description = "Declarative Steam client configuration for NixOS";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      nixosModules.default = ./modules/client.nix;
      nixosModules.client = ./modules/client.nix;

      packages = forAllSystems (pkgs: {
        steam-config-apply = pkgs.callPackage ./pkgs/steam-config-apply { };
        default = self.packages.${pkgs.stdenv.hostPlatform.system}.steam-config-apply;
      });

      # Steam itself is x86_64-only, so the module is only evaluated there
      checks.x86_64-linux =
        let
          pkgs = nixpkgs.legacyPackages.x86_64-linux;
        in
        {
          # evaluate a configuration that sets one option of every kind
          module-eval =
            let
              sys = nixpkgs.lib.nixosSystem {
                system = pkgs.stdenv.hostPlatform.system;
                modules = [
                  self.nixosModules.default
                  {
                    nixpkgs.config.allowUnfree = true;
                    boot.loader.grub.enable = false;
                    fileSystems."/" = {
                      device = "nodev";
                      fsType = "ext4";
                    };
                    system.stateVersion = "25.11";
                    programs.steam.enable = true;
                    programs.steam.client = {
                      enable = true;
                      presets.noBackgroundServices = true;
                      runAtStartup = true;
                      settings.enable_overlay = false;
                      settings.overlay_fps_counter_bgopacity = 0.5;
                      settings.enable_shader_precache = false;
                      settings.start_in_big_picture_mode = "DesktopUI";
                      extraSettings.autoLoginUser = "alice";
                      friends.chatFlashMode = "Never";
                      switches.silent = true;
                      switches.language = "english";
                      convars."@nContentUpdateAutoVerifyEnable" = 0;
                      environment.STEAM_SPEW_LEVELS = "Overlay=4,4";
                      environment.STEAM_FORCE_CLIENT = "steamrt64";
                      steamCfg.BootStrapperInhibitAll = "enable";
                      gameEnvironment.MANGOHUD = true;
                      gameEnvironment.PRESSURE_VESSEL_SHELL = "instead";
                      defaultCompatTool = "proton_experimental";
                      games."570" = {
                        launchOptions = "-novid %command%";
                        environment.DXVK_HUD = "fps";
                        compatTool = "proton_9";
                        overlay = false;
                        autoUpdate = "onLaunch";
                        steamInput = "enable";
                      };
                      libraryFolders = [ "/mnt/games" ];
                      shortcuts.test = {
                        exe = "/bin/true";
                        compatTool = "proton_experimental";
                      };
                      clientBeta = "publicbeta";
                      cefRemoteDebugging = true;
                      vdf.registry.HKCU.Software.Valve.Steam.SkinV5 = "";
                    };
                  }
                ];
              };
            in
            # evaluate the wrapped package and the full generated configuration
            pkgs.writeText "module-eval" (
              builtins.unsafeDiscardStringContext (
                sys.config.programs.steam.package.drvPath
                + builtins.toJSON sys.config.programs.steam.client.finalConfig
              )
            );
        };

      formatter = forAllSystems (pkgs: pkgs.nixfmt);
    };
}
