let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/fd487183437963a59ba763c0cc4f27e3447dd6dd.tar.gz";
  pkgs = import nixpkgs {
    config = { };
    overlays = [ ];
  };
in
pkgs.mkShellNoCC {
  venvDir = ".venv";
  buildInputs = with pkgs; [ portaudio ];
  packages =
    with pkgs;
    [
      python311
      clang
    ]
    ++ (with pkgs.python311Packages; [
      pip
      venvShellHook
    ]);
}
