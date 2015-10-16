#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
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
    dataPrefix = ""

    def __init__(self, **kwargs):
        ProcessCcdTask.__init__(self, **kwargs)

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

    @pipeBase.timeMethod
    def run(self, sensorRef):
        """Process a CCD: including source detection, photometry and WCS determination
        
        @param sensorRef: sensor-level butler data reference to Decam instcal file
        @return pipe_base Struct containing these fields:
        - exposure: calibrated exposure (calexp): as computed if config.doCalibrate,
            else as upersisted and updated if config.doDetection, else None
        - calib: object returned by calibration process if config.doCalibrate, else None
        - apCorr: aperture correction: as computed config.doCalibrate, else as unpersisted
            if config.doMeasure, else None
        - sources: detected source if config.doPhotometry, else None
        """
        # delegate most of the work to ProcessCcdTask (which, in turn, delegates to ProcessImageTask)
        result = ProcessCcdTask.run(self, sensorRef)
        return result

    #This needs to be fixed in pipe_tasks.  Issue number coming up.
    def propagateCalibFlags(self, icSources, sources, matchRadius=1):
        pass
