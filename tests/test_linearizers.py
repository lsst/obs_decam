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

import lsst.daf.butler


class DecamLinearizersTestCase(lsst.utils.tests.TestCase):
    """DECam linearizer tests."""
    @classmethod
    def setUpClass(cls):
        try:
            cls.data_dir = lsst.utils.getPackageDir("testdata_decam")
        except LookupError:
            raise unittest.skipTest("testdata_decam not setup")

        cls.repo = os.path.join(cls.data_dir, 'repo')

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
