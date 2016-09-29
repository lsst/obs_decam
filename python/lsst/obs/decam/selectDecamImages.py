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
from __future__ import print_function
import MySQLdb
import os
import re

import lsst.pex.config as pexConfig
from lsst.afw.coord import IcrsCoord
import lsst.afw.geom as afwGeom
from lsst.daf.persistence import DbAuth
import lsst.pipe.base as pipeBase
from lsst.pipe.tasks.selectImages import DatabaseSelectImagesConfig, BaseSelectImagesTask, BaseExposureInfo

__all__ = ["SelectDecamImagesTask"]


class SelectDecamImagesConfig(DatabaseSelectImagesConfig):
    """Config for SelectDecamImagesTask
    """
    table = pexConfig.Field(
        doc="Name of database table",
        dtype=str,
        default="y1CcdQuality",
    )

    def setDefaults(self):
        BaseSelectImagesTask.ConfigClass.setDefaults(self)
        self.host = "lsst-db.ncsa.illinois.edu"
        self.port = 3306
        self.database = "yusra_y1_quality_db"

    def validate(self):
        BaseSelectImagesTask.ConfigClass.validate(self)
        if not re.match(r"^[a-zA-Z0-9_.]+$", self.table):
            raise RuntimeError("table=%r is an invalid name" % (self.table,))


class ExposureInfo(BaseExposureInfo):
    """Data about a selected exposure

    Data includes:
    - dataId: data ID of exposure (a dict)
    - coordList: a list of corner coordinates of the exposure (list of IcrsCoord)
    - fwhm: mean FWHM of exposure
    - airmass: mean airmass of exposure
    - filename: original filename of exposure
    """

    def __init__(self, result):
        """Set exposure information based on a query result from a db connection
        """
        self._ind = -1

        dataId = dict(
            visit=result[self._nextInd],
            ccdnum=result[self._nextInd],
            filter=result[self._nextInd],
        )
        coordList = []
        for i in range(4):
            coordList.append(
                IcrsCoord(
                    afwGeom.Angle(result[self._nextInd], afwGeom.degrees),
                    afwGeom.Angle(result[self._nextInd], afwGeom.degrees),
                )
            )
        BaseExposureInfo.__init__(self, dataId, coordList)

        self.fwhm = result[self._nextInd]
        self.airmass = result[self._nextInd]
        self.filename = result[self._nextInd]

    @property
    def _nextInd(self):
        """Return the next index

        This allows one to progress through returned database columns,
        repeatedly using _nextInd, e.g.:
            dataId = dict(
                visit = result[self._nextInd],
                ccdnum = result[self._nextInd],
                filter = result[self._nextInd],
            )
        """
        self._ind += 1
        return self._ind

    @staticmethod
    def getColumnNames():
        """Get database columns to retrieve, in a format useful to the database interface

        @return database column names as list of strings
        """
        return (
            "visit ccdNum filter ra1 dec1 ra2 dec2 ra3 dec3 ra4 dec4".split() +
            "fwhm airmass filename".split()
        )


class SelectDecamImagesTask(BaseSelectImagesTask):
    """Select Decam images suitable for coaddition
    """
    ConfigClass = SelectDecamImagesConfig
    _DefaultName = "selectImages"

    @pipeBase.timeMethod
    def run(self, coordList, filter):
        """Select Decam images suitable for coaddition in a particular region

        @param[in] filter: filter for images (one of g", "r", "i", "z", Y")
        @param[in] coordList: list of coordinates defining region of interest

        @return a pipeBase Struct containing:
        - exposureInfoList: a list of ExposureInfo objects
        """
        if filter not in set(("g", "r", "i", "z", "Y")):
            raise RuntimeError("filter=%r is an invalid name" % (filter,))

        read_default_file = os.path.expanduser("~/.my.cnf")

        try:
            open(read_default_file)
            kwargs = dict(
                read_default_file=read_default_file,
            )
        except IOError:
            kwargs = dict(
                user=DbAuth.username(self.config.host, str(self.config.port)),
                passwd=DbAuth.password(self.config.host, str(self.config.port)),
            )

        db = MySQLdb.connect(
            host=self.config.host,
            port=self.config.port,
            db=self.config.database,
            **kwargs
        )
        cursor = db.cursor()

        columnNames = tuple(ExposureInfo.getColumnNames())
        if not columnNames:
            raise RuntimeError("Bug: no column names")
        queryStr = "select %s " % (", ".join(columnNames),)
        dataTuple = () # tuple(columnNames)

        if coordList is not None:
            # look for exposures that overlap the specified region

            # create table scisql.Region containing patch region
            coordStrList = ["%s, %s" % (c.getLongitude().asDegrees(),
                                        c.getLatitude().asDegrees()) for c in coordList]
            coordStr = ", ".join(coordStrList)
            coordCmd = "call scisql.scisql_s2CPolyRegion(scisql_s2CPolyToBin(%s), 10)" % (coordStr,)
            cursor.execute(coordCmd)
            cursor.nextset() # ignore one-line result of coordCmd

            queryStr += """
    from %s as ccdExp,
    (select distinct id
    from y1CcdQuality_To_Htm10 as ccdHtm inner join scisql.Region
    on (ccdHtm.htmId10 between scisql.Region.htmMin and scisql.Region.htmMax)
    where ccdHtm.filter = %%s) as idList
    where ccdExp.id = idList.id and """ % (self.config.table,)
            dataTuple += (filter,)
        else:
            # no region specified; look over the whole sky
            queryStr += " from %s as ccdExp where " % (self.config.table,)

        # compute where clauses as a list of (clause, data)
        whereDataList = [
            ("filter = %s", filter),
        ]

        queryStr += " and ".join(wd[0] for wd in whereDataList)
        dataTuple += tuple(wd[1] for wd in whereDataList)
        self.log.info("queryStr=%r; dataTuple=%s" % (queryStr, dataTuple))

        cursor.execute(queryStr, dataTuple)
        exposureInfoList = [ExposureInfo(result) for result in cursor]

        return pipeBase.Struct(
            exposureInfoList=exposureInfoList,
        )

    def _runArgDictFromDataId(self, dataId):
        """Extract keyword arguments for run (other than coordList) from a data ID
        @return keyword arguments for run (other than coordList), as a dict
        """
        return dict(
            filter=dataId["filter"],
        )

if __name__ == "__main__":
    # example of use
    selectTask = SelectDecamImagesTask()
    minRa = afwGeom.Angle(351, afwGeom.degrees)
    maxRa = afwGeom.Angle(354, afwGeom.degrees)
    minDec = afwGeom.Angle(-1, afwGeom.degrees)
    maxDec = afwGeom.Angle(1, afwGeom.degrees)
    coordList = [
        IcrsCoord(minRa, minDec),
        IcrsCoord(maxRa, minDec),
        IcrsCoord(maxRa, maxDec),
        IcrsCoord(minRa, maxDec),
    ]
    results = selectTask.run(coordList=coordList, filter='r')
    filenames = set()

    for ccdInfo in results.exposureInfoList:
        print("dataId=%s, fwhm=%s, filename=%s" % (ccdInfo.dataId, ccdInfo.fwhm, ccdInfo.filename))
        filenames.add(ccdInfo.filename)

    print(filenames)
