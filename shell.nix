let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/fd487183437963a59ba763c0cc4f27e3447dd6dd.tar.gz";
  pkgs = import nixpkgs {
    config = { };
    overlays = [ ];
  };

  python-with-pkg = pkgs.python312.withPackages (
    ps: with ps; [
      pip
    ]
  );
in
pkgs.mkShellNoCC {
  venvDir = ".venv";
  buildInputs = with pkgs; [ portaudio ];
  packages =
    [
      python-with-pkg
      python-with-pkg.pkgs.venvShellHook
    ]
    ++ (with pkgs; [
      clang
    ]);
}
