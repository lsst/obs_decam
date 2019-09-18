# This file is part of obs_decam.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit tests for DECam raw data ingest.
"""

import unittest
import os
import lsst.utils.tests

from lsst.obs.base.ingest_tests import IngestTestBase
import lsst.obs.decam

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except lsst.pex.exceptions.NotFoundError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    def setUp(self):
        self.ingestDir = os.path.dirname(__file__)
        self.instrument = lsst.obs.decam.DarkEnergyCamera()
        self.file = os.path.join(testDataDirectory, "rawData", "raw", "raw.fits")
        self.dataId = dict(instrument="DECam", exposure=229388, detector=25)

        super().setUp()


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
