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
    ffmpeg
    git
    gnugrep
    zip
    socat
  ];

  pythonPackages = self: with self; [
    flask
    uvloop
    aiohttp
    aiohttp-jinja2
    aiohttp-session
    aiosqlite
    gunicorn
    cryptography
    numpy
    pyqrcode
    pydub
  ];
}
