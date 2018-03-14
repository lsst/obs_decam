#
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
#
from __future__ import absolute_import, division, print_function

import os
import warnings
import unittest
import lsst.utils.tests

from lsst.utils import getPackageDir
import lsst.pex.exceptions as pexExcept
import lsst.afw.geom as afwGeom
import lsst.daf.persistence as dafPersist
from lsst.obs.decam.decamCpIsr import DecamCpIsrTask

obsDecamDir = getPackageDir('obs_decam')
displayDiffs = False


def getObsDecamConfig(TaskClass):
    """Helper function to get a command-line task config customized by obs_decam.

    Borrowed from test_processCcd.py.
    """
    config = TaskClass.ConfigClass()
    filename = os.path.join(obsDecamDir, 'config', TaskClass._DefaultName + '.py')
    if os.path.exists(filename):
        config.load(filename)
    return config


class CrosstalkTestCase(lsst.utils.tests.TestCase):
    """A set of tests for DECam crosstalk correction.
    """

    def setUp(self):
        try:
            datadir = getPackageDir('testdata_decam')
        except pexExcept.NotFoundError:
            message = "testdata_decam not setup. Skipping."
            warnings.warn(message)
            raise unittest.SkipTest(message)

        self.repoPath = os.path.join(datadir, 'rawData')
        self.calibPath = os.path.join(datadir, 'rawData/cpCalib')
        self.butler = dafPersist.Butler(
            inputs={'root': self.repoPath, 'mapperArgs': {'calibRoot': self.calibPath}},
            outputs=None
        )
        self.dataId = {'visit': 229388, 'ccdnum': 1}
        # Location of pixels where crosstalk is appreciable in the test image
        self.xtalkX = 1810
        self.xtalkY = 2970
        self.xtalkRad = 100

    def tearDown(self):
        del self.butler

    def runIsr(self, doCrosstalk):
        """Run DecamCpIsrTask with or without crosstalk correction
        """
        dataRef = self.butler.dataRef('raw', dataId=self.dataId)
        rawExposure = self.butler.get('raw', dataId=self.dataId)
        camera = dataRef.get('camera')
        config = getObsDecamConfig(DecamCpIsrTask)
        config.doCrosstalk = doCrosstalk

        # Special DECam ISR config settings from config/processCcdCpIsr.py
        config.doDark = False
        config.doAddDistortionModel = False
        config.fringe.filters = ['z', 'y']
        config.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                           'TRIMSECA', 'TRIMSECB',
                                           'BIASSECA', 'BIASSECB',
                                           'PRESECA', 'PRESECB',
                                           'POSTSECA', 'POSTSECB']

        decamCpIsrTask = DecamCpIsrTask(config=config)
        isrData = decamCpIsrTask.readIsrData(dataRef, rawExposure)
        isrResult = decamCpIsrTask.run(
            rawExposure,
            bias=isrData.bias,
            linearizer=isrData.linearizer,
            flat=isrData.flat,
            defects=isrData.defects,
            fringes=isrData.fringes,
            bfKernel=isrData.bfKernel,
            camera=camera,
            otherDataRef=dataRef,
        )
        return isrResult

    def testCrosstalk(self):
        """Compare DECam postISR images with and without crosstalk removal.

        A region with known crosstalk from the neighbor amp is inspected to
        verify the crosstalk is removed, and we also test to see that the
        image statistics are altered as expected by crosstalk removal.
        This test requires running DecamCpIsrTask twice.
        """
        # Run ISR with and without crosstalk correction
        expWithoutCrosstalkCorr = self.runIsr(doCrosstalk=False).exposure
        expWithCrosstalkCorr = self.runIsr(doCrosstalk=True).exposure
        image1 = expWithoutCrosstalkCorr.getMaskedImage().getImage()
        image2 = expWithCrosstalkCorr.getMaskedImage().getImage()

        # Check that the image data is different with crosstalk on vs. off
        assert (image1.getArray() != image2.getArray()).all()

        # Work with a small image chunk only
        pmin = afwGeom.Point2I(self.xtalkX - self.xtalkRad, self.xtalkY - self.xtalkRad)
        pmax = afwGeom.Point2I(self.xtalkX + self.xtalkRad, self.xtalkY + self.xtalkRad)
        box = afwGeom.Box2I(pmin, pmax)
        chunk1 = image1.Factory(image1, box)
        chunk2 = image2.Factory(image2, box)
        chunkDiff = chunk1.clone()
        chunkDiff -= chunk2

        # Check that the difference of the two image chunks is nonzero
        all_zeros = not chunkDiff.getArray().any()
        self.assertFalse(all_zeros)

        # Check that the standard deviation with crosstalk signatures still
        # present is larger than when it has been removed
        self.assertGreater(chunk1.getArray().std(), chunk2.getArray().std())

        # More specific tests for the exact image statistics expected
        self.assertAlmostEqual(chunk1.getArray().mean(), 3731.2451, places=3)
        self.assertAlmostEqual(chunk2.getArray().mean(), 3727.834, places=3)
        self.assertAlmostEqual(chunkDiff.getArray().mean(), 3.4109073, places=3)
        self.assertAlmostEqual(chunk1.getArray().std(), 33.811527, places=5)
        self.assertAlmostEqual(chunk2.getArray().std(), 33.319572, places=5)
        self.assertAlmostEqual(chunkDiff.getArray().std(), 5.8550658, places=5)

        # Option to display the portions of the image with/without crosstalk
        if displayDiffs:
            import lsst.afw.display.ds9 as ds9
            ds9.mtv(chunk1, frame=1)
            ds9.mtv(chunk2, frame=2)
            ds9.mtv(chunkDiff, frame=3)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
