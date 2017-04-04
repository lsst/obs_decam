#
# LSST Data Management System
# Copyright 2012, 2015 LSST Corporation.
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
from __future__ import absolute_import, division, print_function

import math
import os
import warnings
import unittest

from lsst.daf.base import DateTime
import lsst.afw.image as afwImage
import lsst.utils.tests
from lsst.utils import getPackageDir

import lsst.pex.exceptions as pexExcept
import lsst.daf.persistence as dafPersist
from lsst.obs.base import MakeRawVisitInfo
from lsst.afw.image import RotType
from lsst.afw.coord import IcrsCoord, Coord
from lsst.afw.geom import degrees


# Desired VisitInfo values for visit 229388, shared between testGetRaw.py and
# testGetInstcal.py

boresightRaDec = IcrsCoord('02:51:16.790', '-00:00:05.699')
# NOTE: if we deal with DM-8053 and implement UT1, ERA will not come from HA, so this will change.
HA = -42.505291666666665*degrees
era = HA + boresightRaDec[0] - 70.81489000000001*degrees
visit229388_info = {
    "dateAvg": DateTime("2013-09-01T06:05:10.753848", DateTime.TAI),
    "exposureTime": 200.0,
    "darkTime": 201.15662,
    "era": era,
    "boresightRaDec": boresightRaDec,
    "boresightAzAlt": Coord(61.24*degrees, (90-50.46)*degrees),
    "boresightAirmass": 1.57,
    "boresightRotAngle": float("nan")*degrees,
    "rotType": RotType.UNKNOWN,
    "obs_longitude": 70.81489000000001*degrees,
    "obs_latitude": -30.16606*degrees,
    "obs_elevation": 2215.0,
    "weath_airTemperature": 11.9,
    "weath_airPressure": MakeRawVisitInfo.pascalFromMmHg(779.0),
    "weath_humidity": 23.0}


class GetRawTestCase(lsst.utils.tests.TestCase):
    """Testing butler raw image retrieval"""

    def setUp(self):
        try:
            datadir = getPackageDir("testdata_decam")
        except pexExcept.NotFoundError:
            message = "testdata_decam not setup. Skipping."
            warnings.warn(message)
            raise unittest.SkipTest(message)

        self.repoPath = os.path.join(datadir, "rawData")
        calibPath = os.path.join(datadir, "rawData/cpCalib")
        self.butler = dafPersist.Butler(root=self.repoPath, calibRoot=calibPath)
        self.size = (2160, 4146)
        self.dataId = {'visit': 229388, 'ccdnum': 1}
        self.filter = "z"

    def tearDown(self):
        del self.butler

    def testPackageName(self):
        name = dafPersist.Butler.getMapperClass(root=self.repoPath).packageName
        self.assertEqual(name, "obs_decam")

    def testRaw(self):
        """Test retrieval of raw image"""
        exp = self.butler.get("raw", self.dataId)

        print("dataId: %s" % self.dataId)
        print("width: %s" % exp.getWidth())
        print("height: %s" % exp.getHeight())
        print("detector id: %s" % exp.getDetector().getId())

        self.assertEqual(exp.getWidth(), self.size[0])
        self.assertEqual(exp.getHeight(), self.size[1])
        self.assertEqual(exp.getDetector().getId(), self.dataId["ccdnum"])
        self.assertEqual(exp.getFilter().getFilterProperty().getName(), self.filter)
        self.assertTrue(exp.hasWcs())

        # Metadata which should have been copied from zeroth extension.
        visitInfo = exp.getInfo().getVisitInfo()
        self.assertEqual(visitInfo.getDate(), visit229388_info['dateAvg'])
        self.assertEqual(visitInfo.getExposureTime(), visit229388_info['exposureTime'])
        self.assertEqual(visitInfo.getDarkTime(), visit229388_info['darkTime'])
        visitInfo = exp.getInfo().getVisitInfo()
        self.assertEqual(visitInfo.getDate(), visit229388_info['dateAvg'])
        self.assertAnglesNearlyEqual(visitInfo.getEra(), visit229388_info['era'])
        self.assertCoordsNearlyEqual(visitInfo.getBoresightRaDec(), visit229388_info['boresightRaDec'])
        self.assertCoordsNearlyEqual(visitInfo.getBoresightAzAlt(), visit229388_info['boresightAzAlt'])
        self.assertAlmostEqual(visitInfo.getBoresightAirmass(), visit229388_info['boresightAirmass'])
        self.assertTrue(math.isnan(visitInfo.getBoresightRotAngle().asDegrees()))
        self.assertEqual(visitInfo.getRotType(), visit229388_info['rotType'])
        observatory = visitInfo.getObservatory()
        self.assertAnglesNearlyEqual(observatory.getLongitude(), visit229388_info['obs_longitude'])
        self.assertAnglesNearlyEqual(observatory.getLatitude(), visit229388_info['obs_latitude'])
        self.assertAlmostEqual(observatory.getElevation(), visit229388_info['obs_elevation'])
        weather = visitInfo.getWeather()
        self.assertAlmostEqual(weather.getAirTemperature(), visit229388_info['weath_airTemperature'])
        self.assertAlmostEqual(weather.getAirPressure(), visit229388_info['weath_airPressure'])
        self.assertAlmostEqual(weather.getHumidity(), visit229388_info['weath_humidity'])

        # Example of metadata which should *not* have been copied from zeroth extension.
        self.assertNotIn("PROPOSER", exp.getMetadata().paramNames())

    def testRawMetadata(self):
        """Test retrieval of metadata"""
        md = self.butler.get("raw_md", self.dataId)
        print("EXPNUM(visit): %s" % md.get('EXPNUM'))
        print("ccdnum: %s" % md.get('CCDNUM'))
        self.assertEqual(md.get('EXPNUM'), self.dataId["visit"])
        self.assertEqual(md.get('CCDNUM'), self.dataId["ccdnum"])

    def testBias(self):
        """Test retrieval of bias image"""
        exp = self.butler.get("cpBias", self.dataId)
        print("dataId: %s" % self.dataId)
        print("detector id: %s" % exp.getDetector().getId())
        self.assertEqual(exp.getDetector().getId(), self.dataId["ccdnum"])
        self.assertTrue(exp.hasWcs())

    def testFlat(self):
        """Test retrieval of flat image"""
        exp = self.butler.get("cpFlat", self.dataId)
        print("dataId: %s" % self.dataId)
        print("detector id: %s" % exp.getDetector().getId())
        print("filter: %s" % self.filter)
        self.assertEqual(exp.getDetector().getId(), self.dataId["ccdnum"])
        self.assertEqual(exp.getFilter().getFilterProperty().getName(), self.filter)
        self.assertTrue(exp.hasWcs())

    def testFringe(self):
        """Test retrieval of fringe image"""
        exp = self.butler.get("fringe", self.dataId)
        print("dataId: %s" % self.dataId)
        print("detector id: %s" % exp.getDetector().getId())
        print("filter: %s" % self.filter)
        self.assertEqual(exp.getDetector().getId(), self.dataId["ccdnum"])
        self.assertEqual(exp.getFilter().getFilterProperty().getName(), self.filter)

    def testDefect(self):
        """Test retrieval of defect list"""
        defectList = self.butler.get("defects", self.dataId)
        self.assertEqual(len(defectList), 9)
        for d in defectList:
            self.assertIsInstance(d, afwImage.DefectBase)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
