#!/usr/bin/env python2
#
# LSST Data Management System
# Copyright 2014 LSST Corporation.
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
"""Generate camera geometry for Mosaic

Example of use (if mosaic/camGeom already exists, move it aside first):

    python mosaic/makeMosaicCameraRepository.py mosaic/chipcenters.txt mosaic/segmentfile.txt mosaic/camGeom
"""
from __future__ import absolute_import
from __future__ import print_function
from builtins import range
import argparse
import os
import shutil

import lsst.utils
import lsst.afw.geom as afwGeom
import lsst.afw.table as afwTable
from lsst.afw.cameraGeom import DetectorConfig, CameraConfig, PUPIL, FOCAL_PLANE, PIXELS
from lsst.ip.isr import LinearizeLookupTable
from lsst.obs.mosaic import MosaicMapper


def makeAmpTables(segmentsFile):
    """
    Read the segments file from a PhoSim release and produce the appropriate AmpInfo
    @param segmentsFile -- String indicating where the file is located
    """
    returnDict = {}
    readoutMap = {'LL': afwTable.LL, 'LR': afwTable.LR, 'UR': afwTable.UR, 'UL': afwTable.UL}
    detectorName = [] # set to a value that is an invalid dict key, to catch bugs
    with open(segmentsFile) as fh:
        fh.readline()
        for l in fh:
            els = l.rstrip().split()
            detectorName = els[1]
            #skip focus and guiding for now:
            if detectorName[0] in ('F', 'G'):
                continue
            if detectorName not in returnDict:
                schema = afwTable.AmpInfoTable.makeMinimalSchema()
                returnDict[detectorName] = afwTable.AmpInfoCatalog(schema)
            record = returnDict[detectorName].addNew()
            name = els[2]
            gain = float(els[7])
            saturation = int(els[8])
            readnoise = float(els[9])
            xoff = int(els[5])
            yoff = int(els[6])
            ndatax = int(els[3])
            ndatay = int(els[4])

            flipx = False
            flipy = False

            if detectorName.startswith("S") and name == "A":
                readCorner = readoutMap['UR']
            elif detectorName.startswith("S") and name == "B":
                readCorner = readoutMap['UL']
            elif detectorName.startswith("N") and name == "A":
                readCorner = readoutMap['LL']
            elif detectorName.startswith("N") and name == "B":
                readCorner = readoutMap['LR']
            else:
                raise RuntimeError("Did not recognize detector name or amp name")

            prescan = 6
            hoverscan = 50
            voverscan = 50
            rawBBox = afwGeom.Box2I(afwGeom.Point2I(xoff, yoff),
                                    afwGeom.Extent2I(ndatax + prescan + hoverscan, ndatay + voverscan))
            # Note: I'm not particularry happy with how the data origin is derived (it neglects [xy]off),
            # but I don't see a better way.
            if readCorner is afwTable.LL:
                originRawData = afwGeom.Point2I(xoff + prescan + hoverscan, yoff)
                originData = afwGeom.Point2I(0, 0)
                originHOverscan = afwGeom.Point2I(xoff + prescan, yoff)
                originVOverscan = afwGeom.Point2I(xoff + prescan + hoverscan, yoff + ndatay)
                originPrescan = afwGeom.Point2I(xoff, yoff)
            elif readCorner is afwTable.LR:
                originRawData = afwGeom.Point2I(xoff, yoff)
                originData = afwGeom.Point2I(ndatax, 0)
                originHOverscan = afwGeom.Point2I(xoff + ndatax, yoff)
                originVOverscan = afwGeom.Point2I(xoff, yoff + ndatay)
                originPrescan = afwGeom.Point2I(xoff + ndatax + hoverscan, yoff)
            elif readCorner is afwTable.UL:
                originRawData = afwGeom.Point2I(xoff + prescan + hoverscan, yoff + voverscan)
                originData = afwGeom.Point2I(0, 0)
                originHOverscan = afwGeom.Point2I(xoff + prescan, yoff + voverscan)
                originVOverscan = afwGeom.Point2I(xoff + prescan + hoverscan, yoff)
                originPrescan = afwGeom.Point2I(xoff, yoff + voverscan)
            elif readCorner is afwTable.UR:
                originRawData = afwGeom.Point2I(xoff, yoff + voverscan)
                originData = afwGeom.Point2I(ndatax, 0)
                originHOverscan = afwGeom.Point2I(xoff + ndatax, yoff + voverscan)
                originVOverscan = afwGeom.Point2I(xoff, yoff)
                originPrescan = afwGeom.Point2I(xoff + ndatax + hoverscan, yoff + voverscan)
            else:
                raise RuntimeError("Expected readout corner to be LL, LR, UL, or UR")

            rawDataBBox = afwGeom.Box2I(originRawData, afwGeom.Extent2I(ndatax, ndatay))
            dataBBox = afwGeom.Box2I(originData, afwGeom.Extent2I(ndatax, ndatay))
            rawHorizontalOverscanBBox = afwGeom.Box2I(originHOverscan, afwGeom.Extent2I(hoverscan, ndatay))
            rawVerticalOverscanBBox = afwGeom.Box2I(originVOverscan, afwGeom.Extent2I(ndatax, voverscan))
            rawPrescanBBox = afwGeom.Box2I(originPrescan, afwGeom.Extent2I(prescan, ndatay))

            print("\nDetector=%s; Amp=%s" % (detectorName, name))
            print(rawHorizontalOverscanBBox)
            print(rawVerticalOverscanBBox)
            print(dataBBox)
            print(rawBBox)
            #Set the elements of the record for this amp
            record.setBBox(dataBBox) # This is the box for the amp in the assembled frame
            record.setName(name)
            record.setReadoutCorner(readCorner)
            record.setGain(gain)
            record.setSaturation(saturation)
            record.setSuspectLevel(float("nan"))
            record.setReadNoise(readnoise)
            ampIndex = dict(A=0, B=1)[name]
            record.setLinearityCoeffs([ampIndex, 0, 0, 0])
            record.setLinearityType(LinearizeLookupTable.LinearityType)
            print("Linearity type=%r; coeffs=%s" % (record.getLinearityType(), record.getLinearityCoeffs()))
            record.setHasRawInfo(True)
            record.setRawFlipX(flipx)
            record.setRawFlipY(flipy)
            record.setRawBBox(rawBBox)
            # I believe that xy offset is not needed if the raw data are pre-assembled
            record.setRawXYOffset(afwGeom.Extent2I(0, 0))
            """
            if readCorner is afwTable.LL:
                record.setRawXYOffset(afwGeom.Extent2I(xoff + prescan + hoverscan, yoff))
            elif readCorner is afwTable.LR:
                record.setRawXYOffset(afwGeom.Extent2I(xoff, yoff))
            elif readCorner is afwTable.UL:
                record.setRawXYOffset(afwGeom.Extent2I(xoff + prescan + hoverscan, yoff + voverscan))
            elif readCorner is afwTable.UR:
                record.setRawXYOffset(afwGeom.Extent2I(xoff, yoff + voverscan))
            """
            record.setRawDataBBox(rawDataBBox)
            record.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
            record.setRawVerticalOverscanBBox(rawVerticalOverscanBBox)
            # I think of prescan as being along the bottom of the raw data.  I actually
            # don't know how you would do a prescan in the serial direction.
            record.setRawPrescanBBox(afwGeom.Box2I())
    return returnDict


def makeDetectorConfigs(detectorLayoutFile):
    """
    Create the detector configs to use in building the Camera
    @param detectorLayoutFile -- String describing where the focalplanelayout.txt file is located.

    """
    detectorConfigs = []
    xsize = 2048
    ysize = 4096
    #Only do Science detectors right now.
    #There is an overall 0.05 deg rotation to the entire focal plane that I'm ignoring here.
    with open(detectorLayoutFile) as fh:
        fh.readline()
        for l in fh:
            els = l.rstrip().split()
            detectorName = els[1]
            #skip focus and guiding for now:
            if detectorName[0] in ('F', 'G'):
                continue

            detConfig = DetectorConfig()
            detConfig.name = detectorName
            detConfig.id = int(els[0])
            detConfig.bbox_x0 = 0
            detConfig.bbox_y0 = 0
            detConfig.bbox_x1 = xsize - 1
            detConfig.bbox_y1 = ysize - 1
            detConfig.detectorType = 0
            detConfig.serial = els[0]

            # Convert from microns to mm.
            detConfig.offset_x = (float(els[2]) + float(els[3]))/2.
            detConfig.offset_y = (float(els[4]) + float(els[5]))/2.

            detConfig.refpos_x = (xsize - 1.)/2.
            detConfig.refpos_y = (ysize - 1.)/2.
            # TODO translate between John's angles and Orientation angles.
            # It's not an issue now because there is no rotation except about z in John's model.
            detConfig.yawDeg = float(els[6])
            detConfig.pitchDeg = 0.
            detConfig.rollDeg = 0.
            detConfig.pixelSize_x = 0.015
            detConfig.pixelSize_y = 0.015
            detConfig.transposeDetector = False
            detConfig.transformDict.nativeSys = PIXELS.getSysName()
            # The FOCAL_PLANE and TAN_PIXEL transforms are generated by the Camera maker,
            # based on orientaiton and other data.
            # Any additional transforms (such as ACTUAL_PIXELS) should be inserted here.
            detectorConfigs.append(detConfig)
    return detectorConfigs

if __name__ == "__main__":
    """
    Create the configs for building a camera.
    """
    baseDir = lsst.utils.getPackageDir("obs_mosaic")
    defaultOutDir = os.path.join(os.path.normpath(baseDir), "description", "camera")

    parser = argparse.ArgumentParser()
    parser.add_argument("DetectorLayoutFile", help="Path to detector layout file")
    parser.add_argument("SegmentsFile", help="Path to amp segments file")
    parser.add_argument("OutputDir",
                        help="Path to dump configs and AmpInfo Tables; defaults to %r" % (defaultOutDir,),
                        nargs="?",
                        default=defaultOutDir,
                        )
    parser.add_argument("--clobber", action="store_true", dest="clobber", default=False,
                        help=("remove and re-create the output directory if it already exists?"))
    args = parser.parse_args()
    ampTableDict = makeAmpTables(args.SegmentsFile)
    detectorConfigList = makeDetectorConfigs(args.DetectorLayoutFile)

    #Build the camera config.
    camConfig = CameraConfig()
    camConfig.detectorList = dict([(i, detectorConfigList[i]) for i in range(len(detectorConfigList))])
    camConfig.name = 'Mosaic'
    #From Mosaic calibration doc
    camConfig.plateScale = 17.575
    pScaleRad = afwGeom.arcsecToRad(camConfig.plateScale)
    tConfig = afwGeom.TransformConfig()
    tConfig.transform.name = 'radial'
    nomWavelen = 0.625 #nominal wavelen in microns
    coeff0 = 0
    coeff1 = 1 - 2.178e-4 - 2.329e-4/nomWavelen + 4.255e-5/nomWavelen**2
    coeff2 = 0
    coeff3 = -6.174e-8 + 5.569e-9/nomWavelen
    tConfig.transform.active.coeffs = [pScaleRad*coeff0, pScaleRad*coeff1, pScaleRad*coeff2,
                                       pScaleRad*coeff3]
    tmc = afwGeom.TransformMapConfig()
    tmc.nativeSys = FOCAL_PLANE.getSysName()
    tmc.transforms = {PUPIL.getSysName(): tConfig}
    camConfig.transformDict = tmc

    def makeDir(dirPath, doClobber=False):
        """Make a directory; if it exists then clobber or fail, depending on doClobber

        @param[in] dirPath: path of directory to create
        @param[in] doClobber: what to do if dirPath already exists:
            if True and dirPath is a dir, then delete it and recreate it, else raise an exception
        @throw RuntimeError if dirPath exists and doClobber False
        """
        if os.path.exists(dirPath):
            if doClobber and os.path.isdir(dirPath):
                print("Clobbering directory %r" % (dirPath,))
                shutil.rmtree(dirPath)
            else:
                raise RuntimeError("Directory %r exists" % (dirPath,))
        print("Creating directory %r" % (dirPath,))
        os.makedirs(dirPath)

    # write data products
    outDir = args.OutputDir
    makeDir(dirPath=outDir, doClobber=args.clobber)

    camConfigPath = os.path.join(outDir, "camera.py")
    camConfig.save(camConfigPath)

    for detectorName, ampTable in ampTableDict.items():
        shortDetectorName = MosaicMapper.getShortCcdName(detectorName)
        ampInfoPath = os.path.join(outDir, shortDetectorName + ".fits")
        ampTable.writeFits(ampInfoPath)
