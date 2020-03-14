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

"""Unit tests for gen3 DECam raw formatter, which has to determine which
HDU a given detector is in in a multi-extension FITS file.
"""

import astro_metadata_translator
import unittest
import os

import lsst.utils.tests
import lsst.obs.decam
import lsst.daf.butler
import lsst.afw.image

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DarkEnergyCameraRawFormatterTestCase(lsst.utils.tests.TestCase):
    def setUp(self):
        path = 'rawData/2013-09-01/z/decam0229388.fits.fz'
        self.filename = os.path.join(testDataDirectory, path)
        location = lsst.daf.butler.Location(testDataDirectory, path)
        self.fileDescriptor = lsst.daf.butler.FileDescriptor(location, None)

    def check_readMetadata(self, dataId, expected):
        formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(self.fileDescriptor, dataId)
        metadata = formatter.readMetadata()
        self.assertEqual(metadata, expected)

    def test_readMetadata(self):
        dataId = {'detector': 25}
        # detector 25 is in HDU 1
        expected = lsst.afw.image.readMetadata(self.filename, 1)
        self.assertEqual(expected['CCDNUM'], 25)  # sanity check
        self.check_readMetadata(dataId, expected)

        dataId = {'detector': 1}
        # detector 1 is in HDU 2
        expected = lsst.afw.image.readMetadata(self.filename, 2)
        astro_metadata_translator.fix_header(expected)
        self.assertEqual(expected['CCDNUM'], 1)  # sanity check
        self.check_readMetadata(dataId, expected)

    def test_readMetadata_raises(self):
        dataId = {'detector': 70}
        formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(self.fileDescriptor, dataId)
        with self.assertRaisesRegex(ValueError, "detectorId=70"):
            formatter.readMetadata()

    def check_readImage(self, dataId, expected):
        formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(self.fileDescriptor, dataId)
        image = formatter.readImage()
        self.assertImagesEqual(image, expected)

    def test_readImage(self):
        dataId = {'detector': 25}
        # detector 25 is in HDU 1
        expected = lsst.afw.image.ImageI(self.filename, 1)
        self.check_readImage(dataId, expected)

        dataId = {'detector': 1}
        # detector 1 is in HDU 2
        expected = lsst.afw.image.ImageI(self.filename, 2)
        self.check_readImage(dataId, expected)

    def test_readMetadata_full_file(self):
        """Test reading a file with all HDUs, and with all HDUs in a shuffled
        order.
        """

        full_file = 'rawData/raw/c4d_150227_012718_ori-stripped.fits.fz'
        full_location = lsst.daf.butler.Location(testDataDirectory, full_file)
        full_fileDescriptor = lsst.daf.butler.FileDescriptor(full_location, None)

        shuffled_file = 'rawData/raw/c4d_150227_012718_ori-stripped-shuffled.fits.fz'
        shuffled_location = lsst.daf.butler.Location(testDataDirectory, shuffled_file)
        shuffled_fileDescriptor = lsst.daf.butler.FileDescriptor(shuffled_location, None)

        for detector in range(1, 63):
            formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(full_fileDescriptor, detector)
            full_index, full_metadata = formatter._determineHDU(detector)
            formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(shuffled_fileDescriptor, detector)
            shuffled_index, shuffled_metadata = formatter._determineHDU(detector)

            # The shuffled file should have different indices,
            self.assertNotEqual(full_index, shuffled_index)
            # but the metadata should be the same in both files.
            self.assertEqual(shuffled_metadata, full_metadata)


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DarkEnergyCameraCPCalibFormatterTestCase(lsst.utils.tests.TestCase):
    """DECam Community Pipeline calibrations have one detector per HDU.
    """
    def setUp(self):
        path = 'hits2015-zeroed/c4d_150218_191721_zci_v1.fits.fz'
        self.biasFile = os.path.join(testDataDirectory, path)
        location = lsst.daf.butler.Location(testDataDirectory, path)
        self.biasDescriptor = lsst.daf.butler.FileDescriptor(location, None)

        path = 'hits2015-zeroed/c4d_150218_200522_fci_g_v1.fits.fz'
        self.flatFile = os.path.join(testDataDirectory, path)
        location = lsst.daf.butler.Location(testDataDirectory, path)
        self.flatDescriptor = lsst.daf.butler.FileDescriptor(location, None)

    def check_readMetadata(self, dataId, expected, fileDescriptor):
        formatter = lsst.obs.decam.DarkEnergyCameraCPCalibFormatter(fileDescriptor, dataId)
        metadata = formatter.readMetadata()
        self.assertEqual(metadata['CCDNUM'], dataId['detector'], dataId)
        self.assertEqual(metadata, expected, msg=dataId)

    def test_readMetadata(self):
        for i in range(1, 63):
            dataId = {'detector': i}
            expected = lsst.afw.image.readMetadata(self.biasFile, i)
            self.check_readMetadata(dataId, expected, self.biasDescriptor)

            expected = lsst.afw.image.readMetadata(self.flatFile, i)
            self.check_readMetadata(dataId, expected, self.flatDescriptor)


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
