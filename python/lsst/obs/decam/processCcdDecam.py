#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008-2015 AURA/LSST.
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
# see <https://www.lsstcorp.org/LegalNotices/>.
#
import lsst.pipe.base as pipeBase
from lsst.pipe.tasks.processCcd import ProcessCcdTask

class ProcessCcdDecamConfig(ProcessCcdTask.ConfigClass):
    """Config for ProcessCcdDecam"""

    def setDefaults(self):
        ProcessCcdTask.ConfigClass.setDefaults(self)
        self.doIsr = False

class ProcessCcdDecamTask(ProcessCcdTask):
    """Process a CCD for Decam
    """
    ConfigClass = ProcessCcdDecamConfig
    _DefaultName = "processCcdDecam"

    @classmethod
    def _makeArgumentParser(cls):
        """Create an argument parser

        Subclasses may wish to override, e.g. to change the dataset type or data ref level
        """
        parser = pipeBase.ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "instcal", "data ID, e.g. visit=155293 ccdnum=10")
        return parser

    def setPostIsrExposure(self, sensorRef):
        """Load the post instrument signature removal image

        \param[in]  sensorRef        sensor-level butler data reference

        \return     postIsrExposure  exposure to be passed to processCcdExposure
        """
        exp = sensorRef.get("instcal")
        return exp
