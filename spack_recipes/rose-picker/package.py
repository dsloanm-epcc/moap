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
#     spack install rose-picker
#
# You can edit this file again by typing:
#
#     spack edit rose-picker
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class RosePicker(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://code.metoffice.gov.uk/svn/lfric/GPL-utilities"
    svn = homepage+"/trunk"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ["github_user1", "github_user2"]

    # FIXME: Add proper versions and checksums here.
    version("r31715", revision=31715)

    # FIXME: Add dependencies if required.
    extends("python@3:")

    def install(self, spec, prefix):
        install_tree("meta_data_utils/", prefix.meta_data_utils)
        install_tree("rose_picker/", prefix.rose_picker)
        install_tree("bin/", prefix.bin)

        # Install lib/python libraries to path expected by extends("python")
        # e.g. lib/python3.10/site-packages
        pythonpath = join_path(prefix.lib, "python%s" % spec["python"].version.up_to(2), "site-packages")
        install_tree("lib/python", pythonpath)

