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

from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.daf.butler.instrument import Instrument
from lsst.obs.decam.decamFilters import DECAM_FILTER_DEFINITIONS

from lsst.utils import getPackageDir


class DarkEnergyCamera(Instrument):
    filterDefinitions = DECAM_FILTER_DEFINITIONS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        packageDir = getPackageDir("obs_decam")
        self.configPaths = [os.path.join(packageDir, "config")]

    @classmethod
    def getName(cls):
        return "DECam"

    def getCamera(self):
        path = os.path.join(getPackageDir("obs_decam"), "decam", "camGeom")
        config = CameraConfig()
        config.load(os.path.join(path, "camera.py"))
        return makeCameraFromPath(
            cameraConfig=config,
            ampInfoPath=path,
            shortNameFunc=lambda name: name.replace(" ", "_"),
        )

    def register(self, registry):
        camera = self.getCamera()
        dataId = {"instrument": self.getName()}
        obsMax = 2**31
        registry.addDimensionEntry("instrument", dataId,
                                   entries={"detector_max": 64,
                                            "visit_max": obsMax,
                                            "exposure_max": obsMax})

        for detector in camera:
            registry.addDimensionEntry(
                "detector", dataId,
                detector=detector.getId(),
                name=detector.getName(),
            )

        self._registerFilters(registry)

    def getRawFormatter(self, dataId):
        # local import to prevent circular dependency
        from .rawFormatter import DarkEnergyCameraRawFormatter
        return DarkEnergyCameraRawFormatter

    def writeCuratedCalibrations(self, butler):
        # TODO: DM-21016
        pass
