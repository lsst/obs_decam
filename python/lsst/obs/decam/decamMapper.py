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
import pwd

import lsst.daf.base as dafBase
import lsst.afw.geom as afwGeom
import lsst.afw.coord as afwCoord
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils

from lsst.daf.butlerUtils import CameraMapper, exposureFromImage
import lsst.pex.policy as pexPolicy

class DecamInstcalMapper(CameraMapper):
    def __init__(self, inputPolicy=None, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile("obs_decam", "DecamMapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)

        super(DecamInstcalMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)

        afwImageUtils.defineFilter('u', lambdaEff=350)
        afwImageUtils.defineFilter('g', lambdaEff=450)
        afwImageUtils.defineFilter('r', lambdaEff=600)
        afwImageUtils.defineFilter('i', lambdaEff=750)
        afwImageUtils.defineFilter('z', lambdaEff=900)
        afwImageUtils.defineFilter('y', lambdaEff=1000, alias='Y')

    def _extractDetectorName(self, dataId):
        ccd = dataId['ccd']
        side = dataId['side']
        return "%s%d" % (side, ccd)

    def _defectLookup(self, dataId, ccdSerial):
        """Find the defects for a given CCD.
        @param dataId (dict) Dataset identifier
        @param ccdSerial (string) CCD serial number
        @return (string) path to the defects file or None if not available
        """
        return None 

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCcdExposureId(dataId)
    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 32 # not really, but this leaves plenty of space for sources
    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        visit = dataId['visit']
        ccd = dataId['ccd']
        side = dataId['side']
        return "%07d0%d%d" % (visit, 1 if side=="N" else 0, ccd)



    def bypass_raw(self, datasetType, pythonType, butlerLocation, dataId):
        print "CAW"
        
    def std_raw(self, image, dataId):
        """Fix missing header keywords"""

        md = image.getMetadata()
        md.add('CRVAL2', 0.0)
        if md.exists("BACKMEAN") and md.exists("ARAWGAIN"):
           backmean = md.get("BACKMEAN")
           gain = md.get("ARAWGAIN")
        else:
           backmean = 0.0
           gain = 1.0
        filterName = md.get("FILTER")[0]
        if filterName == "Y":
            filterName = "z"

        # Not until the camera part gets worked out
        #return super(DecamMapper, self).std_raw(image, dataId)

        # we have to deal with the variance ourselves, at least for the test data I got # ACB
        exp = exposureFromImage(image)
        mi  = exp.getMaskedImage()
        var = mi.getVariance().Factory(mi.getImage())
        var += backmean
        var /= gain
        mi2 = mi.Factory(mi.getImage(), mi.getMask(), var)
        exp2 = exp.Factory(mi2, exp.getWcs())

        # hacking around filter issues
        exp2.setFilter(afwImage.Filter(filterName))
        
        return exp2
