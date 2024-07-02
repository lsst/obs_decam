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

import lsst.utils
import lsst.utils.tests

from lsst.daf.butler import Butler


EXPOSURE = 229388
DETECTOR = 1


test_data_package = "testdata_decam"
try:
    test_data_directory = lsst.utils.getPackageDir(test_data_package)
except LookupError:
    test_data_directory = None


@unittest.skipIf(test_data_directory is None, "testdata_decam must be set up")
class WcsCardsTestCase(lsst.utils.tests.TestCase):
    """Test wcs keywords in the metadata"""

    @classmethod
    def setUpClass(cls):
        cls.repo = os.path.join(test_data_directory, 'repo')

    def test_raw_wcs(self):
        """Test wcs keywords are removed from the metadata of the raw
        Exposure.
        """
        butler = Butler(self.repo, instrument='DECam', collections='DECam/raw/all')

        md = butler.get('raw.metadata', exposure=EXPOSURE, detector=DETECTOR)
        self.assertFalse(md.exists('CTYPE1'))
        self.assertFalse(md.exists('CD1_2'))
        self.assertFalse(md.exists('CRPIX2'))
        self.assertFalse(md.exists('PV1_4'))
        self.assertFalse(md.exists('PV2_10'))


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
