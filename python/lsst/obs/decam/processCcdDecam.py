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
from .decamNullIsr import DecamNullIsrTask

class ProcessCcdDecamConfig(ProcessCcdTask.ConfigClass):
    """Config for ProcessCcdDecam"""

    def setDefaults(self):
        ProcessCcdTask.ConfigClass.setDefaults(self)
        self.isr.retarget(DecamNullIsrTask)


## \addtogroup LSST_task_documentation
## \{
## \page ProcessCcdDecamTask
## \ref ProcessCcdDecamTask_ "ProcessCcdDecamTask"
## \copybrief ProcessCcdDecamTask
## \}

class ProcessCcdDecamTask(ProcessCcdTask):
    """!Process DECam "instcal" images

    @anchor ProcessCcdDecamTask_
    
    @section pipe_tasks_processCcdDecam_Contents  Contents

     - @ref pipe_tasks_processCcdDecam_Purpose
     - @ref pipe_tasks_processCcdDecam_Initialize
     - @ref pipe_tasks_processCcdDecam_IO
     - @ref pipe_tasks_processCcdDecam_Config

    @section pipe_tasks_processCcdDecam_Purpose  Description

    Process "instcal" data from the community pipeline, as loaded by DecamNullIsrTask.
    This trivial subclass of lsst.pipe.tasks.ProcessCcdTask exists solely to provide the correct dataset type
    to the `--id` command-line argument. Once ticket DM-4952 is implemented this task will not be needed.

    @section pipe_tasks_processCcdDecam_Initialize  Task initialisation

    @copydoc \_\_init\_\_

    @section pipe_tasks_processCcdDecam_IO  Invoking the Task

    The main method is `run`.

    @section pipe_tasks_processCcdDecam_Config  Configuration parameters

    See @ref ProcessCcdDecamConfig
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
