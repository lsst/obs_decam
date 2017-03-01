from __future__ import absolute_import, division, print_function

import collections
import re
from glob import glob
from lsst.pipe.tasks.ingestCalibs import CalibsParseTask
from lsst.pipe.tasks.ingestCalibs import IngestCalibsTask
from lsst.pipe.tasks.ingestCalibs import IngestCalibsConfig, IngestCalibsArgumentParser
from lsst.pex.config import Field


class DecamCalibsParseTask(CalibsParseTask):
    def _translateFromCalibId(self, field, md):
        """Fetch the ID from the CALIB_ID header.
        Calibration products made with constructCalibs have some metadata
        saved in its FITS header CALIB_ID.
        """
        data = md.get("CALIB_ID")
        match = re.search(".*%s=(\S+)" % field, data)
        return match.groups()[0]

    def translate_ccdnum(self, md):
        """Return CCDNUM as a integer

        @param md (PropertySet) FITS header metadata
        """
        if md.exists("CCDNUM"):
            ccdnum = md.get("CCDNUM")
        else:
            return self._translateFromCalibId("ccdnum", md)
        # Some MasterCal from NOAO Archive has 2 CCDNUM keys in each HDU
        # Make sure only one integer is returned.
        if isinstance(ccdnum, collections.Sequence):
            try:
                ccdnum = ccdnum[0]
            except IndexError:
                ccdnum = None
        return ccdnum

    def translate_date(self, md):
        """Extract the date as a strong in format YYYY-MM-DD from the FITS header DATE-OBS.
        Return "unknown" if the value cannot be found or converted.

        @param md (PropertySet) FITS header metadata
        """
        if md.exists("DATE-OBS"):
            date = md.get("DATE-OBS")
            found = re.search('(\d\d\d\d-\d\d-\d\d)', date)
            if found:
                date = found.group(1)
            else:
                self.log.warn("DATE-OBS does not match format YYYY-MM-DD")
                date = "unknown"
        elif md.exists("CALIB_ID"):
            date = self._translateFromCalibId("calibDate", md)
        else:
            date = "unknown"
        return date

    def translate_filter(self, md):
        """Extract the filter name

        Translate a full filter description into a mere filter name.
        Return "unknown" if the keyword FILTER does not exist in the header,
        which can happen for some valid Community Pipeline products.

        @param md (PropertySet) FITS header metadata
        """
        if md.exists("FILTER"):
            if md.exists("OBSTYPE") and "zero" in md.get("OBSTYPE").strip().lower():
                return "NONE"
            return CalibsParseTask.translate_filter(self, md)
        elif md.exists("CALIB_ID"):
            return self._translateFromCalibId("filter", md)
        else:
            return "unknown"

    @staticmethod
    def getExtensionName(md):
        """ Get the name of the extension

        @param md (PropertySet) FITS header metadata
        """
        return md.get('EXTNAME')

    def getDestination(self, butler, info, filename):
        """Get destination for the file

        @param butler      Data butler
        @param info        File properties, used as dataId for the butler
        @param filename    Input filename
        @return Destination filename
        """
        # Arbitrarily set ccdnum = 1 to make the mapper template happy
        info["ccdnum"] = 1
        calibType = self.getCalibType(filename)
        if "flat" in calibType.lower():
            raw = butler.get("cpFlat_filename", info)[0]
        elif ("bias" or "zero") in calibType.lower():
            raw = butler.get("cpBias_filename", info)[0]
        else:
            assert False, "Invalid calibType '{:s}'".format(calibType)
        # Remove HDU extension (ccdnum) since we want to refer to the whole file
        c = raw.find("[")
        if c > 0:
            raw = raw[:c]
        return raw
