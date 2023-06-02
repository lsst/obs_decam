#
# LSST Data Management System
# Copyright 2022 AURA/LSST.
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
import unittest
import os
import tempfile
import pytest
import shutil

import lsst.utils
import lsst.utils.tests
import lsst.daf.butler
import lsst.obs.decam
import lsst.afw.image
import lsst.geom as geom

from lsst.pipe.base import Pipeline
from lsst.ctrl.mpexec import SimplePipelineExecutor

from lsst.daf.butler.cli.cliLog import CliLog


ROOT = os.path.abspath(os.path.dirname(__file__))

EXPOSURE = 229388
DETECTOR = 1


test_data_package = "testdata_decam"
try:
    test_data_directory = lsst.utils.getPackageDir(test_data_package)
except LookupError:
    test_data_directory = None


def _run_simple_isr_pipeline(repo, output_collection, do_crosstalk=False):
    """Run the simple ISR pipeline.

    Parameters
    ----------
    repo : `str`
        Location of test repo.
    output_collection : `str`
        Name of output collection.
    do_crosstalk : `bool`, optional
        Do crosstalk correction?

    Returns
    -------
    n_quanta : `int`
        Number of quanta successfully run.
    """
    butler = SimplePipelineExecutor.prep_butler(
        repo,
        inputs=['DECam/raw/all', 'DECam/calib'],
        output=output_collection
    )
    pipe_str = """description: Run test DECam ISR
instrument: lsst.obs.decam.DarkEnergyCamera
tasks:
  isr: lsst.ip.isr.IsrTask
"""
    pipeline = Pipeline.fromString(pipe_str)
    pipeline.addConfigFile('isr', os.path.join(ROOT, 'config', 'isr.py'))
    pipeline.addConfigOverride('isr', 'doCrosstalk', do_crosstalk)

    executor = SimplePipelineExecutor.from_pipeline(
        pipeline,
        where=f"exposure={EXPOSURE} and detector={DETECTOR}",
        root=repo,
        butler=butler
    )

    quanta = executor.run(register_dataset_types=True)
    return len(quanta)


@unittest.skipIf(test_data_directory is None, "testdata_decam must be set up")
class DecamIsrTestCase(lsst.utils.tests.TestCase):
    """DECam ISR Tests."""
    @classmethod
    def _import_repository(cls, export_path, export_file):
        """Import a test repository into self.test_dir

        Parameters
        ----------
        export_path : `str`
            Path to location of repository.
        export_file : `str`
            Filename of export data.
        """
        cls.repo = os.path.join(cls.test_dir, 'testrepo')

        # Make the repo and retrieve a writeable Butler
        _ = lsst.daf.butler.Butler.makeRepo(cls.repo)
        butler = lsst.daf.butler.Butler(cls.repo, writeable=True)
        # Register the instrument
        instr_instance = lsst.obs.decam.DarkEnergyCamera()
        instr_instance.register(butler.registry)
        # Import the export_file
        butler.import_(directory=export_path, filename=export_file, transfer='symlink')

    @classmethod
    def setUpClass(cls):
        CliLog.initLog(longlog=False)

        cls.test_dir = tempfile.mkdtemp(dir=ROOT, prefix="TestObsDecam-")

        cls._import_repository(
            os.path.join(test_data_directory, 'repo'),
            os.path.join(test_data_directory, 'repo', 'exports.yaml')
        )

        cls.basic_collection = 'isr_basic'
        _run_simple_isr_pipeline(cls.repo, cls.basic_collection)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir, True)

    def test_isr_basic(self):
        """Test basic ISR."""
        butler = lsst.daf.butler.Butler(self.repo, instrument='DECam', collections=self.basic_collection)

        exp = butler.get('postISRCCD', exposure=EXPOSURE, detector=DETECTOR)
        self.assertIsInstance(exp, lsst.afw.image.ExposureF)

        self.assertEqual(exp.width, 2048)
        self.assertEqual(exp.height, 4096)

    @pytest.mark.xfail
    def test_wcs_basic(self):
        """Test WCS after basic ISR.

        This test (in gen2) had previously been skipped but would have failed.
        """
        return
        butler = lsst.daf.butler.Butler(self.repo, instrument='DECam', collections=self.basic_collection)

        wcs_raw = butler.get('raw.wcs', exposure=EXPOSURE, detector=DETECTOR)
        exp_post = butler.get('postISRCCD', exposure=EXPOSURE, detector=DETECTOR)
        wcs_post = exp_post.wcs

        # Shift WCS for trimming the prescan and overscan region
        # detector 1 is S29, with overscan in the bottom
        wcs_raw = wcs_raw.copyAtShiftedPixelOrigin(geom.Extent2D(-56, -50))
        self.assertWcsAlmostEqualOverBBox(wcs_raw, wcs_post, exp_post.getBBox())

    def test_isr_crosstalk(self):
        """Test ISR with intra-detector crosstalk."""
        crosstalk_collection = 'isr_crosstalk'
        _run_simple_isr_pipeline(self.repo, crosstalk_collection, do_crosstalk=True)

        butler = lsst.daf.butler.Butler(self.repo, instrument='DECam')

        isr_config = butler.get(
            'isr_config',
            exposure=EXPOSURE,
            detector=DETECTOR,
            collections=crosstalk_collection
        )
        self.assertTrue(isr_config.doCrosstalk)

        exp_basic = butler.get(
            'postISRCCD',
            exposure=EXPOSURE,
            detector=DETECTOR,
            collections=self.basic_collection
        )
        exp_crosstalk = butler.get(
            'postISRCCD',
            exposure=EXPOSURE,
            detector=DETECTOR,
            collections=crosstalk_collection
        )
        image1 = exp_basic.image
        image2 = exp_crosstalk.image

        # Location of pixels where crosstalk is appreciable in the test image
        xtalk_x = 1810
        xtalk_y = 2970
        xtalk_rad = 100

        # Work with a small image chunk only
        pmin = geom.Point2I(xtalk_x - xtalk_rad, xtalk_y - xtalk_rad)
        pmax = geom.Point2I(xtalk_x + xtalk_rad, xtalk_y + xtalk_rad)
        box = geom.Box2I(pmin, pmax)
        chunk1 = image1.Factory(image1, box)
        chunk2 = image2.Factory(image2, box)
        chunk_diff = chunk1.clone()
        chunk_diff -= chunk2

        # Check that the difference of the two image chunks is nonzero
        # (the non-crosstalk-corrected and crosstalk-corrected images should differ)
        all_zeros = not chunk_diff.getArray().any()
        self.assertFalse(all_zeros)

        # Check that the standard deviation with crosstalk signatures still
        # present is larger than when it has been removed
        self.assertGreater(chunk1.array.std(), chunk2.array.std())

        # More specific tests for the exact image statistics expected
        self.assertAlmostEqual(chunk1.array.mean(), 3730.9856, places=2)
        self.assertAlmostEqual(chunk2.array.mean(), 3727.5760, places=2)
        self.assertAlmostEqual(chunk_diff.array.mean(), 3.41, places=2)
        self.assertAlmostEqual(chunk1.array.std(), 33.802116, places=2)
        self.assertAlmostEqual(chunk2.array.std(), 33.309788, places=2)
        self.assertAlmostEqual(chunk_diff.array.std(), 5.86, places=2)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
