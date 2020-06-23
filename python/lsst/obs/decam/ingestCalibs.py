
import collections.abc
import re
from lsst.afw.fits import readMetadata
from lsst.pipe.tasks.ingestCalibs import CalibsParseTask

__all__ = ["DecamCalibsParseTask"]


class DecamCalibsParseTask(CalibsParseTask):
    """Parse calibration products for ingestion.

    Handle either DECam Community Pipeline calibration products or
    calibration products produced with the LSST Science Pipelines
    (i.e., pipe_drivers' constructBias.py and constructFlat.py).
    """

    def getInfo(self, filename):
        """Retrieve path, calib_hdu, and possibly calibDate.

        Parameters
        ----------
        filename: `str`
            Calibration file to inspect.

        Returns
        -------
        phuInfo : `dict`
            Primary header unit info.
        infoList : `list` of `dict`
            List of file properties to use for each extension.
        """
        phuInfo, infoList = CalibsParseTask.getInfo(self, filename)
        # In practice, this returns an empty dict
        # and a list containing an empty dict.
        for item in infoList:
            item['path'] = filename
            try:
                item['calib_hdu'] = item['hdu']
            except KeyError:  # calib_hdu is required for the calib registry
                item['calib_hdu'] = 1
        # Try to fetch a date from filename
        # and use as the calibration dates if not already set
        found = re.search(r'(\d\d\d\d-\d\d-\d\d)', filename)
        if found:
            date = found.group(1)
            for info in infoList:
                if 'calibDate' not in info or info['calibDate'] == "unknown":
                    info['calibDate'] = date
        return phuInfo, infoList

    def _translateFromCalibId(self, field, md):
        """Fetch the ID from the CALIB_ID header.

        Calibration products made with constructCalibs have some metadata
        saved in its FITS header CALIB_ID.
        """
        data = md["CALIB_ID"]
        match = re.search(r".*%s=(\S+)" % field, data)
        return match.groups()[0]

    def translate_ccdnum(self, md):
        """Return CCDNUM as a integer.

        Parameters
        ----------
        md : `lsst.daf.base.PropertySet`
            FITS header metadata.
        """
        if "CCDNUM" in md:
            ccdnum = md["CCDNUM"]
        else:
            return self._translateFromCalibId("ccdnum", md)
        # Some MasterCal from NOAO Archive has 2 CCDNUM keys in each HDU
        # Make sure only one integer is returned.
        if isinstance(ccdnum, collections.abc.Sequence):
            try:
                ccdnum = ccdnum[0]
            except IndexError:
                ccdnum = None
        return ccdnum

    def translate_date(self, md):
        """Extract the date as a strong in format YYYY-MM-DD from the FITS header DATE-OBS.
        Return "unknown" if the value cannot be found or converted.

        Parameters
        ----------
        md : `lsst.daf.base.PropertySet`
            FITS header metadata.
        """
        if "DATE-OBS" in md:
            date = md["DATE-OBS"]
            found = re.search(r'(\d\d\d\d-\d\d-\d\d)', date)
            if found:
                date = found.group(1)
            else:
                self.log.warn("DATE-OBS does not match format YYYY-MM-DD")
                date = "unknown"
        elif "CALIB_ID" in md:
            date = self._translateFromCalibId("calibDate", md)
        else:
            date = "unknown"
        return date

    def translate_filter(self, md):
        """Extract the filter name.

        Translate a full filter description into a mere filter name.
        Return "unknown" if the keyword FILTER does not exist in the header,
        which can happen for some valid Community Pipeline products.

        Parameters
        ----------
        md : `lsst.daf.base.PropertySet`
            FITS header metadata.

        Returns
        -------
        filter : `str`
            The name of the filter to use in the calib registry.
        """
        if "FILTER" in md:
            if "OBSTYPE" in md:
                obstype = md["OBSTYPE"].strip().lower()
                if "zero" in obstype or "bias" in obstype:
                    return "NONE"
            filterName = CalibsParseTask.translate_filter(self, md)
            # TODO (DM-24514): remove workaround if/else
            if filterName == '_unknown_' and "CALIB_ID" in md:
                return self._translateFromCalibId("filter", md)
            else:
                return CalibsParseTask.translate_filter(self, md)
        elif "CALIB_ID" in md:
            return self._translateFromCalibId("filter", md)
        else:
            return "unknown"

    def getDestination(self, butler, info, filename):
        """Get destination for the file.

        Parameters
        ----------
        butler : `lsst.daf.persistence.Butler`
            Data butler.
        info : data ID
            File properties, used as dataId for the butler.
        filename : `str`
            Input filename.

        Returns
        -------
        raw : `str`
            Destination filename.
        """
        calibType = self.getCalibType(filename)
        md = readMetadata(filename, self.config.hdu)
        if "PROCTYPE" not in md:
            raise RuntimeError(f"Unable to find the calib header keyword PROCTYPE \
                               in {filename}, hdu {self.config.hdu}")
        proctype = md["PROCTYPE"].strip()
        if "MasterCal" in proctype:  # DECam Community Pipeline calibration product case
            # Arbitrarily set ccdnum and calib_hdu to 1 to make the mapper template happy
            info["ccdnum"] = 1
            info["calib_hdu"] = 1
            if "flat" in calibType.lower():
                raw = butler.get("cpFlat_filename", info)[0]
            elif ("bias" or "zero") in calibType.lower():
                raw = butler.get("cpBias_filename", info)[0]
            elif ("illumcor") in calibType.lower():
                raw = butler.get("cpIllumcor_filename", info)[0]
            else:
                raise RuntimeError(f"Invalid DECam Community Pipeline calibType {calibType}")
        else:  # LSST-built calibration product case
            raw = butler.get(calibType + "_filename", info)[0]
        # Remove HDU extension (ccdnum) since we want to refer to the whole file
        c = raw.find("[")
        if c > 0:
            raw = raw[:c]
        return raw
