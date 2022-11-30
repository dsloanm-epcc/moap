# MOAP

## Installation Instructions

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

