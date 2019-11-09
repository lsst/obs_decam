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

"""Tests of the DarkEnergyCamera instrument class.
"""

import unittest

import lsst.utils.tests
from lsst.obs.base.instrument_tests import InstrumentTests, InstrumentTestData
import lsst.obs.decam


class TestDarkEnergyCamera(InstrumentTests, lsst.utils.tests.TestCase):
    def setUp(self):
        physical_filters = {"VR DECam c0007 6300.0 2600.0",
                            "r DECam SDSS c0002 6415.0 1480.0",
                            "g DECam SDSS c0001 4720.0 1520.0",
                            "N964 DECam c0008 9645.0 94.0",
                            "Y DECam c0005 10095.0 1130.0",
                            "z DECam SDSS c0004 9260.0 1520.0",
                            "i DECam SDSS c0003 7835.0 1470.0",
                            "u DECam c0006 3500.0 1000.0",
                            "solid"}
        self.data = InstrumentTestData(name="DECam",
                                       nDetectors=62,
                                       firstDetectorName="S29",
                                       physical_filters=physical_filters)

        self.instrument = lsst.obs.decam.DarkEnergyCamera()


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == '__main__':
    lsst.utils.tests.init()
    unittest.main()
