#
# LSST Data Management System
# Copyright 2012 LSST Corporation.
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

from lsst.pipe.tasks.ingest import ParseTask

def parseExtname(md):
    side, ccd = "X", 0
    if not md.exists("EXTNAME"):
        return side, ccd
    extname = md.get("EXTNAME").strip()
    if extname[0] in "NS":
        side = extname[0]
    ccd = int(extname[1:])
    return side, ccd

class DecamParseTask(ParseTask):
    def translate_side(self, md):
        side, ccd = parseExtname(md)
        return side

    def translate_ccd(self, md):
        side, ccd = parseExtname(md)
        return ccd

    def translate_object(self, md):
        obj = None
        if md.exists("OBJECT"):
            obj = md.get("OBJECT").strip()
        if obj is None or len(obj) == 0 and md.exists("OBSTYPE"):
            obj = md.get("OBSTYPE").strip()
        if obj is None or len(obj) == 0:
            return "UNKNOWN"
        return obj
