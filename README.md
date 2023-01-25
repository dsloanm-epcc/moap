# MOAP

## Spack Setup

On ARCHER2, a pre-prepared Spack install is available for use at
`/work/d435/d435/shared/spack` alongside a working copy of this repository.

If the pre-prepared install cannot be used, to install from scratch:

```
# Check out the latest Spack
git clone https://github.com/spack/spack.git
# Replace recipes with those from this repository's `spack_recipes`
cd spack/var/spack/repos/builtin/packages
for pkg in blitz lfric py-psyclone rose-picker xios yaxt; do
  # Delete any old recipes
  rm -r ${pkg}
  # Symlink new recipes
  ln -s /work/d435/d435/shared/spack_recipes/${pkg} ${pkg}
done
```

Passwordless SVN access to:

```
https://code.metoffice.gov.uk/svn/lfric/GPL-utilities/trunk
https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk
```

must be set up to enable installation of the `rose-picker` dependency and
`LFRic` itself. Failure to do so will result in permissions issues during the
install.

## GCC 10+11 Build

Create a Spack environment with the `env.yaml` configuration file:

```
source /work/d435/d435/shared/spack/share/spack/setup-env.sh
spack env create moap-gcc10 /work/d435/d435/shared/spack_config/env.yaml
```

The config file sets various ARCHER2-specific options, such as the use of
`cray-mpich` rather than a custom MPI.

Activate the new environment and install the `lfric` spec:

```
spack env activate moap-gcc10
# User's choice of %gcc@10.2.0 or %gcc@11.2.0
spack add lfric %gcc@10.2.0
# View and confirm the spec then install
spack spec
spack install
```

Note, `spack compiler find` may be needed to set up `gcc`.

## CCE 13 Build

Follow GCC instructions above but specify `%cce@13.0.2` compiler instead:

```
spack add lfric %cce@13.0.2
```

See below for build issue workarounds.

### Workaround for OpenSSL Build Stall

Cray compilers <= `cce@13.0.2` indefinitely stall when building OpenSSL due to
bugs with Cray-specific optimisations.

Work around by running `spack install` until Spack hangs on OpenSSL. Then
interrupt build (ctrl+c) and install only OpenSSL with `-fno-cray` flag:

```
CFLAGS="-fno-cray" CPPFLAGS="-fno-cray" spack install --dirty openssl %cce@13.0.2
```

Argument `--dirty` necessary for Spack to pick up on `FLAGS` environment
variables.

Resume `spack install` afterwards.

### Workaround for LFRic Failing to Find _dgemm_, etc.

When build fails with missing references to `_dgemm_` and other BLAS/LAPACK
routines, restart with:

```
spack install --dirty
```

It is believed Spack is failing to pick up on `cray-libsci` without the
`--dirty` flag.

## Intel 2021.1.1 Build

Unload all central MPI, compiler and BLAS modules and setup the Intel modules:

```
source scripts/setup-intel.sh
```

or manually:

```
module use /work/z19/shared/adrianj/intel/oneapi/modulefiles 
module load compiler
module load mpi
module load mkl
module unload cray-mpich PrgEnv-cray cce cray-libsci
```

Create a new environment using `intel-env.yaml`:

```
source /work/d435/d435/shared/spack/share/spack/setup-env.sh
spack env create moap-intel /work/d435/d435/shared/spack_config/intel-env.yaml
```

Activate the new environment and install the `lfric` spec:

```
spack env activate moap-intel
spack add lfric %intel@2021.1.1
# View and confirm the spec then install
spack spec
spack install
```

## Manual LFRic Build

To rebuild a working copy of LFRic, e.g. to test local changes, Spack can be
used to set up all dependent packages then a manual build of LFRic performed.

First, complete an LFRic install in a Spack environment as detailed above.
Switch compiler to match the version used for the environment install, set
relevant build environment variables and perform a manual `make`.

### GCC Setup

```
spack env activate moap-gcc11
module swap PrgEnv-cray PrgEnv-gnu
# Using the moap-gcc11 environment so use gcc/11 compiler
module swap gcc gcc/11.2.0

# Set compiler names
export FC=ftn
export LDMPI=ftn
```

### CCE Setup

```
spack env activate moap-cce13
# Using the moap-gcc13 environment so use cce/13 compiler
module swap cce cce/13.0.2

# Set compiler names
export FC=ftn
export LDMPI=ftn
```

### Intel Setup

```
spack env activate moap-intel
source scripts/setup-intel.sh

# Set compiler names 
export FC=ifort
export LDMPI=mpiifort
```

### Perform the Build

Set up remaining compiler-agnostic variables and build:

```
export FPP="cpp -traditional-cpp"
# HACK: Get the prefix directory for the Spack environment, e.g.
#   /mnt/lustre/a2fs-work3/work/d435/d435/shared/spack/var/spack/environments/moap-gcc11/.spack-env/view
# Get the path to `psyclone`, use `rev` to reverse the string, `cut` to remove
# `/bin/psyclone` from the "beginning" and `rev` again to restore the original
# order.
INSTALL_DIR=$(which psyclone | rev | cut -d/ -f3- | rev)
export FFLAGS="-I$INSTALL_DIR/include"
export LDFLAGS="-L$INSTALL_DIR/lib"
export CPPFLAGS="-I$INSTALL_DIR/include"

# Set target to enable OpenMP use
export LFRIC_TARGET_PLATFORM=meto-xc40

# Build
cd trunk/gungho
make -j64 build
```

New binary will be produced in `bin/gungho`. CAUTION: the old `gungho` binary
provided by the chosen environment will still be on `$PATH`. Carefully specify
your paths to ensure only the intended binary is run.

### Running the New Build

```
# Ensure libraries provided by environment are linked correctly
export LD_LIBRARY_PATH=$INSTALL_DIR/lib:$LD_LIBRARY_PATH
cd example
../bin/gungho configuration.nml
```

