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

"""Gen3 Butler Formatters for Dark Energy Camera raw data.
"""

import astro_metadata_translator

import lsst.afw.fits
import lsst.afw.image
import lsst.log
from lsst.obs.base import FitsRawFormatterBase

from . import DarkEnergyCamera

__all__ = ("DarkEnergyCameraRawFormatter", "DarkEnergyCameraCPCalibFormatter")


# The mapping of detector id to HDU in raw files for "most" DECam data.
# We try this first before scaning the HDUs manually.
detector_to_hdu = {25: 1, 26: 2, 27: 3, 32: 4, 33: 5, 34: 6, 19: 7, 20: 8, 13: 9,
                   14: 10, 8: 11, 4: 12, 39: 13, 40: 14, 45: 15, 46: 16, 51: 17, 56: 18, 21: 19,
                   22: 20, 23: 21, 24: 22, 17: 23, 18: 24, 15: 25, 16: 26, 9: 27, 10: 28, 11: 29,
                   12: 30, 5: 31, 6: 32, 7: 33, 1: 34, 2: 35, 3: 36, 35: 37, 36: 38, 37: 39,
                   38: 40, 28: 41, 29: 42, 30: 43, 31: 44, 41: 45, 42: 46, 43: 47, 44: 48, 49: 49,
                   50: 50, 47: 51, 48: 52, 52: 53, 53: 54, 54: 55, 55: 56, 57: 57, 58: 58, 59: 59,
                   60: 60, 61: 61, 62: 62, 72: 63, 71: 64, 64: 65, 63: 66, 73: 67, 74: 68, 70: 69,
                   69: 70
                   }


class DarkEnergyCameraRawFormatter(FitsRawFormatterBase):
    translatorClass = astro_metadata_translator.DecamTranslator
    filterDefinitions = DarkEnergyCamera.filterDefinitions

    # DECam has a coordinate system flipped on X with respect to our
    # VisitInfo definition of the field angle orientation.
    # We have to specify the flip explicitly until DM-20746 is implemented.
    wcsFlipX = True

    def getDetector(self, id):
        return DarkEnergyCamera().getCamera()[id]

    def _scanHdus(self, filename, detectorId):
        """Scan through a file for the HDU containing data from one detector.

        Parameters
        ----------
        filename : `str`
            The file to search through.
        detectorId : `int`
            The detector id to search for.

        Returns
        -------
        index : `int`
            The index of the HDU with the requested data.
        metadata: `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.

        Raises
        ------
        ValueError
            Raised if detectorId is not found in any of the file HDUs
        """
        log = lsst.log.Log.getLogger("DarkEnergyCameraRawFormatter")
        log.debug("Did not find detector=%s at expected HDU=%s in %s: scanning through all HDUs.",
                  detectorId, detector_to_hdu[detectorId], filename)

        fitsData = lsst.afw.fits.Fits(filename, 'r')
        # NOTE: The primary header (HDU=0) does not contain detector data.
        for i in range(1, fitsData.countHdus()):
            fitsData.setHdu(i)
            metadata = fitsData.readMetadata()
            if metadata['CCDNUM'] == detectorId:
                return i, metadata
        else:
            raise ValueError(f"Did not find detectorId={detectorId} as CCDNUM in any HDU of {filename}.")

    def _determineHDU(self, detectorId):
        """Determine the correct HDU number for a given detector id.

        Parameters
        ----------
        detectorId : `int`
            The detector id to search for.

        Returns
        -------
        index : `int`
            The index of the HDU with the requested data.
        metadata : `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.

        Raises
        ------
        ValueError
            Raised if detectorId is not found in any of the file HDUs
        """
        filename = self.fileDescriptor.location.path
        try:
            index = detector_to_hdu[detectorId]
            metadata = lsst.afw.image.readMetadata(filename, index)
            if metadata['CCDNUM'] != detectorId:
                # the detector->HDU mapping is different in this file: try scanning
                return self._scanHdus(filename, detectorId)
            else:
                fitsData = lsst.afw.fits.Fits(filename, 'r')
                fitsData.setHdu(index)
                return index, metadata
        except lsst.afw.fits.FitsError:
            # if the file doesn't contain all the HDUs of "normal" files, try scanning
            return self._scanHdus(filename, detectorId)

    def readMetadata(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        astro_metadata_translator.fix_header(metadata)
        return metadata

    def readImage(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        return lsst.afw.image.ImageI(self.fileDescriptor.location.path, index)


class DarkEnergyCameraCPCalibFormatter(DarkEnergyCameraRawFormatter):
    """DECam Community Pipeline calibrations (bias, dark, flat, fringe) are
    multi-extension FITS files with detector=index+1.
    """

    def _determineHDU(self, detectorId):
        """The HDU to read is the same as the detector number."""
        filename = self.fileDescriptor.location.path
        metadata = lsst.afw.image.readMetadata(filename, detectorId)
        if metadata['CCDNUM'] != detectorId:
            msg = f"Found CCDNUM={metadata['CCDNUM']} instead of {detectorId} in {filename} HDU={detectorId}."
            raise ValueError(msg)
        return detectorId, metadata

    def readImage(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        return lsst.afw.image.ImageF(self.fileDescriptor.location.path, index)
