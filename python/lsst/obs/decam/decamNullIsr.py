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
import lsst.pex.config as pexConfig


class DecamNullIsrConfig(pexConfig.Config):
    doWrite = pexConfig.Field(
        dtype=bool,
        doc="Persist loaded data as a postISRCCD? The default is false, to avoid duplicating data.",
        default=False,
    )
    datasetType = pexConfig.Field(
        dtype=str,
        doc="Dataset type for input data; read by ProcessCcdTask; users will typically leave this alone",
        default="instcal",
    )


class DecamNullIsrTask(pipeBase.Task):
    """Load an "instcal" exposure as a post-ISR CCD exposure.

    Load "instcal" exposures from the community pipeline as a post-ISR exposure,
    and optionally persist it as a `postISRCCD`.

    This is used to retarget the `isr` subtask in `ProcessCcdTask` when you prefer to use
    the community pipeline instead of the LSST software stack to perform ISR on DECam images.
    """
    ConfigClass = DecamNullIsrConfig
    _DefaultName = "isr"

    @pipeBase.timeMethod
    def runDataRef(self, sensorRef):
        """Load a DECam community pipeline "instcal" exposure as a post-ISR CCD exposure

        Parameters
        ----------
        sensorRef : `lsst.daf.persistence.butlerSubset.ButlerDataRef`
            Butler data reference for post-ISR exposure.

        Returns
        -------
        result : `struct`
            A pipeBase.Struct with fields:

            - ``exposure`` : Exposure after application of ISR: the "instcal" exposure, unchanged.

        """
        self.log.info("Loading DECam community pipeline file %s" % (sensorRef.dataId))

        exposure = sensorRef.get("instcal", immediate=True)
        if self.config.doWrite:
            sensorRef.put(exposure, "postISRCCD")

        return pipeBase.Struct(
            exposure=exposure,
        )
