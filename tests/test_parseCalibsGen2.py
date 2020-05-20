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

"""Unit tests for gen2 DECam calibration product parsing, a precursor to ingestion.
"""

import unittest
import os
import lsst.utils.tests
from lsst.obs.decam import ingestCalibs
import lsst.daf.persistence as dafPersist
from lsst.afw.fits import readMetadata

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DecamCalibsParseTaskTestCase(lsst.utils.tests.TestCase):
    """Test the methods in DecamCalibsParseTask.

    Uses a bias+flat pair of LSST-Science-Pipeline-built calibs as well as
    a bias+flat pair of DECam Community Pipeline calibs, all full of zeros,
    which live in testdata_decam.
    """
    def setUp(self):
        self.task = ingestCalibs.DecamCalibsParseTask(name='ItsATest')

        # LSST-Science-Pipeline-built calibration products, full of zeros
        self.biasFile = os.path.join(testDataDirectory, "pipeline-calibs", "BIAS", "BIAS-47.fits")
        self.flatFile = os.path.join(testDataDirectory, "pipeline-calibs", "FLAT", "FLAT-g-47.fits")

        # DECam Community Pipeline calibration products, also full of zeros
        cpBiasFilename = "c4d_150218_191721_zci_v1.fits.fz"
        self.cpBiasFile = os.path.join(testDataDirectory, "hits2015-zeroed", cpBiasFilename)
        cpFlatFilename = "c4d_150218_200522_fci_g_v1.fits.fz"
        self.cpFlatFile = os.path.join(testDataDirectory, "hits2015-zeroed", cpFlatFilename)

        # A Butler repository with ingested raws and Community Pipeline calibs
        repo = os.path.join(testDataDirectory, "ingested")
        calibRepo = os.path.join(testDataDirectory, "calibingested")
        self.butler = dafPersist.Butler(root=repo, calibRoot=calibRepo)

    def checkGetInfo(self, filename):
        """Test that the filepath and a calib_hdu value of 1 is in the info.
        """
        phuInfo, infoList = self.task.getInfo(filename)
        self.assertEqual(phuInfo['calib_hdu'], 1)
        self.assertIn('path', phuInfo)
        for item in infoList:
            self.assertEqual(item['calib_hdu'], 1)
            self.assertIn('path', item)

    def testLsstCalibsGetInfo(self):
        """Test that the filepath and a calib_hdu value of 1 is in the info.
        """
        # LSST-Science-Pipelines-built bias
        self.checkGetInfo(self.biasFile)

        # LSST-Science-Pipelines-built flat
        self.checkGetInfo(self.flatFile)

    def testLsstCalibsGetDestination(self):
        """Test that file path destinations conform to the mapper templates.
        """
        # LSST-Science-Pipelines-built bias
        dataId = {'ccdnum': 1, 'date': '2015-02-18'}
        filename = self.task.getDestination(self.butler, dataId, self.biasFile)
        self.assertIn(f"BIAS/{dataId['date']}/BIAS-{dataId['date']}-{dataId['ccdnum']:02}.fits", filename)
        self.assertNotIn('[', filename)

        # LSST-Science-Pipelines-built flat
        dataId = {'ccdnum': 1, 'date': '2015-02-18', 'filter': 'g'}
        filename = self.task.getDestination(self.butler, dataId, self.flatFile)
        self.assertIn(f"FLAT/{dataId['date']}/{dataId['filter']}/"
                      + f"FLAT-{dataId['date']}-{dataId['ccdnum']:02}.fits", filename)
        self.assertNotIn('[', filename)

    def testLsstCalibsTranslateFilter(self):
        """Test that filter is set to "NONE" for the bias and "g" for the flat.
        """
        # LSST-Science-Pipelines-built bias
        md = readMetadata(self.biasFile, self.task.config.hdu)
        biasFilter = self.task.translate_filter(md)
        self.assertEqual(biasFilter, "NONE")

        # LSST-Science-Pipelines-built flat
        md = readMetadata(self.flatFile, self.task.config.hdu)
        flatFilter = self.task.translate_filter(md)
        self.assertEqual(flatFilter, "g")

    def testCpCalibsGetInfo(self):
        """Test that the filepath and a calib_hdu value of 1 is in the info.
        """
        # DECam Community Pipeline bias
        self.checkGetInfo(self.cpBiasFile)

        # DECam Community Pipeline flat
        self.checkGetInfo(self.cpFlatFile)

    def testCpCalibsGetDestination(self):
        """Test that file path destinations conform to the mapper templates.
        """
        # DECam Community Pipeline bias
        dataId = {'ccdnum': 1, 'date': '2015-02-18'}
        filename = self.task.getDestination(self.butler, dataId, self.cpBiasFile)
        self.assertIn(f"cpBIAS/{dataId['date']}/BIAS-{dataId['date']}.fits", filename)
        self.assertNotIn('[', filename)

        # DECam Community Pipeline flat
        dataId = {'ccdnum': 1, 'date': '2015-02-18', 'filter': 'g'}
        filename = self.task.getDestination(self.butler, dataId, self.cpFlatFile)
        self.assertIn(f"cpFLAT/{dataId['date']}/{dataId['filter']}/FLAT-{dataId['date']}.fits", filename)
        self.assertNotIn('[', filename)

    def testCpCalibsTranslateFilter(self):
        """Test that filter is set to "NONE" for the cpBias and "g" for the cpFlat.
        """
        # DECam Community Pipeline bias
        md = readMetadata(self.cpBiasFile, self.task.config.hdu)
        cpBiasFilter = self.task.translate_filter(md)
        self.assertEqual(cpBiasFilter, "NONE")

        # DECam Community Pipeline flat
        md = readMetadata(self.cpFlatFile, self.task.config.hdu)
        cpFlatFilter = self.task.translate_filter(md)
        self.assertEqual(cpFlatFilter, "g")


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
