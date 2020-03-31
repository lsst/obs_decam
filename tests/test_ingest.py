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

"""Unit tests for gen3 DECam raw data ingest.
"""

import unittest
import os
import lsst.utils.tests

from lsst.obs.base.ingest_tests import IngestTestBase
import lsst.obs.decam

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    curatedCalibrationDatasetTypes = ("camera", "defects")

    def setUp(self):
        self.ingestDir = os.path.dirname(__file__)
        self.instrument = lsst.obs.decam.DarkEnergyCamera()
        # DecamRawIngestTask ingests every detector in each raw file, so we
        # only have to specify one file here, but should get two dataIds
        # in the output repo.
        self.file = os.path.join(testDataDirectory, "rawData", "raw", "raw.fits")
        self.dataIds = [dict(instrument="DECam", exposure=229388, detector=25),
                        dict(instrument="DECam", exposure=229388, detector=1)]
        self.RawIngestTask = lsst.obs.decam.DecamRawIngestTask

        super().setUp()


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestFullFileTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    """Test ingesting a file that contains all "normal" DECam HDUs.
    """
    # No need to test writeCuratedCalibrations again
    curatedCalibrationDatasetTypes = None

    def setUp(self):
        self.ingestDir = os.path.dirname(__file__)
        self.instrument = lsst.obs.decam.DarkEnergyCamera()
        # DecamRawIngestTask ingests every detector in each raw file, so we
        # only have to specify one file here, but should get many dataIds
        # in the output repo.
        self.file = os.path.join(testDataDirectory, "rawData", "raw",
                                 "c4d_150227_012718_ori-stripped.fits.fz")
        self.dataIds = [{"instrument": "DECam", "exposure": 415282, "detector": i} for i in range(1, 63)]
        self.RawIngestTask = lsst.obs.decam.DecamRawIngestTask

        super().setUp()


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestShuffledFullFileTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    """Test ingesting a file that contains all detectors in a random order.
    """
    # No need to test writeCuratedCalibrations again
    curatedCalibrationDatasetTypes = None

    def setUp(self):
        self.ingestDir = os.path.dirname(__file__)
        self.instrument = lsst.obs.decam.DarkEnergyCamera()
        # DecamRawIngestTask ingests every detector in each raw file, so we
        # only have to specify one file here, but should get many dataIds
        # in the output repo.
        self.file = os.path.join(testDataDirectory, "rawData", "raw",
                                 "c4d_150227_012718_ori-stripped-shuffled.fits.fz")
        self.dataIds = [{"instrument": "DECam", "exposure": 415282, "detector": i} for i in range(1, 63)]
        self.RawIngestTask = lsst.obs.decam.DecamRawIngestTask

        super().setUp()


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
