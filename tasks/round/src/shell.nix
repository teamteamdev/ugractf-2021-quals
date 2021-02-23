{ pkgs ? import <nixpkgs> {} }:

let
  qt5env = pkgs.qt5.env "qt-${pkgs.qt5.qtbase.version}" (with pkgs.qt5; [
    qtbase
    qtdeclarative
    qtquickcontrols2
    qttools
  ]);
  env = pkgs.buildFHSUserEnv {
    name = "round";
    targetPkgs = pkgs: with pkgs; [
      qtcreator
      qt5env
      stdenv.cc
      gnumake
      gdb
    ];
    extraOutputsToInstall = [ "dev" ];
    profile = ''
      export QML2_IMPORT_PATH=${qt5env}/${pkgs.qt5.qtbase.qtQmlPrefix}
    '';
    runScript = pkgs.writeScript "env-shell" ''
      #!${pkgs.stdenv.shell}
      exec ${userShell}
    '';
  };

  userShell = builtins.getEnv "SHELL";

in pkgs.stdenv.mkDerivation {
  name = "round-fhs-dev";

  shellHook = ''
    exec ${env}/bin/round
  '';
  buildCommand = "exit 1";
}

