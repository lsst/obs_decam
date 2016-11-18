#
# LSST Data Management System
# Copyright 2008-2015 AURA/LSST.
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
import lsst.utils.tests

import lsst.daf.persistence as dafPersist
from lsst.obs.mosaic import MosaicMapper


class GetIdTestCase(lsst.utils.tests.TestCase):
    """Testing butler exposure id retrieval"""

    def setUp(self):
        self.bf = dafPersist.ButlerFactory(mapper=MosaicMapper(root="."))
        self.butler = self.bf.create()

    def tearDown(self):
        del self.butler
        del self.bf

    def testId(self):
        """Test retrieval of exposure ids"""
        bits = self.butler.get("ccdExposureId_bits")
        self.assertEqual(bits, 32)
        id = self.butler.get("ccdExposureId", visit=229388, ccdnum=13, filter="z")
        self.assertEqual(id, 22938813)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
