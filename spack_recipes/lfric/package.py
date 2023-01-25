# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install lfric
#
# You can edit this file again by typing:
#
#     spack edit lfric
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Lfric(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://code.metoffice.gov.uk/trac/lfric"
    svn = "https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ["github_user1", "github_user2"]

    # FIXME: Add proper versions and checksums here.
    version("r39162", revision=39162)

    # FIXME: Add dependencies if required.
    # FIXME: Restrict versions
    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran ^netcdf-c+mpi")

    depends_on("yaxt")
    depends_on("xios@2.5")
    depends_on("py-jinja2")
    depends_on("py-psyclone@2.3.1")
    depends_on("rose-picker")

    # Patch out "-warn errors" for Intel so build doesn't fail with:
    #   utilities/mpi_mod.F90(184): error #8889: Explicit declaration of the
    #   EXTERNAL attribute is required.   [MPI_ALLREDUCE]
    #      call mpi_allreduce( l_sum, g_sum, 1, get_mpi_datatype( real_type,
    #      r_double ), &
    patch("ifort.mk.patch", when="%intel")


    def setup_build_environment(self, env):
        env.set("LFRIC_TARGET_PLATFORM", "meto-xc40")
        env.set("FPP", "cpp -traditional-cpp")
        env.set("LDMPI", self.spec["mpi"].mpifc)


    build_directory = "gungho" # FIXME
    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("build")

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree("bin/", prefix.bin)
            
