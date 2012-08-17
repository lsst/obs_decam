#!/usr/bin/env python

import glob
import os
import re
import sqlite
import sys
import datetime
import lsst.daf.base   as dafBase
import lsst.pex.policy as pexPolicy
import lsst.afw.image  as afwImage


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--create", default=False, action="store_true", help="Create new registry (clobber old)?")
parser.add_argument("--root", default=".", help="Root directory")
args = parser.parse_args()

root = args.root
if root == '-':
    files = [l.strip() for l in sys.stdin.readlines()]
else:
    files = glob.glob(os.path.join(root, "*", "*-*-*", "*.fits"))
sys.stderr.write('processing %d files...\n' % (len(files)))

registryName = "registry.sqlite3"
if os.path.exists(registryName) and args.create:
    os.unlink(registryName)

makeTables = not os.path.exists(registryName)
conn = sqlite.connect(registryName)
if makeTables:
    cmd = "create table raw (id integer primary key autoincrement"
    cmd += ", field text, year int, doy int, frac int"
    cmd += ", date text, datetime text, unique(year, doy, frac))"
    conn.execute(cmd)
    conn.commit()

for fits in files:
    matches = re.search(r"(\S+)/(\d{4}-\d{2}-\d{2})/(\d{4})(\d{3})_(\d{6})\.fits", fits)
    if not matches:
        print >>sys.stderr, "Warning: skipping unrecognized filename:", fits
        continue

    sys.stderr.write("Processing %s\n" % (fits))

    field, date, year, doy, frac = matches.groups()

    year = int(year)
    doy = int(doy)
    frac = int(frac)
    
    hours = int(frac*24/10**6)
    sec = frac*86400/10**6 - hours*3600

    dateObs = (datetime.datetime(year, 1, 1) +
               datetime.timedelta(days=doy-1, hours=hours, seconds=sec)).isoformat()

    try:
        conn.execute("INSERT INTO raw VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                     (field, year, doy, frac, date, dateObs))

    except Exception, e:
        print "skipping botched %s: %s" % (fits, e)
        continue

conn.commit()
conn.close()
