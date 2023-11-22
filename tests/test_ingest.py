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

from lsst.daf.butler import Butler, DataCoordinate
from lsst.obs.base.ingest_tests import IngestTestBase
import lsst.obs.decam
import lsst.afw.cameraGeom.testUtils

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


class DecamTestBase(IngestTestBase):

    ingestDir = os.path.dirname(__file__)
    instrumentClassName = "lsst.obs.decam.DarkEnergyCamera"


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestTestCase(DecamTestBase, lsst.utils.tests.TestCase):

    curatedCalibrationDatasetTypes = ("camera", "defects")

    # Decam ingests every detector in each raw file, so we
    # only have to specify one file here, but should get two dataIds
    # in the output repo.
    @property
    def file(self):
        return os.path.join(testDataDirectory, "rawData", "raw", "raw.fits")

    dataIds = [dict(instrument="DECam", exposure=229388, detector=25),
               dict(instrument="DECam", exposure=229388, detector=1)]
    filterLabel = lsst.afw.image.FilterLabel(physical="z DECam SDSS c0004 9260.0 1520.0", band="z")

    @property
    def visits(self):
        butler = Butler(self.root, collections=[self.outputRun])
        return {
            DataCoordinate.standardize(
                instrument="DECam",
                visit=229388,
                universe=butler.dimensions
            ): [
                DataCoordinate.standardize(
                    instrument="DECam",
                    exposure=229388,
                    universe=butler.dimensions
                )
            ]
        }


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestFullFileTestCase(DecamTestBase, lsst.utils.tests.TestCase):
    """Test ingesting a file that contains all "normal" DECam HDUs.
    """

    # No need to test writeCuratedCalibrations again
    curatedCalibrationDatasetTypes = None

    # Decam ingests every detector in each raw file, so we
    # only have to specify one file here, but should get many dataIds
    # in the output repo.
    @property
    def file(self):
        return os.path.join(testDataDirectory, "rawData", "raw", "c4d_150227_012718_ori-stripped.fits.fz")

    dataIds = [{"instrument": "DECam", "exposure": 415282, "detector": i} for i in range(1, 63)]
    filterLabel = lsst.afw.image.FilterLabel(physical="r DECam SDSS c0002 6415.0 1480.0", band="r")

    @property
    def visits(self):
        butler = Butler(self.root, collections=[self.outputRun])
        return {
            DataCoordinate.standardize(
                instrument="DECam",
                visit=415282,
                universe=butler.dimensions
            ): [
                DataCoordinate.standardize(
                    instrument="DECam",
                    exposure=415282,
                    universe=butler.dimensions
                )
            ]
        }

    def checkRepo(self, files=None):
        """Additional tests run on post-ingest repos.

        See base class for additional information; note that using this hook
        rather than adding a new test_ method saves us from having to (slowly)
        run ingest again just to get a useful to repo to test against.
        """
        butler = Butler(self.root)
        # Test that packing visit+detector data IDs into integers yields
        # results consistent with what we have historically gotten (from Gen2).
        for dataId in self.dataIds:
            expandedDataId = butler.registry.expandDataId(dataId)
            packer = self.instrumentClass.make_default_dimension_packer(expandedDataId, is_exposure=True)
            packed, bits = packer.pack(expandedDataId, returnMaxBits=True)
            self.assertEqual(packed, int(f"{dataId['exposure']}{dataId['detector']:02}"))
            self.assertEqual(bits, 32)


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamIngestShuffledFullFileTestCase(DecamTestBase, lsst.utils.tests.TestCase):
    """Test ingesting a file that contains all detectors in a random order.
    """

    # No need to test writeCuratedCalibrations again
    curatedCalibrationDatasetTypes = None

    # Decam ingests every detector in each raw file, so we
    # only have to specify one file here, but should get many dataIds
    # in the output repo.
    @property
    def file(self):
        return os.path.join(testDataDirectory, "rawData", "raw",
                            "c4d_150227_012718_ori-stripped-shuffled.fits.fz")

    dataIds = [{"instrument": "DECam", "exposure": 415282, "detector": i} for i in range(1, 63)]
    filterLabel = lsst.afw.image.FilterLabel(physical="r DECam SDSS c0002 6415.0 1480.0", band="r")

    @property
    def visits(self):
        butler = Butler(self.root, collections=[self.outputRun])
        return {
            DataCoordinate.standardize(
                instrument="DECam",
                visit=415282,
                universe=butler.dimensions
            ): [
                DataCoordinate.standardize(
                    instrument="DECam",
                    exposure=415282,
                    universe=butler.dimensions
                )
            ]
        }


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
