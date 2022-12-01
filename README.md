# MOAP

## Installation Instructions

### GCC

Create a test environment with the given environment file:

```
source /work/d435/d435/shared/share/spack/setup-env.sh
spack env create moap-test /work/d435/d435/shared/spack_config/env.yaml
```

The config file sets various ARCHER2-specific options, such as the use of
`cray-mpich` rather than a custom MPI.

Activate the new environment and install the `lfric` spec:

```
spack env activate moap-test
spack add lfric %gcc@10.2.0
# View and confirm the spec then install
spack spec
spack install
```

Note, `spack compiler find` may be needed to set up `gcc`.

### CCE

Follow GCC instructions above but specify `%cce@13.0.2` compiler instead:

```
spack add lfric %cce@13.0.2
```

See below for build issue workarounds.

#### Workaround for OpenSSL Build Stall

Cray compilers <= `cce@13.0.2` indefinitely stall when building OpenSSL due to
bugs with Cray-specific optimisations.

Work around by running `spack install` until Spack hangs on OpenSSL. Then
interrupt build (ctrl+c) and install only OpenSSL with `-fno-cray` flag:

```
CFLAGS="-fno-cray" CPPFLAGS="-fno-cray" FFLAGS="-fno-cray" spack install --dirty openssl %cce@13.0.2
```

Argument `--dirty` necessary for Spack to pick up on `FLAGS` environment
variables.

Resume `spack install` afterwards.

#### Workaround for LFRic Failing to Find _dgemm_, etc.

When build fails with missing references to `_dgemm_` and other BLAS/LAPACK
routines, restart with:

```
spack install --dirty
```

It is believed Spack is failing to pick up on `cray-libsci` without the
`--dirty` flag.

