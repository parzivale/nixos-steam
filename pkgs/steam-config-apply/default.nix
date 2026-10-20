{ lib, python3 }:

python3.pkgs.buildPythonApplication {
  pname = "steam-config-apply";
  version = "0.1.0";
  format = "other";

  src = ./.;

  installPhase = ''
    runHook preInstall
    install -Dm755 steam_config_apply.py $out/bin/steam-config-apply
    runHook postInstall
  '';

  doCheck = true;
  checkPhase = ''
    runHook preCheck
    HOME=$TMPDIR python3 -m unittest -v test_steam_config_apply
    runHook postCheck
  '';

  meta = {
    description = "Merge declarative settings into Steam's VDF config files";
    license = lib.licenses.mit;
    mainProgram = "steam-config-apply";
    platforms = lib.platforms.linux;
  };
}
