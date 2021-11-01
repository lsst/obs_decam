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

import os
import warnings
import unittest

from lsst.daf.base import DateTime
import lsst.afw.image as afwImage
import lsst.utils.tests
from lsst.utils import getPackageDir

import lsst.daf.persistence as dafPersist
from lsst.afw.image import RotType
from lsst.geom import degrees, radians, arcseconds, SpherePoint


# Desired VisitInfo values for visit 229388, shared between test_getRaw.py and
# test_getInstcal.py

visit229388_info = {
    "dateAvg": DateTime("2013-09-01T06:06:00.876924000", DateTime.TAI),
    "exposureTime": 200.0,
    "darkTime": 201.15662,
    "era": 1.25232*radians,
    "boresightRaDec": SpherePoint(42.81995833, -0.00158305, degrees),
    "boresightAzAlt": SpherePoint(61.24, 90 - 50.46, degrees),
    "boresightAirmass": 1.57,
    "boresightRotAngle": 90*degrees,
    "rotType": RotType.SKY,
    "obs_longitude": -70.81489000000001*degrees,
    "obs_latitude": -30.16606*degrees,
    "obs_elevation": 2215.0,
    "weath_airTemperature": 11.9,
    "weath_airPressure": 77900.,
    "weath_humidity": 23.0}


class GetRawTestCase(lsst.utils.tests.TestCase):
    """Testing butler raw image retrieval"""

    def setUp(self):
        try:
            datadir = getPackageDir("testdata_decam")
        except LookupError:
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
        self.assertEqual(exp.getFilter().getCanonicalName(), self.filter)
        self.assertTrue(exp.hasWcs())

        # Metadata which should have been copied from zeroth extension.
        visitInfo = exp.getInfo().getVisitInfo()
        self.assertEqual(visitInfo.getDate(), visit229388_info['dateAvg'])
        self.assertEqual(visitInfo.getExposureTime(), visit229388_info['exposureTime'])
        self.assertEqual(visitInfo.getDarkTime(), visit229388_info['darkTime'])
        self.assertEqual(exp.info.id, int("%07d%02d" % (229388, 1)))
        self.assertAnglesAlmostEqual(visitInfo.getEra(), visit229388_info['era'],
                                     maxDiff=0.0001*radians)
        self.assertSpherePointsAlmostEqual(visitInfo.getBoresightRaDec(), visit229388_info['boresightRaDec'],
                                           maxSep=0.1*arcseconds)
        self.assertSpherePointsAlmostEqual(visitInfo.getBoresightAzAlt(), visit229388_info['boresightAzAlt'])
        self.assertAlmostEqual(visitInfo.getBoresightAirmass(), visit229388_info['boresightAirmass'])
        self.assertEqual(visitInfo.getBoresightRotAngle(), visit229388_info['boresightRotAngle'])
        self.assertEqual(visitInfo.getRotType(), visit229388_info['rotType'])
        observatory = visitInfo.getObservatory()
        self.assertAnglesAlmostEqual(observatory.getLongitude(), visit229388_info['obs_longitude'])
        self.assertAnglesAlmostEqual(observatory.getLatitude(), visit229388_info['obs_latitude'])
        self.assertAlmostEqual(observatory.getElevation(), visit229388_info['obs_elevation'])
        weather = visitInfo.getWeather()
        self.assertAlmostEqual(weather.getAirTemperature(), visit229388_info['weath_airTemperature'])
        self.assertAlmostEqual(weather.getAirPressure(), visit229388_info['weath_airPressure'])
        self.assertAlmostEqual(weather.getHumidity(), visit229388_info['weath_humidity'])

    def testRawMetadata(self):
        """Test retrieval of metadata"""
        md = self.butler.get("raw_md", self.dataId)
        print("EXPNUM(visit): %s" % md.getScalar('EXPNUM'))
        print("ccdnum: %s" % md.getScalar('CCDNUM'))
        self.assertEqual(md.getScalar('EXPNUM'), self.dataId["visit"])
        self.assertEqual(md.getScalar('CCDNUM'), self.dataId["ccdnum"])

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
        self.assertEqual(exp.getFilter().getCanonicalName(), self.filter)
        self.assertTrue(exp.hasWcs())

    def testFringe(self):
        """Test retrieval of fringe image"""
        exp = self.butler.get("fringe", self.dataId)
        print("dataId: %s" % self.dataId)
        print("detector id: %s" % exp.getDetector().getId())
        print("filter: %s" % self.filter)
        self.assertEqual(exp.getDetector().getId(), self.dataId["ccdnum"])
        self.assertEqual(exp.getFilter().getCanonicalName(), self.filter)

    def testDefect(self):
        """Test retrieval of defect list"""
        defectList = self.butler.get("defects", self.dataId)
        self.assertEqual(len(defectList), 395)
        for d in defectList:
            self.assertIsInstance(d, afwImage.DefectBase)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
