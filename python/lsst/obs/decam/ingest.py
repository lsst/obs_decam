#
# LSST Data Management System
# Copyright 2012,2015 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import os
import re


from lsst.daf.butler import ButlerURI, Formatter
from astro_metadata_translator import fix_header, DecamTranslator
from lsst.afw.fits import readMetadata
from lsst.pipe.tasks.ingest import ParseTask, IngestTask, IngestArgumentParser
from lsst.obs.base.ingest import RawFileData
import lsst.obs.base

__all__ = ["DecamRawIngestTask", "DecamIngestArgumentParser", "DecamIngestTask", "DecamParseTask"]


class DecamRawIngestTask(lsst.obs.base.RawIngestTask):
    """Task for ingesting raw DECam data into a Gen3 Butler repository.
    """
    def extractMetadata(self, filename: ButlerURI) -> RawFileData:
        datasets = []
        try:
            with filename.as_local() as local_file:
                fitsData = lsst.afw.fits.Fits(local_file.ospath, 'r')
                # NOTE: The primary header (HDU=0) does not contain detector data.
                for i in range(1, fitsData.countHdus()):
                    fitsData.setHdu(i)
                    header = fitsData.readMetadata()
                    if header['CCDNUM'] > 62:  # ignore the guide CCDs
                        continue
                    datasets.append(self._calculate_dataset_info(header, filename))
        except Exception as e:
            self.log.debug("Problem extracting metadata from %s: %s", filename, e)
            # Indicate to the caller that we failed to read.
            # Do not try to ingest partial contents of file.
            datasets = []
            formatterClass = Formatter
            instrument = None
            self._on_metadata_failure(filename, e)
            if self.config.failFast:
                raise RuntimeError(f"Problem extracting metadata for file {filename}") from e
        else:
            # The data model currently assumes that whilst multiple datasets
            # can be associated with a single file, they must all share the
            # same formatter.
            instrument, formatterClass = self._determine_instrument_formatter(datasets[0].dataId, filename)
            if instrument is None:
                datasets = []

        self.log.debug(f"Found images for {len(datasets)} detectors in {filename}")
        return RawFileData(datasets=datasets, filename=filename,
                           FormatterClass=formatterClass,
                           instrumentClass=type(instrument))


class DecamIngestArgumentParser(IngestArgumentParser):
    """Gen2 DECam ingest additional arguments.
    """

    def __init__(self, *args, **kwargs):
        super(DecamIngestArgumentParser, self).__init__(*args, **kwargs)
        self.add_argument("--filetype", default="raw", choices=["instcal", "raw"],
                          help="Data processing level of the files to be ingested")


class DecamIngestTask(IngestTask):
    """Gen2 DECam file ingest task.
    """
    ArgumentParser = DecamIngestArgumentParser

    def __init__(self, *args, **kwargs):
        super(DecamIngestTask, self).__init__(*args, **kwargs)

    def run(self, args):
        """Ingest all specified files and add them to the registry
        """
        if args.filetype == "instcal":
            root = args.input
            with self.register.openRegistry(root, create=args.create, dryrun=args.dryrun) as registry:
                for infile in args.files:
                    fileInfo, hduInfoList = self.parse.getInfo(infile, args.filetype)
                    if len(hduInfoList) > 0:
                        outfileInstcal = os.path.join(root, self.parse.getDestination(args.butler,
                                                                                      hduInfoList[0],
                                                                                      infile, "instcal"))
                        outfileDqmask = os.path.join(root, self.parse.getDestination(args.butler,
                                                                                     hduInfoList[0], infile,
                                                                                     "dqmask"))
                        outfileWtmap = os.path.join(root, self.parse.getDestination(args.butler,
                                                                                    hduInfoList[0], infile,
                                                                                    "wtmap"))

                        ingestedInstcal = self.ingest(fileInfo["instcal"], outfileInstcal,
                                                      mode=args.mode, dryrun=args.dryrun)
                        ingestedDqmask = self.ingest(fileInfo["dqmask"], outfileDqmask,
                                                     mode=args.mode, dryrun=args.dryrun)
                        ingestedWtmap = self.ingest(fileInfo["wtmap"], outfileWtmap,
                                                    mode=args.mode, dryrun=args.dryrun)

                        if not (ingestedInstcal or ingestedDqmask or ingestedWtmap):
                            continue

                    for info in hduInfoList:
                        self.register.addRow(registry, info, dryrun=args.dryrun, create=args.create)

        elif args.filetype == "raw":
            IngestTask.run(self, args)


class DecamParseTask(ParseTask):
    """Parse an image filename to get the required information to
    put the file in the correct location and populate the registry.
    """

    _translatorClass = DecamTranslator

    def __init__(self, *args, **kwargs):
        super(ParseTask, self).__init__(*args, **kwargs)

        self.expnumMapper = None

        # Note that these should be syncronized with the fields in
        # root.register.columns defined in config/ingest.py
        self.instcalPrefix = "instcal"
        self.dqmaskPrefix = "dqmask"
        self.wtmapPrefix = "wtmap"

    def _listdir(self, path, prefix):
        for file in os.listdir(path):
            fileName = os.path.join(path, file)
            md = readMetadata(fileName)
            fix_header(md, translator_class=self._translatorClass)
            if "EXPNUM" not in md:
                return
            expnum = md["EXPNUM"]
            if expnum not in self.expnumMapper:
                self.expnumMapper[expnum] = {self.instcalPrefix: None,
                                             self.wtmapPrefix: None,
                                             self.dqmaskPrefix: None}
            self.expnumMapper[expnum][prefix] = fileName

    def buildExpnumMapper(self, basepath):
        """Extract exposure numbers from filenames to set self.expnumMapper

        Parameters
        ----------
        basepath : `str`
            Location on disk of instcal, dqmask, and wtmap subdirectories.
        """
        self.expnumMapper = {}

        instcalPath = basepath
        dqmaskPath = re.sub(self.instcalPrefix, self.dqmaskPrefix, instcalPath)
        wtmapPath = re.sub(self.instcalPrefix, self.wtmapPrefix, instcalPath)
        if instcalPath == dqmaskPath:
            raise RuntimeError("instcal and mask directories are the same")
        if instcalPath == wtmapPath:
            raise RuntimeError("instcal and weight map directories are the same")

        if not os.path.isdir(dqmaskPath):
            raise OSError("Directory %s does not exist" % (dqmaskPath))
        if not os.path.isdir(wtmapPath):
            raise OSError("Directory %s does not exist" % (wtmapPath))

        # Traverse each directory and extract the expnums
        for path, prefix in zip((instcalPath, dqmaskPath, wtmapPath),
                                (self.instcalPrefix, self.dqmaskPrefix, self.wtmapPrefix)):
            self._listdir(path, prefix)

    def getInfo(self, filename, filetype="raw"):
        """Get metadata header info from multi-extension FITS decam image file.

        The science pixels, mask, and weight (inverse variance) are
        stored in separate files each with a unique name but with a
        common unique identifier EXPNUM in the FITS header.  We have
        to aggregate the 3 filenames for a given EXPNUM and return
        this information along with that returned by the base class.

        Parameters
        ----------
        filename : `str`
            Image file to retrieve info from.
        filetype : `str`
            One of "raw" or "instcal".

        Returns
        -------
        phuInfo : `dict`
            Primary header unit info.
        infoList : `list` of `dict`
            Info for the other HDUs.

        Notes
        -----
        For filetype="instcal", we expect a directory structure that looks
        like the following:

        .. code-block:: none

            dqmask/
            instcal/
            wtmap/

        The user creates the registry by running:

        .. code-block:: none

            ingestImagesDecam.py outputRepository --filetype=instcal --mode=link instcal/*fits
        """
        if filetype == "instcal":
            if self.expnumMapper is None:
                self.buildExpnumMapper(os.path.dirname(os.path.abspath(filename)))

            # Note that phuInfo will have
            #   'side': 'X', 'ccd': 0
            phuInfo, infoList = super(DecamParseTask, self).getInfo(filename)
            expnum = phuInfo["visit"]
            phuInfo[self.instcalPrefix] = self.expnumMapper[expnum][self.instcalPrefix]
            phuInfo[self.dqmaskPrefix] = self.expnumMapper[expnum][self.dqmaskPrefix]
            phuInfo[self.wtmapPrefix] = self.expnumMapper[expnum][self.wtmapPrefix]
            for info in infoList:
                expnum = info["visit"]
                info[self.instcalPrefix] = self.expnumMapper[expnum][self.instcalPrefix]
                info[self.dqmaskPrefix] = self.expnumMapper[expnum][self.dqmaskPrefix]
                info[self.wtmapPrefix] = self.expnumMapper[expnum][self.wtmapPrefix]

        elif filetype == "raw":
            phuInfo, infoList = super(DecamParseTask, self).getInfo(filename)
            for info in infoList:
                info[self.instcalPrefix] = ""
                info[self.dqmaskPrefix] = ""
                info[self.wtmapPrefix] = ""

        # Some data IDs can not be extracted from the zeroth extension
        # of the MEF. Add them so Butler does not try to find them
        # in the registry which may still yet to be created.
        for key in ("ccdnum", "hdu", "ccd", "calib_hdu"):
            if key not in phuInfo:
                phuInfo[key] = 0

        return phuInfo, infoList

    def getDestination(self, butler, info, filename, filetype="raw"):
        """Get destination for the file

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
        raw = butler.get("%s_filename"%(filetype), info)[0]
        # Ensure filename is devoid of cfitsio directions about HDUs
        c = raw.find("[")
        if c > 0:
            raw = raw[:c]
        return raw
