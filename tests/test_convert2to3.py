# This file is part of obs_decam.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit tests for DECam gen2 to gen3 conversion.
"""

import itertools
import os
import unittest

import lsst.utils.tests
from lsst.obs.base.gen2to3 import convertTests
import lsst.obs.decam

testDataPackage = "testdata_decam"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, f"{testDataPackage} not setup")
class DecamConvertGen2To3TestCase(convertTests.ConvertGen2To3TestCase,
                                  lsst.utils.tests.TestCase):

    instrumentClassName = "lsst.obs.decam.DarkEnergyCamera"

    def setUp(self):
        # NOTE: this test will produce a bunch of "Skipping ingestion for" warnings,
        # due to the bias/flat calibRegistry only having the same ccds as the
        # raws, even though the files themselves have more.
        self.gen2root = os.path.join(testDataDirectory, 'ingested')
        self.gen2calib = os.path.join(testDataDirectory, 'calibingested')
        self.config = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   "config", "convert2to3Config.py")
        self.kwargs = {}

        detectors = (5, 10, 56, 60)
        dates = ('2015-02-18', '2015-03-13')
        self.biasName = 'cpBias'
        self.biases = [{'detector': detector, 'instrument': 'DECam'}
                       for detector, date in itertools.product(detectors, dates)]
        self.flatName = 'cpFlat'
        self.flats = [{'detector': detector,
                       'instrument': 'DECam', 'physical_filter': 'g DECam SDSS c0001 4720.0 1520.0'}
                      for detector, date in itertools.product(detectors, dates)]
        self.refcats = ['gaia', 'panstarrs']
        super().setUp()


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
