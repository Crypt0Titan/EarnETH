{pkgs}: {
  deps = [
    pkgs.lsof
    pkgs.iana-etc
    pkgs.run
    pkgs.mailutils
    pkgs.imagemagick_light
    pkgs.openssl
    pkgs.postgresql
  ];
}
