#
# LSST Data Management System
# Copyright 2015 LSST Corporation.
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

import lsst.pex.config as pexConfig
from lsst.pipe.tasks.imageDifference import ImageDifferenceTask, ImageDifferenceConfig


class DecamImageDifferenceConfig(ImageDifferenceConfig):
    templateVisit = pexConfig.Field(
        doc="Integer visit number of the calexp to use as the template",
        dtype=int,
        default=None
    )


class DecamImageDifferenceTask(ImageDifferenceTask):
    ConfigClass = DecamImageDifferenceConfig
    _DefaultName = "ImageDifference"

    def getTemplate(self, exposure, sensorRef):
        """Return a calexp exposure that overlaps the exposure
        @param[in] exposure: exposure
        @param[in] sensorRef: a Butler data reference that can be used to obtain template calexp
        @return templateExposure: a template calexp exposure
                templateSources: sources measured on the calexp

        Assumes that the template ccd number is the same as the science ccd-number,
        and that the visit number is passed in as config.templateVisit

        Eventually we will want getTemplate() to be a subtask that can be retargeted
        or configurable.
        """

        butler = sensorRef.getButler()
        templateCalexp = butler.get('calexp',
                                    ccdnum=sensorRef.dataId['ccdnum'],
                                    visit=self.config.templateVisit)

        if self.config.doAddCalexpBackground:
            mi = templateCalexp.getMaskedImage()
            mi += sensorRef.get("calexpBackground",
                                ccdnum=sensorRef.dataId['ccdnum'],
                                visit=self.config.templateVisit).getImage()

        templateSources = butler.get('src',
                                     ccdnum=sensorRef.dataId['ccdnum'],
                                     visit=self.config.templateVisit)

        #Add validation such as: filters are same band
        return templateCalexp, templateSources
