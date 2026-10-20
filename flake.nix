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
                    fileSystems."/".device = "nodev";
                    system.stateVersion = "25.11";
                    programs.steam.enable = true;
                    programs.steam.client = {
                      enable = true;
                      settings.enable_overlay = false;
                      settings.overlay_fps_counter_bgopacity = 0.5;
                      switches.silent = true;
                      switches.language = "english";
                      convars."@nContentUpdateAutoVerifyEnable" = 0;
                      environment.STEAM_SPEW_LEVELS = "Overlay=4,4";
                      steamCfg.BootStrapperInhibitAll = "enable";
                    };
                  }
                ];
              };
            in
            pkgs.writeText "module-eval" (
              builtins.unsafeDiscardStringContext sys.config.programs.steam.package.drvPath
            );
        };

      formatter = forAllSystems (pkgs: pkgs.nixfmt);
    };
}
