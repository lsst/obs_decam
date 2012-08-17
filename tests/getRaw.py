#!/usr/bin/env python

import os

import unittest
import lsst.utils.tests as utilsTests

from lsst.pex.policy import Policy
import lsst.daf.persistence as dafPersist
from lsst.obs.sst import SstMapper

import lsst.afw.display.ds9 as ds9
import lsst.afw.display.utils as displayUtils

import lsst.afw.cameraGeom as cameraGeom
import lsst.afw.cameraGeom.utils as cameraGeomUtils
try:
    type(display)
except NameError:
    display = False


def getButler(datadir):
    bf = dafPersist.ButlerFactory(mapper=SstMapper(root=os.path.join(datadir, "DATA"),
                                                   calibRoot=os.path.join(datadir, "CALIB")))
    return bf.create()


class GetRawTestCase(unittest.TestCase):
    """Testing butler raw image retrieval"""

    def setUp(self):
        self.datadir = os.getenv("TESTDATA_SST_DIR")
        assert self.datadir, "testdata_sst is not setup"
        self.butler = getButler(self.datadir)
        self.size = (2048, 4096)
        self.dataId = {'year': 2012,
                       'doy': 89,
                       'frac': 132221,
                       }
    def tearDown(self):
        del self.butler

    def assertExposure(self, exp, ccd):
        print "dataId: ", self.dataId
        print "ccd: ", ccd
        print "width: ", exp.getWidth()
        print "height: ", exp.getHeight()
        print "detector name: ", exp.getDetector().getId().getName()
        
        self.assertEqual(exp.getWidth(), self.size[0])
        self.assertEqual(exp.getHeight(), self.size[1])
        self.assertEqual(exp.getFilter().getFilterProperty().getName(), "OPEN") 
        self.assertEqual(exp.getDetector().getId().getName(), "%d,%d" % (ccd % 6, ccd // 6))

    def testRaw(self):
        """Test retrieval of raw image"""
        for ccd in range(12):
            raw = self.butler.get("raw", self.dataId, ccd=ccd)

            self.assertExposure(raw, ccd)

            if display:
                ccd = cameraGeom.cast_Ccd(raw.getDetector())
                for amp in ccd:
                    amp = cameraGeom.cast_Amp(amp)
                    print ccd.getId(), amp.getId(), amp.getDataSec().toString(), \
                          amp.getBiasSec().toString(), amp.getElectronicParams().getGain()
                cameraGeomUtils.showCcd(ccd, ccdImage=raw, frame=frame)
                frame += 1

    def testFlat(self):
        """Test retrieval of flat image"""
        for ccd in range(12):
            flat = self.butler.get("flat", self.dataId, ccd=ccd)

            self.assertExposure(flat, ccd)

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
