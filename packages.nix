{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
    gnused
    inkscape
    xorg.xorgserver
    cdrtools
  ];

  pythonPackages = self: with self; [
    flask
    uvloop
    aiohttp
    aiohttp-jinja2
    aiohttp-session
    gunicorn
    numpy
  ];
}
