This project is a fork of [HyperPardinus](https://github.com/haslab/HyperPardinus) with a slightly different pipeline and multiple trace visualization.

For more details on the original [HyperPardinus](https://github.com/haslab/HyperPardinus) or [Alloy](https://github.com/AlloyTools/org.alloytools.alloy) check the [original README](./original-README.md).

# Requirements

Tailored for Linux.

Beyond the [original Alloy](https://github.com/AlloyTools/org.alloytools.alloy) dependencies. It requires either [NuSMV](https://nusmv.fbk.eu/) or [nuXmv](https://nuxmv.fbk.eu/). [NuSMV](https://nusmv.fbk.eu/)/[nuXmv](https://nuxmv.fbk.eu/), [Electrod](https://github.com/hpacheco/electrod) and [HyperSMV](https://github.com/haslab/HyperSMV/tree/main) should be cloned to outside this repository.

## nuXmv

```bash
# Download nuXmv 2.2.0 for Linux 64-bit
wget https://nuxmv.fbk.eu/dist/nuXmv-2.2.0-linux64.tar.xz -O nuXmv.tar.xz

# Extract
tar -xf nuXmv.tar.xz

# Enter the binary directory
cd nuXmv-2.2.0-linux64/bin

# Make executable
chmod +x nuXmv

# Add nuXmv to PATH
echo "export PATH=\"\$PATH:$(pwd)\"" >> ~/.bashrc
source ~/.bashrc

# Verify installation
nuXmv -h
```

## Electrod

```bash
# Install OPAM, the OCaml package manager
sudo apt install -y opam

# Initialize OPAM
opam init
eval $(opam env)

# Clone Electrod
git clone https://github.com/hpacheco/electrod.git
cd electrod

# Install Electrod dependencies and build the release version
make setup
make release

# Add Electrod to PATH
echo "export PATH=\"$(pwd):\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

## HyperSMV

```bash
# Install GHCup, the Haskell toolchain installer
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh

# Install GHC (Glasgow Haskell Compiler) and Cabal
ghcup install ghc
ghcup install cabal

# Clone HyperSMV
git clone https://github.com/haslab/HyperSMV.git
cd HyperSMV

# Build and install HyperSMV
cabal install

# Add Cabal's local binary directory to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

# Usage

```bash
# Clone HyperPardinus
git clone https://github.com/MiguelLPMM/HyperPardinus.git
cd HyperPardinus

# Compile
./gradlew build

# Or compile without testing
./gradlew build -xtest

# Execute it
java -jar org.alloytools.alloy.dist/target/org.alloytools.alloy.dist.jar
```

After the GUI opens, head to `Options > Solver` and select `hyper.autohyper`, for AutoHyper, or `hyper.hyperq`, for HyperQube.

Also in `Options`, `Max DD Block Size`, `Atomic Propositions`, `HyperQube unrolling Bound`, `HyperQube Semantics`, and `AutoHyper Solver` can all be changed with fixed options. Follow the recommended values in [HyperPardinus-benchmarks](https://github.com/haslab/HyperPardinus-benchmarks/blob/snark/benchmarks/benchsHyperAlloy.json).