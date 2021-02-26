{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
    gnused
    inkscape
    cdrtools
    bubblewrap
    xorg.xorgserver
    python3.pkgs.gunicorn
  ];

  pythonPackages = self: with self; [
    flask
    uvloop
    aiohttp
    aiohttp-jinja2
    aiohttp-session
    gunicorn
    cryptography
    numpy
  ];
}
