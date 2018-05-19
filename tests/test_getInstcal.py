#
# LSST Data Management System
# Copyright 2016 LSST Corporation.
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

import math
import os
import warnings
import unittest

import lsst.utils.tests
from lsst.utils import getPackageDir

import lsst.pex.exceptions as pexExcept
import lsst.daf.persistence as dafPersist

from test_getRaw import visit229388_info


class GetInstcalTestCase(lsst.utils.tests.TestCase):

    def setUp(self):
        try:
            datadir = getPackageDir("testdata_decam")
        except pexExcept.NotFoundError:
            message = "testdata_decam not setup. Skipping."
            warnings.warn(message)
            raise unittest.SkipTest(message)

        self.repoPath = os.path.join(datadir, "cpData")
        self.butler = dafPersist.Butler(root=self.repoPath)
        self.size = (2046, 4094)
        self.dataId = {'visit': 229388, 'ccdnum': 1}
        self.filter = "z"

    def tearDown(self):
        del self.butler

    def testInstcal(self):
        """Test retrieval of community pipeline-processed image"""
        exp = self.butler.get("instcal", self.dataId, immediate=True)

        self.assertEqual(exp.getWidth(), self.size[0])
        self.assertEqual(exp.getHeight(), self.size[1])
        self.assertEqual(exp.getDetector().getId(), self.dataId["ccdnum"])
        self.assertEqual(exp.getFilter().getFilterProperty().getName(), self.filter)
        self.assertTrue(exp.hasWcs())

        visitInfo = exp.getInfo().getVisitInfo()
        self.assertEqual(visitInfo.getDate(), visit229388_info['dateAvg'])
        self.assertEqual(visitInfo.getExposureTime(), visit229388_info['exposureTime'])
        self.assertEqual(visitInfo.getDarkTime(), visit229388_info['darkTime'])
        visitInfo = exp.getInfo().getVisitInfo()
        self.assertEqual(visitInfo.getDate(), visit229388_info['dateAvg'])
        self.assertAnglesAlmostEqual(visitInfo.getEra(), visit229388_info['era'])
        self.assertSpherePointsAlmostEqual(visitInfo.getBoresightRaDec(), visit229388_info['boresightRaDec'])
        self.assertSpherePointsAlmostEqual(visitInfo.getBoresightAzAlt(), visit229388_info['boresightAzAlt'])
        self.assertAlmostEqual(visitInfo.getBoresightAirmass(), visit229388_info['boresightAirmass'])
        self.assertTrue(math.isnan(visitInfo.getBoresightRotAngle().asDegrees()))
        self.assertEqual(visitInfo.getRotType(), visit229388_info['rotType'])
        observatory = visitInfo.getObservatory()
        self.assertAnglesAlmostEqual(observatory.getLongitude(), visit229388_info['obs_longitude'])
        self.assertAnglesAlmostEqual(observatory.getLatitude(), visit229388_info['obs_latitude'])
        self.assertAlmostEqual(observatory.getElevation(), visit229388_info['obs_elevation'])
        weather = visitInfo.getWeather()
        self.assertAlmostEqual(weather.getAirTemperature(), visit229388_info['weath_airTemperature'])
        self.assertAlmostEqual(weather.getAirPressure(), visit229388_info['weath_airPressure'])
        self.assertAlmostEqual(weather.getHumidity(), visit229388_info['weath_humidity'])

        # Metadata should not contain WCS or TPV headers.
        # This is not an exhaustive list.
        wcs_keywords = ("PV1_1", "PV2_1", "CRPIX1", "CD2_1", "CRVAL2", "LTV1")
        for keyword in wcs_keywords:
            self.assertNotIn(keyword, exp.getMetadata().paramNames())

    def testCcdName(self):
        """Verify that we get the proper CCD for a specified ccdnum."""
        dataId = {'visit': 229388, 'ccdnum': 62}
        exp = self.butler.get("instcal", dataId, immediate=True)
        md = exp.getMetadata()
        self.assertEqual(md.get("DETPOS"), "N31")


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
