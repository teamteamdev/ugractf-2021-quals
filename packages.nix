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
    docker
    docker-compose
  ];

  pythonPackages = self: with self; [
    flask
    uvloop
    aiogram
    aiohttp
    aiohttp-jinja2
    aiohttp-session
    aiosqlite
    gunicorn
    cryptography
    numpy
    pyqrcode
    pyzbar
    pydub
  ];
}
