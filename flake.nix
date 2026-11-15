{
  description = "ID protocols Python dev env (Nix + venv + pip requirements)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.git
            pkgs.uv
            pkgs.stdenv.cc.cc.lib
          ];

          shellHook = ''
            # Make libstdc++ visible to wheels like pyzmq (manylinux)
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

            export VENV_DIR=.venv
            if [ ! -d "$VENV_DIR" ]; then
              ${pkgs.uv}/bin/uv venv "$VENV_DIR"
            fi
            source "$VENV_DIR/bin/activate"

            if [ -f requirements.txt ]; then
              ${pkgs.uv}/bin/uv pip install -r requirements.txt
            fi
          '';
        };
      });
}
