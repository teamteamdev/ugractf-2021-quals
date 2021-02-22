with import <nixpkgs> {};

python3.pkgs.buildPythonPackage {
  name = "haha";
  propagatedBuildInputs = [ python3.pkgs.flask ];
  nativeBuildInputs = [ (import /home/abbradar/projects/kyzylborda/shell.nix) ];
}

