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

"""Butler instrument description for the Dark Energy Camera.
"""

__all__ = ("DarkEnergyCamera",)

import os
from functools import lru_cache

from astro_metadata_translator import DecamTranslator
from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.obs.base import Instrument, VisitSystem
from lsst.obs.decam.decamFilters import DECAM_FILTER_DEFINITIONS

from lsst.utils.introspection import get_full_type_name
from lsst.utils import getPackageDir


class DarkEnergyCamera(Instrument):
    filterDefinitions = DECAM_FILTER_DEFINITIONS
    policyName = "decam"
    obsDataPackage = "obs_decam_data"
    translatorClass = DecamTranslator

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        packageDir = getPackageDir("obs_decam")
        self.configPaths = [os.path.join(packageDir, "config")]

    @classmethod
    def getName(cls):
        return "DECam"

    def getCamera(self):
        path = os.path.join(getPackageDir("obs_decam"), self.policyName, "camGeom")
        return self._getCameraFromPath(path)

    @staticmethod
    @lru_cache()
    def _getCameraFromPath(path):
        """Return the camera geometry given solely the path to the location
        of that definition."""
        config = CameraConfig()
        config.load(os.path.join(path, "camera.py"))
        return makeCameraFromPath(
            cameraConfig=config,
            ampInfoPath=path,
            shortNameFunc=lambda name: name.replace(" ", "_"),
        )

    def register(self, registry, update=False):
        camera = self.getCamera()
        # Combined with detector_max=100 (below), obsMax=2**25 causes the
        # number of bits in packed IDs to match the Gen2 ones.
        obsMax = 2**25
        with registry.transaction():
            # Note that detector_max here is really only used for packing
            # detector and visit/exposure IDs together into a single integer,
            # so it's rounded up to the nearest power of ten to make that
            # encoding decodable by humans (and consistent with its previous
            # Gen2 definition).  There are other checks (database constraints)
            # that ensure any ingested raws have "real" detector values, and
            # those are based on the detector records added in the loop below.
            registry.syncDimensionData(
                "instrument",
                {
                    "name": self.getName(), "detector_max": 100, "visit_max": obsMax, "exposure_max": obsMax,
                    "class_name": get_full_type_name(self),
                    # Some schemas support default visit_system
                    "visit_system": VisitSystem.ONE_TO_ONE.value,
                },
                update=update
            )

            for detector in camera:
                registry.syncDimensionData(
                    "detector",
                    {
                        "instrument": self.getName(),
                        "id": detector.getId(),
                        "full_name": detector.getName(),
                        "name_in_raft": detector.getName()[1:],
                        "raft": detector.getName()[0],
                        "purpose": str(detector.getType()).split(".")[-1],
                    },
                    update=update
                )

            self._registerFilters(registry, update=update)

    def getRawFormatter(self, dataId):
        # local import to prevent circular dependency
        from .rawFormatter import DarkEnergyCameraRawFormatter
        return DarkEnergyCameraRawFormatter
