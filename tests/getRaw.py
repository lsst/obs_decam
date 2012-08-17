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
        self.size = (2048, 4096)
        assert self.datadir, "testdata_sst is not setup"

    def testRaw(self):
        """Test retrieval of raw image"""

        year = 2012
        doy = 89
        frac = 132221

        butler = getButler(self.datadir)
        for ccd in range(12):
            dataId = {'year': year,
                      'doy': doy,
                      'frac': frac,
                      'ccd': ccd,
                      }
            raw = butler.get("raw", dataId)
            x,y = ccd % 6, ccd // 6

            print "dataId: ", dataId
            print "width: ", raw.getWidth()
            print "height: ", raw.getHeight()
            print "detector name: ", raw.getDetector().getId().getName()

            self.assertEqual(raw.getWidth(), self.size[0]) # untrimmed
            self.assertEqual(raw.getHeight(), self.size[1]) # untrimmed

            self.assertEqual(raw.getFilter().getFilterProperty().getName(), "OPEN") 
            self.assertEqual(raw.getDetector().getId().getName(), "%d,%d" % (x,y))

            if display:
                ccd = cameraGeom.cast_Ccd(raw.getDetector())
                for amp in ccd:
                    amp = cameraGeom.cast_Amp(amp)
                    print ccd.getId(), amp.getId(), amp.getDataSec().toString(), \
                          amp.getBiasSec().toString(), amp.getElectronicParams().getGain()
                cameraGeomUtils.showCcd(ccd, ccdImage=raw, frame=frame)
                frame += 1


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
