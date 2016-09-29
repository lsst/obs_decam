#!/usr/bin/env python

from __future__ import print_function
import argparse
import os
import shutil
import sqlite3
import lsst.daf.persistence as dafPersist


parser = argparse.ArgumentParser(description='Output the defects in text format')
parser.add_argument("--root", default=".", help="Root directory of data repository")
parser.add_argument("--outputDir", default="defects", help="Directory to dump the output text files")
parser.add_argument("--clobber", action="store_true", default=False,
                    help="Remove and re-create the output directory if it already exists?")
args = parser.parse_args()

if os.path.exists(args.outputDir):
    if args.clobber and os.path.isdir(args.outputDir):
        print("Clobbering directory %r" % args.outputDir)
        shutil.rmtree(args.outputDir)
    else:
        raise RuntimeError("Directory %r exists" % args.outputDir)

registryName = os.path.join(args.root, "calibRegistry.sqlite3")
conn = sqlite3.connect(registryName)
conn.text_factory = str
cursor = conn.cursor()
cmd = "select distinct validStart from defect;"
cursor.execute(cmd)
rows = cursor.fetchall()
conn.close()

butler = dafPersist.Butler(args.root)
for row in rows:
    date = row[0]
    os.makedirs(os.path.join(args.outputDir, date))
    filePath = os.path.join(args.outputDir, date, 'defects.dat')
    print("Writing file ", filePath)
    f = open(filePath, 'w')
    f.write("#CCD x0    y0    width height\n")
    for ccdnum in range(1, 63):
        defectList = butler.get("defects", date=date, ccdnum=ccdnum)
        for defect in defectList:
            bbox = defect.getBBox()
            s = (repr(ccdnum).ljust(5) + repr(bbox.getBeginX()).ljust(6) +
                 repr(bbox.getBeginY()).ljust(6) + repr(bbox.getWidth()).ljust(6) +
                 repr(bbox.getHeight()).ljust(6) + '\n')
            f.write(s)
    f.close()
