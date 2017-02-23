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
        if "flat" in info.get("obstype").strip().lower():
            raw = butler.get("cpFlat_filename", info)[0]
        elif info.get("obstype").strip().lower() == "zero":
            raw = butler.get("cpBias_filename", info)[0]
        else:
            assert False, "Invalid OBSTYPE '{:s}'".format(info.get("obstype"))
        # Remove HDU extension (ccdnum) since we want to refer to the whole file
        c = raw.find("[")
        if c > 0:
            raw = raw[:c]
        return raw


class DecamIngestCalibsArgumentParser(IngestCalibsArgumentParser):
    """Argument parser to support ingesting calibration images into the repository"""
    def __init__(self, *args, **kwargs):
        IngestCalibsArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument("--mode", choices=["move", "copy", "link", "skip"], default="link",
                          help="Mode of delivering the files to their destination")


class DecamIngestCalibsConfig(IngestCalibsConfig):
    """Configuration for DecamIngestCalibsTask"""
    allowError = Field(dtype=bool, default=False, doc="Allow error in ingestion?")
    clobber = Field(dtype=bool, default=False, doc="Clobber existing file?")


class DecamIngestCalibsTask(IngestCalibsTask):
    """Task that generates registry for decam calibration images"""
    ConfigClass = DecamIngestCalibsConfig
    ArgumentParser = DecamIngestCalibsArgumentParser
    _DefaultName = "decamIngestCalibs"

    def run(self, args):
        """Ingest all specified files and add them to the registry"""
        calibRoot = args.calib if args.calib is not None else "."
        filenameList = sum([glob(filename) for filename in args.files], [])
        with self.register.openRegistry(calibRoot, create=args.create, dryrun=args.dryrun) as registry:
            for infile in filenameList:
                fileInfo, hduInfoList = self.parse.getInfo(infile)
                if args.calibType is None:
                    calibType = self.parse.getCalibType(infile)
                else:
                    calibType = args.calibType
                if calibType not in self.register.config.tables:
                    self.log.warn(str("Skipped adding %s of observation type '%s' to registry" %
                                      (infile, calibType)))
                    continue
                outfile = self.parse.getDestination(args.butler, fileInfo, infile)
                ingested = self.ingest(infile, outfile, mode=args.mode, dryrun=args.dryrun)
                if not ingested:
                    continue
                for info in hduInfoList:
                    self.register.addRow(registry, info, dryrun=args.dryrun,
                                         create=args.create, table=calibType)
            if not args.dryrun:
                self.register.updateValidityRanges(registry, args.validity)
            else:
                self.log.info("Would update validity ranges here, but dryrun")
