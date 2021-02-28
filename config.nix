{ domain, config, pkgs, lib, ... }:

with lib;

let
  icecastPort = 44100;
  icecastPassword = "5kUnRXWndu8ADfXr";

in {
  networking.firewall = {
    allowedTCPPorts = [
      17792
      4443
    ];
  };

  services.icecast = {
    enable = true;
    hostname = "dj.ugractf.ru";
    listen = {
      port = icecastPort;
    };
    admin = {
      user = "root";
      password = "MAAcAAZPrJ5RJ93e";
    };
    extraConf = ''
      <authentication>
        <source-password>${icecastPassword}</source-password>
      </authentication>
    '';
  };

  services.nginx.virtualHosts."dj.ugractf.ru" = {
    forceSSL = true;
    enableACME = true;
    locations."/".proxyPass = "http://127.0.0.1:${toString icecastPort}";
  };

  systemd.services.best-edm-songs = {
    wantedBy = [ "multi-user.target" ];
    after = [ "icecast.service" ];
    serviceConfig = {
      Restart = "on-failure"; 
      ExecStart = "${pkgs.ffmpeg}/bin/ffmpeg -stream_loop -1 -re -i ${./tasks/thevillage/private/long.flac} -c:a libmp3lame -ab 32k -ac 1 -content_type audio/mpeg -f mp3 icecast://source:${icecastPassword}@localhost:${toString icecastPort}/thevillage.mp3";
    };
  };
}
