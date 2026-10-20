{ lib, python3 }:

python3.pkgs.buildPythonApplication {
  pname = "steam-config-apply";
  version = "0.1.0";
  format = "other";

  src = ./steam_config_apply.py;
  dontUnpack = true;

  installPhase = ''
    runHook preInstall
    install -Dm755 $src $out/bin/steam-config-apply
    runHook postInstall
  '';

  meta = {
    description = "Merge declarative settings into Steam's VDF config files";
    license = lib.licenses.mit;
    mainProgram = "steam-config-apply";
    platforms = lib.platforms.linux;
  };
}
