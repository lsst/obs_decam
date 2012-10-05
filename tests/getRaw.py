#!/usr/bin/env python

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

import unittest
import lsst.utils.tests as utilsTests

from lsst.pex.policy import Policy
import lsst.daf.persistence as dafPersist
from lsst.obs.decam import DecamMapper

import lsst.afw.display.ds9 as ds9
import lsst.afw.display.utils as displayUtils

import lsst.afw.cameraGeom as cameraGeom
import lsst.afw.cameraGeom.utils as cameraGeomUtils
try:
    type(display)
except NameError:
    display = False


def getButler(datadir):
    bf = dafPersist.ButlerFactory(mapper=DecamMapper(root=os.path.join(datadir, "DATA"),
                                                     calibRoot=os.path.join(datadir, "CALIB")))
    return bf.create()


class GetRawTestCase(unittest.TestCase):
    """Testing butler raw image retrieval"""

    def setUp(self):
        self.datadir = os.getenv("TESTDATA_DECAM_DIR")
        assert self.datadir, "testdata_decam is not setup"
        self.butler = getButler(self.datadir)
        self.size = (2160, 4146)
        self.dataId = {'visit': 135635}
        self.filter = "r"

    def tearDown(self):
        del self.butler

    def assertExposure(self, exp, side, ccd):
        print "dataId: ", self.dataId
        print "ccd: ", ccd
        print "width: ", exp.getWidth()
        print "height: ", exp.getHeight()
        print "detector name: ", exp.getDetector().getId().getName()
        
        self.assertEqual(exp.getWidth(), self.size[0])
        self.assertEqual(exp.getHeight(), self.size[1])
        self.assertEqual(exp.getFilter().getFilterProperty().getName(), self.filter)
        self.assertEqual(exp.getDetector().getId().getName(), "%s%d" % (side.upper(), ccd))

    def testRaw(self):
        """Test retrieval of raw image"""
        frame = 0
        if display:
            cameraGeomUtils.showCamera(self.butler.mapper.camera, frame=frame)

        for side in ("N", "S"):
            for ccd in range(1, 32, 1):
                raw = self.butler.get("raw", self.dataId, side=side, ccd=ccd)

                self.assertExposure(raw, side, ccd)

                if display:
                    frame += 1
                    ccd = cameraGeom.cast_Ccd(raw.getDetector())
                    for amp in ccd:
                        amp = cameraGeom.cast_Amp(amp)
                        print ccd.getId(), amp.getId(), amp.getDataSec().toString(), \
                              amp.getBiasSec().toString(), amp.getElectronicParams().getGain()
                    cameraGeomUtils.showCcd(ccd, ccdImage=raw, frame=frame)

#    def testFlat(self):
#        """Test retrieval of flat image"""
#        for ccd in range(12):
#            flat = self.butler.get("flat", self.dataId, ccd=ccd)
#
#            self.assertExposure(flat, ccd)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def suite():
    """Returns a suite containing all the test cases in this module."""

    utilsTests.init()

    suites = []
    suites += unittest.makeSuite(GetRawTestCase)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)

def run(shouldExit = False):
    """Run the tests"""
    utilsTests.run(suite(), shouldExit)

if __name__ == "__main__":
    run(True)
