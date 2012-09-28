#!/usr/bin/env python

"""Cut an SST image into its component CCDs"""

import sys
import os.path
import lsst.afw.image as afwImage
import lsst.afw.geom as afwGeom

xSize, ySize = 2048, 4096

for name in sys.argv[1:]:
    image = afwImage.ImageF(name)
    rootname, ext = os.path.splitext(name)
    for num in range(12):
        x, y = num % 6, num // 6
        bbox = afwGeom.Box2I(afwGeom.Point2I(x * xSize, y * ySize), afwGeom.Extent2I(xSize, ySize))
        sub = image.Factory(image, bbox, True)
        sub.setXY0(afwGeom.Point2I(0, 0))
        sub.writeFits("%s_%02d%s" % (rootname, num, ext))

