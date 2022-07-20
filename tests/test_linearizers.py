#
# LSST Data Management System
# Copyright 2022 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <https://www.lsstcorp.org/LegalNotices/>.
#
import unittest
import os

import lsst.utils
import lsst.utils.tests
import lsst.daf.butler


test_data_package = "testdata_decam"
try:
    test_data_directory = lsst.utils.getPackageDir(test_data_package)
except LookupError:
    test_data_directory = None


@unittest.skipIf(test_data_directory is None, "testdata_decam must be set up")
class DecamLinearizersTestCase(lsst.utils.tests.TestCase):
    """DECam linearizer tests."""
    @classmethod
    def setUpClass(cls):
        cls.repo = os.path.join(test_data_directory, 'repo')

    def test_linearizers_existence(self):
        """Test existence of linearizers."""
        butler = lsst.daf.butler.Butler(self.repo, instrument='DECam')

        datasets = set(butler.registry.queryDatasets('linearizer', collections=...))

        self.assertEqual(len(datasets), 62)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
