with import <nixpkgs> {};

python3.pkgs.buildPythonPackage {
  name = "haha";
  propagatedBuildInputs = with python3.pkgs; [ dataclasses-json aiohttp aiohttp-jinja2 aiohttp-session numpy cryptography ];
}
