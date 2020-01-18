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
from lsst.obs.base.fitsRawFormatterBase import FitsRawFormatterBase

from . import DarkEnergyCamera

__all__ = ("DarkEnergyCameraRawFormatter",)


class DarkEnergyCameraRawFormatter(FitsRawFormatterBase):
    translatorClass = astro_metadata_translator.DecamTranslator
    filterDefinitions = DarkEnergyCamera.filterDefinitions

    def getDetector(self, id):
        return DarkEnergyCamera().getCamera()[id]

    def _determineHDU(self, detectorId):
        """Determine the correct HDU number for a given detector id.

        Returns
        -------
        fitsData: `lsst.afw.fits.Fits`
            An read-only struct for accessing the required HDU.
        metadata: `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.

        Raises
        ------
        RuntimeError
            Raised if detectorId is not found in any of the file HDUs
        """
        filename = self.fileDescriptor.location.path
        fitsData = lsst.afw.fits.Fits(filename, 'r')
        # NOTE: The primary header (HDU=0) does not contain detector data.
        for i in range(1, fitsData.countHdus()):
            fitsData.setHdu(i)
            metadata = fitsData.readMetadata()
            if metadata['CCDNUM'] == detectorId:
                return fitsData, metadata
        else:
            raise ValueError(f"Did not find detectorId={detectorId} as CCDNUM in any HDU of {filename}.")

    def readMetadata(self):
        fitsData, metadata = self._determineHDU(self.dataId['detector'])
        astro_metadata_translator.fix_header(metadata)
        return metadata

    def readImage(self):
        fitsData, metadata = self._determineHDU(self.dataId['detector'])
        return lsst.afw.image.ImageI(fitsData.readImageI())
