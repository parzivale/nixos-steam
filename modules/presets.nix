# Opinionated bundles of options. Every value is set with mkDefault, so an explicit setting always wins.
{
  config,
  lib,
  options,
  ...
}:

let
  inherit (lib)
    mkOption
    mkIf
    mkDefault
    types
    ;
  cfg = config.programs.steam.client;
  hasSetting = n: options.programs.steam.client.settings ? ${n};
in
{
  options.programs.steam.client.presets = {
    noBackgroundServices = mkOption {
      type = types.bool;
      default = false;
      description = ''
        Keep Steam to the client and its web UI: no helper processes or listeners beyond what is needed to run
        the UI and games. This sets, as defaults you can override:
        - shader pre-caching and background Vulkan shader processing (`fossilize_replay`) off, when the
          setting is mapped;
        - switches `-disablelauncherservice` (no `steam-runtime-launcher-service`), `-no-hardware-updater`,
          `-nocrashmonitor`, `-preventsteamdiscovery` (no LAN discovery) and `-skipstreamingdrivers`;
        - LAN peer content transfers off (`nPeerContentDefaultMode = 0`);
        - background game recording, broadcasting and the hardware updater off;
        - the Steam Deck Wi-Fi access point for Remote Play off.
        Games, the overlay, downloads and Steam Input keep working.
      '';
    };
  };

  config = mkIf (cfg.enable && cfg.presets.noBackgroundServices) {
    programs.steam.client = {
      switches = {
        disablelauncherservice = mkDefault true;
        no-hardware-updater = mkDefault true;
        nocrashmonitor = mkDefault true;
        preventsteamdiscovery = mkDefault true;
        skipstreamingdrivers = mkDefault true;
      };
      convars.nPeerContentDefaultMode = mkDefault 0;
      settings = {
        gamerecording_background_mode = mkDefault "k_EGRMode_Never";
        broadcast_permissions = mkDefault "k_EBroadcastPermissionDisabled";
        hardware_updater_enabled = mkDefault false;
        remote_play_wifi_ap_enabled = mkDefault false;
      }
      // lib.optionalAttrs (hasSetting "enable_shader_background_processing") {
        enable_shader_background_processing = mkDefault false;
      };
    };
  };
}
