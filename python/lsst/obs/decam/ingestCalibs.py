import collections
import re
from lsst.pipe.tasks.ingestCalibs import CalibsParseTask

class DecamCalibsParseTask(CalibsParseTask):
    def getInfo(self, filename):
        """Get information about the image from the filename and/or its contents

        @param filename: Name of file to inspect
        @return File properties; list of file properties for each extension
        """
        phuInfo, infoList = CalibsParseTask.getInfo(self, filename)
        # Single-extension fits without EXTNAME can be a valid CP calibration product
        # Use info of primary header unit
        if not infoList:
            infoList.append(phuInfo)
        return phuInfo, infoList

    def translate_ccdnum(self, md):
        """Return CCDNUM as a integer

        @param md (PropertySet) FITS header metadata
        """
        if md.exists("CCDNUM"):
            ccdnum = md.get("CCDNUM")
        else:
            self.log.warn("Unable to find value for CCDNUM")
            ccdnum = None
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
        else:
            self.log.warn("Unable to find value for DATE-OBS")
            date = "unknown"
        return date

    @staticmethod
    def getExtensionName(md):
        """ Get the name of the extension

        @param md (PropertySet) FITS header metadata
        """
        return md.get('EXTNAME')
