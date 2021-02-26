{ config, pkgs, lib, ... }:

with lib;

{
  networking.firewall = {
    allowedTCPPorts = [
    ];
  };
}
