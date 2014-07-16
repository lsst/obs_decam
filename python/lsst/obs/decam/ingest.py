#
# LSST Data Management System
# Copyright 2012 LSST Corporation.
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
import lsst.afw.image as afwImage
from lsst.pipe.tasks.ingest import ParseTask

def parseExtname(md):
    side, ccd = "X", 0
    if not md.exists("EXTNAME"):
        return side, ccd
    extname = md.get("EXTNAME").strip()
    if extname[0] in "NS":
        side = extname[0]
    ccd = int(extname[1:])
    return side, ccd

class DecamParseTask(ParseTask):
    def __init__(self, *args, **kwargs):
        super(ParseTask, self).__init__(*args, **kwargs)
        
        self.expnumMapper  = None

        # Note that these should be syncronized with the fields in
        # root.register.columns defined in config/ingest.py
        self.instcalPrefix = "instCal"
        self.dqmaskPrefix  = "dqmask"
        self.wtmapPrefix   = "wtmap"

    def _listdir(self, path, prefix):
        for file in os.listdir(path):
            fileName = os.path.join(path, file)
            md = afwImage.readMetadata(fileName)
            if not "EXPNUM" in md.names():
                return
            expnum = md.get("EXPNUM")
            if not expnum in self.expnumMapper.keys():
                self.expnumMapper[expnum] = {self.instcalPrefix: None,
                                             self.wtmapPrefix: None,
                                             self.dqmaskPrefix: None}
            self.expnumMapper[expnum][prefix] = fileName
            
    def buildExpnumMapper(self, basepath):
        self.expnumMapper = {}
        
        instcalPath = basepath
        dqmaskPath  = re.sub(self.instcalPrefix, self.dqmaskPrefix, instcalPath)
        wtmapPath   = re.sub(self.instcalPrefix, self.wtmapPrefix, instcalPath)
        if not os.path.isdir(dqmaskPath):
            raise OSError, "Directory %s does not exist" % (dqmaskPath)
        if not os.path.isdir(wtmapPath):
            raise OSError, "Directory %s does not exist" % (wtmapPath)

        # Traverse each directory and extract the expnums
        for path, prefix in zip((instcalPath, dqmaskPath, wtmapPath),
                                (self.instcalPrefix, self.dqmaskPrefix, self.wtmapPrefix)):
            self._listdir(path, prefix)
        
    def getInfo(self, filename):

        """ The science pixels, mask, and weight (inverse variance)
        are stored in separate files each with a unique name but with
        a common unique identifier EXPNUM in the FITS header.  We have
        to aggregate the 3 filenames for a given EXPNUM and return
        this information along with that returned by the base class.

        We expect a directory structure that looks like the following:

          dqmask/ instCal/ wtmap/

        The user creates the registry by running ingest.py on instCal/*.fits.
        """
        if self.expnumMapper is None:
            self.buildExpnumMapper(os.path.dirname(os.path.abspath(filename)))

        # Note that phuInfo will have
        #   'side': 'X', 'ccd': 0
        phuInfo, infoList = super(DecamParseTask, self).getInfo(filename)
        for idx, info in enumerate(infoList):
            expnum = info["visit"]
            info[self.instcalPrefix] = self.expnumMapper[expnum][self.instcalPrefix]
            info[self.dqmaskPrefix]  = self.expnumMapper[expnum][self.dqmaskPrefix]
            info[self.wtmapPrefix]   = self.expnumMapper[expnum][self.wtmapPrefix]

        return phuInfo, infoList
    
    def translate_side(self, md):
        side, ccd = parseExtname(md)
        return side

    def translate_ccd(self, md):
        side, ccd = parseExtname(md)
        return ccd

    @staticmethod
    def getExtensionName(md):
        return md.get('EXTNAME')

