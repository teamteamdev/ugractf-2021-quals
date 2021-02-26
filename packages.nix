{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
    gnused
    inkscape
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
