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

import astropy.units

from lsst.afw.coord import Observatory, Weather
from lsst.afw.geom import SpherePoint
from lsst.obs.base import MakeRawVisitInfo

__all__ = ["MakeDecamRawVisitInfo"]


class MakeDecamRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a raw DECam image

    Fields that are not set:
    - exposureId
    - ut1
    - era (set by back-computing from HourAngle and RA, but not fully correct: see DM-8503)
    - boresightRotAngle
    - rotType
    """
    def setArgDict(self, md, argDict):
        """Set an argument dict for VisitInfo and pop associated metadata

        @param[in,out] md  metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict  a dict of arguments
        """
        MakeRawVisitInfo.setArgDict(self, md, argDict)
        argDict["darkTime"] = self.popFloat(md, "DARKTIME")
        argDict["boresightAzAlt"] = SpherePoint(
            self.popAngle(md, "AZ"),
            self.altitudeFromZenithDistance(self.popAngle(md, "ZD")),
        )
        argDict["boresightRaDec"] = SpherePoint(
            self.popAngle(md, "TELRA", units=astropy.units.h),
            self.popAngle(md, "TELDEC"),
        )
        argDict["boresightAirmass"] = self.popFloat(md, "AIRMASS")
        argDict["observatory"] = Observatory(
            self.popAngle(md, "OBS-LONG"),
            self.popAngle(md, "OBS-LAT"),
            self.popFloat(md, "OBS-ELEV"),
        )
        # Default weather is based on typical conditions at an altitude of 2215 meters.
        temperature = self.defaultMetadata(self.popFloat(md, "OUTTEMP"), 10., minimum=-10., maximum=40.)
        pressure = self.defaultMetadata(self.pascalFromMmHg(self.popFloat(md, "PRESSURE")), 77161.1,
                                        minimum=70000., maximum=85000.)
        humidity = self.defaultMetadata(self.popFloat(md, "HUMIDITY"), 40., minimum=0., maximum=100.)
        argDict["weather"] = Weather(temperature, pressure, humidity)
        longitude = argDict["observatory"].getLongitude()
        argDict['era'] = self.decamGetEra(md, argDict["boresightRaDec"][0], longitude)

    def getDateAvg(self, md, exposureTime):
        """Return date at the middle of the exposure

        @param[in,out] md  FITS metadata; changed in place
        @param[in] exposureTime  exposure time in sec
        """
        dateObs = self.popIsoDate(md, "DATE-OBS")
        return self.offsetDate(dateObs, 0.5*exposureTime)

    def decamGetEra(self, md, RA, longitude):
        """
        DECAM provides HA, so we can get LST and thus an ERA-equivalent from that.

        NOTE: if we deal with DM-8053 and implement UT1, we can delete this method and use UT1 directly.
        """
        HA = self.popAngle(md, "HA", units=astropy.units.h)
        return HA + RA - longitude
