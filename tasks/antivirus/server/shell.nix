with import <nixpkgs> {};

python3.pkgs.buildPythonPackage {
  name = "haha";
  propagatedBuildInputs = [ python3.pkgs.flask (python3.pkgs.callPackage /home/abbradar/projects/kyzylborda {}) ];
  nativeBuildInputs = [ bubblewrap python3.pkgs.gunicorn ];
}

