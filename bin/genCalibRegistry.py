#!/usr/bin/env python

import glob
import os
import re
import sqlite
import sys
import math
import datetime
import collections

import lsst.daf.base   as dafBase
import lsst.afw.image  as afwImage

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--create", default=False, action="store_true", 
                    help="Create new registry (clobber old)?")
parser.add_argument("--root", default=".", help="Root directory")
parser.add_argument("--validity", type=int, default=30, help="Calibration validity (days)")
args = parser.parse_args()

registry = os.path.join(args.root, "calibRegistry.sqlite3")

if os.path.exists(registry):
    if args.create:
        os.unlink(registry)
    else:
        args.create = True
conn = sqlite.connect(registry)

Row = collections.namedtuple("Row", ["calibDate", "calibVersion", "ccd"])

for calib in ('bias', 'dark', 'flat', 'fringe'):
    if args.create:
        cmd = "create table " + calib.lower() + " (id integer primary key autoincrement"
        cmd += ", validStart text, validEnd text"
        cmd += ", calibDate text, calibVersion int, ccd int"
        cmd += ")"
        conn.execute(cmd)
        conn.commit()

    rows = list()

    for fits in glob.glob(os.path.join(args.root, calib.upper(), "20*-*-*", calib.upper() + "-*-*.fits*")):
        print fits
        matches = re.search(r'\w+/(\d{4})-(\d{2})-(\d{2})/\w+-(\d+)-(\d+)\.fits.*', fits)
        if not matches:
            print >>sys.stderr, "Warning: Unrecognized file:", fits
            continue
        year, month, day, calibVersion, ccd = matches.groups()

        date = datetime.date(int(year), int(month), int(day))
        rows.append(Row(date, calibVersion, ccd))

    # Fix up the validStart,validEnd so there are no overlaps
    rows.sort(key=lambda row: row.calibDate)
    validity = datetime.timedelta(args.validity)
    valids = collections.OrderedDict([(row.calibDate, [row.calibDate - validity,
                                                       row.calibDate + validity]) for row in rows])
    dates = valids.keys()
    numDates = len(dates)
    midpoints = [ t1 + (t2 - t1)//2 for t1, t2 in zip(dates[:numDates-1], dates[1:]) ]
    for i, (date, midpoint) in enumerate(zip(dates[:numDates-1], midpoints)):
        if valids[date][1] > midpoint:
            nextDate = dates[i+1]
            #print "Adjusting: %d %s --> %s : %s vs %s" % (i, date, nextDate, valids[date][1], midpoint)
            valids[nextDate][0] = midpoint
            valids[date][1] = midpoint
    del midpoints
    del dates

    for row in rows:
        calibDate = row.calibDate.isoformat()
        validStart = valids[row.calibDate][0].isoformat()
        validEnd = valids[row.calibDate][1].isoformat()

        # print "%f --> %f %f" % (calibDate, validStart, validEnd)

        conn.execute("INSERT INTO " + calib.lower() + " VALUES (NULL, ?, ?, ?, ?, ?)",
                     (validStart, validEnd, calibDate, row.calibVersion, row.ccd))
        

conn.commit()
conn.close()
