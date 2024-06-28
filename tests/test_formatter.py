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

import contextlib
import astro_metadata_translator
import unittest
import os

import lsst.afw.geom
import lsst.utils.tests
import lsst.obs.decam
import lsst.daf.butler
import lsst.afw.image

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None

storageClass = lsst.daf.butler.StorageClassFactory().getStorageClass("ExposureI")


def _clean_metadata_provenance(hdr):
    """Remove metadata fix up provenance."""
    for k in hdr:
        if k.startswith("HIERARCH ASTRO METADATA"):
            print("DELETING A KEY>>>> ", k)
            del hdr[k]

    # Strip WCS for consistency (the formatter returns stripped headers).
    with contextlib.suppress(TypeError):
        lsst.afw.geom.stripWcsMetadata(hdr)


def make_dataset_ref(detector: int) -> lsst.daf.butler.DatasetRef:
    universe = lsst.daf.butler.DimensionUniverse()
    dataset_type = lsst.daf.butler.DatasetType(
        "raw",
        ("instrument", "detector"),
        storageClass,
        universe=universe,
    )
    data_id = lsst.daf.butler.DataCoordinate.standardize(
        instrument="HSC", detector=detector, universe=universe
    )
    return lsst.daf.butler.DatasetRef(dataset_type, data_id, "test")


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DarkEnergyCameraRawFormatterTestCase(lsst.utils.tests.TestCase):
    maxDiff = None

    def setUp(self):
        path = 'rawData/2013-09-01/z/decam0229388.fits.fz'
        self.filename = os.path.join(testDataDirectory, path)
        location = lsst.daf.butler.Location(testDataDirectory, path)
        self.fileDescriptor = lsst.daf.butler.FileDescriptor(location, storageClass)

    def check_readMetadata(self, detector, expected):
        formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(
            self.fileDescriptor, ref=make_dataset_ref(detector)
        )
        metadata = formatter.read(component="metadata")

        # Remove provenance
        _clean_metadata_provenance(metadata)
        _clean_metadata_provenance(expected)

        self.assertEqual(metadata.toDict(), expected.toDict())

    def test_readMetadata(self):
        # detector 25 is in HDU 1
        expected = lsst.afw.fits.readMetadata(self.filename, 1)
        self.assertEqual(expected['CCDNUM'], 25)  # sanity check
        self.check_readMetadata(25, expected)

        # detector 1 is in HDU 2
        expected = lsst.afw.fits.readMetadata(self.filename, 2)
        astro_metadata_translator.fix_header(expected)
        self.assertEqual(expected['CCDNUM'], 1)  # sanity check
        self.check_readMetadata(1, expected)

    def test_readMetadata_raises(self):
        formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(
            self.fileDescriptor, ref=make_dataset_ref(70)
        )
        with self.assertRaisesRegex(ValueError, "detectorId=70"):
            formatter.read(component="metadata")

    def check_readImage(self, detector, expected):
        formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(
            self.fileDescriptor, ref=make_dataset_ref(detector)
        )
        image = formatter.read(component="image")
        self.assertImagesEqual(image, expected)

    def test_readImage(self):
        # detector 25 is in HDU 1
        expected = lsst.afw.image.ImageI(self.filename, 1)
        self.check_readImage(25, expected)

        # detector 1 is in HDU 2
        expected = lsst.afw.image.ImageI(self.filename, 2)
        self.check_readImage(1, expected)

    def test_readMetadata_full_file(self):
        """Test reading a file with all HDUs, and with all HDUs in a shuffled
        order.
        """

        full_file = 'rawData/raw/c4d_150227_012718_ori-stripped.fits.fz'
        full_location = lsst.daf.butler.Location(testDataDirectory, full_file)
        full_fileDescriptor = lsst.daf.butler.FileDescriptor(full_location, storageClass)

        shuffled_file = 'rawData/raw/c4d_150227_012718_ori-stripped-shuffled.fits.fz'
        shuffled_location = lsst.daf.butler.Location(testDataDirectory, shuffled_file)
        shuffled_fileDescriptor = lsst.daf.butler.FileDescriptor(shuffled_location, storageClass)

        for detector in range(1, 63):
            formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(
                full_fileDescriptor, ref=make_dataset_ref(detector)
            )
            full_metadata = formatter.read(component="metadata")

            formatter = lsst.obs.decam.DarkEnergyCameraRawFormatter(
                shuffled_fileDescriptor, ref=make_dataset_ref(detector)
            )
            shuffled_metadata = formatter.read(component="metadata")

            # Remove provenance
            _clean_metadata_provenance(full_metadata)
            _clean_metadata_provenance(shuffled_metadata)

            # the metadata should be the same in both files.
            self.assertEqual(shuffled_metadata.toDict(), full_metadata.toDict())


@unittest.skipIf(testDataDirectory is None, "testdata_decam must be set up")
class DarkEnergyCameraCPCalibFormatterTestCase(lsst.utils.tests.TestCase):
    """DECam Community Pipeline calibrations have one detector per HDU.
    """
    def setUp(self):
        path = 'hits2015-zeroed/c4d_150218_191721_zci_v1.fits.fz'
        self.biasFile = os.path.join(testDataDirectory, path)
        location = lsst.daf.butler.Location(testDataDirectory, path)
        self.biasDescriptor = lsst.daf.butler.FileDescriptor(location, storageClass)

        path = 'hits2015-zeroed/c4d_150218_200522_fci_g_v1.fits.fz'
        self.flatFile = os.path.join(testDataDirectory, path)
        location = lsst.daf.butler.Location(testDataDirectory, path)
        self.flatDescriptor = lsst.daf.butler.FileDescriptor(location, storageClass)

    def check_readMetadata(self, detector, expected, fileDescriptor):
        formatter = lsst.obs.decam.DarkEnergyCameraCPCalibFormatter(
            fileDescriptor, ref=make_dataset_ref(detector)
        )
        metadata = formatter.read(component="metadata")
        self.assertEqual(metadata['CCDNUM'], detector, f"detector={detector}")

        # Remove provenance
        _clean_metadata_provenance(metadata)
        _clean_metadata_provenance(expected)

        self.assertEqual(metadata.toDict(), expected.toDict(), msg=f"Detector {detector}")

    def test_readMetadata(self):
        for i in range(1, 63):
            expected = lsst.afw.fits.readMetadata(self.biasFile, i)
            self.check_readMetadata(i, expected, self.biasDescriptor)

            expected = lsst.afw.fits.readMetadata(self.flatFile, i)
            self.check_readMetadata(i, expected, self.flatDescriptor)


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
