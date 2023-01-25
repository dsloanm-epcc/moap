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
#     spack install yaxt
#
# You can edit this file again by typing:
#
#     spack edit yaxt
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Yaxt(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://swprojects.dkrz.de/redmine/projects/yaxt"
    url      = "https://swprojects.dkrz.de/redmine/attachments/download/523/yaxt-0.9.3.1.tar.gz"
    list_url = "https://swprojects.dkrz.de/redmine/projects/yaxt/wiki/Downloads"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ["github_user1", "github_user2"]

    version("0.9.3.1", sha256="5cc2ffeedf1604f825f22867753b637d41507941b7a0fbbfa6ea40637a77605a")
    version("0.9.3", sha256="c409271f3c19bd7f445adbaf9de2ad1c3ecbc6881a5b63f88daa371bb0782e12")
    version("0.9.2.1", sha256="cada1ecc479eaf088b8c95d9ae80122842843dd6af0a660ab6191fcb0da20a1e")
    version("0.9.2", sha256="b6714e42483486d76db146732bac74bc500096c15c9efa411ece3e00172fc360")
    version("0.9.1", sha256="c87ec59e29b3e4965ce2f8e614bd7f1597012b89af0fda4242f2eef06460794c")
    version("0.9.0", sha256="d3673e88c1cba3b77e0821393b94b5952d8ed7dc494305c8cf93e7ebec19483c")

    depends_on("mpi")


    def setup_build_environment(self, env):
        # MPI wrappers (not bare compilers) expected in $CC and $FC
        env.set("CC", self.spec["mpi"].mpicc)
        env.set("FC", self.spec["mpi"].mpifc)

    def configure_args(self):
        # Disable MPI tests with "--without-regard-for-quality"
        args = ["--with-idxtype=long", "--without-regard-for-quality"]
        return args

