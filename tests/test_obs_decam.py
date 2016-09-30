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
import os
import sys
import unittest

import lsst.utils.tests
from lsst.utils import getPackageDir
from lsst.afw.geom import Extent2I
import lsst.obs.base.tests
import lsst.obs.test
import lsst.daf.persistence
from lsst.ip.isr import LinearizeLookupTable


class TestObsDecam(lsst.obs.base.tests.ObsTests, lsst.utils.tests.TestCase):
    def setUp(self):
        product_dir = getPackageDir('testdata_decam')
        self.data_dir = os.path.join(product_dir, 'rawData')
        calib_root = os.path.join(product_dir, 'rawData', 'cpCalib')

        self.butler = lsst.daf.persistence.Butler(root=self.data_dir, calibRoot=calib_root)
        self.mapper = lsst.obs.decam.DecamMapper(root=self.data_dir)
        self.dataIds = {'raw': {'visit': 229388, 'filter': 'z', 'ccdnum': 1},
                        'bias': unittest.SkipTest,
                        'flat': unittest.SkipTest,
                        'dark': unittest.SkipTest
                        }

        ccdExposureId_bits = 32
        exposureIds = {'raw': 22938801}
        filters = {'raw': 'z'}
        exptimes = {'raw': 200.0}
        detectorIds = {'raw': 1}
        detector_names = {'raw': 'S29'}
        detector_serials = {'raw': '1'}
        dimensions = {'raw': Extent2I(2160, 4146)}
        sky_origin = (42.819958, -0.001583)
        raw_subsets = (({'level': 'sensor', 'visit': 229388, 'ccdnum': 1}, 1),
                       ({'level': 'sensor', 'visit': 229388}, 2),
                       ({'level': 'visit', 'visit': 229388}, 1)
                       )
        good_detectorIds = tuple(range(1, 62))
        bad_detectorIds = (0, 63)
        linearizer_type = {x: LinearizeLookupTable.LinearityType for x in good_detectorIds}
        self.setUp_butler_get(ccdExposureId_bits=ccdExposureId_bits,
                              exposureIds=exposureIds,
                              filters=filters,
                              exptimes=exptimes,
                              detectorIds=detectorIds,
                              detector_names=detector_names,
                              detector_serials=detector_serials,
                              dimensions=dimensions,
                              sky_origin=sky_origin,
                              raw_subsets=raw_subsets,
                              good_detectorIds=good_detectorIds,
                              bad_detectorIds=bad_detectorIds,
                              linearizer_type=linearizer_type
                              )

        path_to_raw = os.path.join(self.data_dir, "raw", "raw.fits")
        keys = set(('filter', 'patch', 'tract', 'visit', 'date', 'ccdnum',
                    'pointing', 'path', 'calibDate', 'hdu'))
        query_format = ["visit", "filter"]
        queryMetadata = (({'visit': 229388}, [(229388, 'z')]),
                         ({'filter': 'z'}, [(229388, 'z')]),
                         )
        metadata_output_path = os.path.join(self.data_dir, '0229388', 'metadata', 'metadata-0229388_01.boost')
        map_python_type = 'lsst.afw.image.DecoratedImageF'
        map_cpp_type = 'DecoratedImageF'
        map_storage_name = 'FitsStorage'
        raw_filename = 'decam0229388.fits.fz[2]'
        default_level = 'sensor'
        raw_levels = (('skyTile', set(['filter', 'date'])),
                      ('filter', set(['filter', 'visit', 'date', 'hdu', 'ccdnum'])),
                      ('visit', set(['filter', 'visit', 'date']))
                      )
        self.setUp_mapper(output=self.data_dir,
                          path_to_raw=path_to_raw,
                          keys=keys,
                          query_format=query_format,
                          queryMetadata=queryMetadata,
                          metadata_output_path=metadata_output_path,
                          map_python_type=map_python_type,
                          map_cpp_type=map_cpp_type,
                          map_storage_name=map_storage_name,
                          raw_filename=raw_filename,
                          default_level=default_level,
                          raw_levels=raw_levels,
                          )

        self.setUp_camera(camera_name='DECAM',
                          n_detectors=62,
                          first_detector_name='S29'
                          )

        super(TestObsDecam, self).setUp()


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == '__main__':
    setup_module(sys.modules[__name__])
    unittest.main()
