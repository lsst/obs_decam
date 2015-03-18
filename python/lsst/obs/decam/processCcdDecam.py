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
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.afw.table as afwTable
import lsst.afw.image as afwImage
import lsst.afw.cameraGeom as afwCameraGeom
import lsst.afw.geom as afwGeom
from lsst.pipe.tasks.processImage import ProcessImageTask

class ProcessCcdDecamConfig(ProcessImageTask.ConfigClass):
    """Config for ProcessCcdDecam"""
    pass

class ProcessCcdDecamTask(ProcessImageTask):
    """Process a CCD for SDSS
    """
    ConfigClass = ProcessCcdDecamConfig
    _DefaultName = "processCcdDecam"
    dataPrefix = ""

    def __init__(self, **kwargs):
        ProcessImageTask.__init__(self, **kwargs)

    @classmethod
    def _makeArgumentParser(cls):
        """Create an argument parser

        Subclasses may wish to override, e.g. to change the dataset type or data ref level
        """
        parser = pipeBase.ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "instcal", "data ID, e.g. visit=155293 ccdnum=10")
        return parser

    def makeIdFactory(self, sensorRef):
        expBits = 24
        expId = long(sensorRef.dataId["visit"])
        return afwTable.IdFactory.makeSource(expId, 64 - expBits)

    @pipeBase.timeMethod
    def run(self, sensorRef):
        """Process a CCD: including source detection, photometry and WCS determination
        
        @param sensorRef: sensor-level butler data reference to SDSS fpC file
        @return pipe_base Struct containing these fields:
        - exposure: calibrated exposure (calexp): as computed if config.doCalibrate,
            else as upersisted and updated if config.doDetection, else None
        - calib: object returned by calibration process if config.doCalibrate, else None
        - apCorr: aperture correction: as computed config.doCalibrate, else as unpersisted
            if config.doMeasure, else None
        - sources: detected source if config.doPhotometry, else None
        """
        self.log.info("Processing %s" % (sensorRef.dataId))
        exp = sensorRef.get("instcal")

        #hack to mask and replace pixels with negative variance
        import numpy as np
        mi = exp.getMaskedImage()
        arr = mi.getVariance().getArray()
        idxNegVar = np.where(arr < 0)
        maskArr = mi.getMask().getArray()
        maskArr[idxNegVar] = 5
        arr[idxNegVar] = np.median(arr)

        # delegate most of the work to ProcessImageTask
        result = self.process(sensorRef, exp)
        return result

    def getExposureId(self, sensorRef):
        return long(sensorRef.get("ccdExposureId"))

    #This needs to be fixed in pipe_tasks.  Issue number coming up.
    def propagateCalibFlags(self, icSources, sources, matchRadius=1):
        pass
