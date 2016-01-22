#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2016 AURA/LSST.
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <https://www.lsstcorp.org/LegalNotices/>.
#

import os
import unittest
import warnings

from lsst.utils import getPackageDir
import lsst.utils.tests as utilsTests

import lsst.daf.persistence as dafPersist
import lsst.pex.exceptions as pexExcept


class WcsCardsTestCase(unittest.TestCase):
    """Testing butler exposure id retrieval"""
    def setUp(self):
        try:
            datadir = getPackageDir("testdata_decam")
        except pexExcept.NotFoundError:
            message = "testdata_decam not setup. Skipping."
            warnings.warn(message)
            raise unittest.SkipTest(message)
        self.butler = dafPersist.Butler(root=os.path.join(datadir, "rawData"))
        self.dataId = {'visit': 229388, 'ccdnum': 1}

    def tearDown(self):
        del self.butler

    def testRawWcs(self):
        """Test wcs keywords are removed from the metadata of the raw Exposure"""
        exp = self.butler.get("raw", self.dataId, immediate=True)
        self.assertFalse(exp.getMetadata().exists('CTYPE1'))
        self.assertFalse(exp.getMetadata().exists('CD1_2'))
        self.assertFalse(exp.getMetadata().exists('CRPIX2'))
        self.assertFalse(exp.getMetadata().exists('LTV1'))
        self.assertFalse(exp.getMetadata().exists('PV1_4'))
        self.assertFalse(exp.getMetadata().exists('PV2_10'))


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def suite():
    """Returns a suite containing all the test cases in this module."""

    utilsTests.init()

    suites = []
    suites += unittest.makeSuite(WcsCardsTestCase)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)

def run(shouldExit=False):
    """Run the tests"""
    utilsTests.run(suite(), shouldExit)

if __name__ == "__main__":
    run(True)
