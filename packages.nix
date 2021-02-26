{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
    gnused
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
