from builtins import range
import lsst.afw.geom as afwGeom
import lsst.afw.cameraGeom as cameraGeom

pixelSize = 24e-3                   # pixel size in mm


def makeAmp(i):
    height = 2048
    width = 4096
    allPixels = afwGeom.BoxI(afwGeom.PointI(0, 0), afwGeom.ExtentI(width + nExtended + nOverclock, height))
    return cameraGeom.Amp(cameraGeom.Id(i), allPixels, None, None, None)


def makeCcd(ccdName):
    ccd = cameraGeom.Ccd(cameraGeom.Id(ccdName), pixelSize)
    ccd.addAmp(1, 0, makeAmp(1))
    return ccd


def makeRaft(raftName):
    dewar = cameraGeom.Raft(cameraGeom.Id("Mosaic"), 1, 1)
    dewar.addDetector(afwGeom.PointI(0, 0), cameraGeom.FpPoint(0.0, 0.0),
                      cameraGeom.Orientation(0), makeCcd(raftName))
    return dewar


def makeCamera(name="Mosaic"):
    camera = cameraGeom.Camera(cameraGeom.Id(name), 62, 1)

    for i in range(62):
        if i > 31:
            dewarName = "S%d" % (62-i+1)
        else:
            dewarName = "S%d" % (i+1)
        camera.addDetector(afwGeom.PointI(i, 0), cameraGeom.FpPoint(25.4*2.5*(2.5 - i), 0.0),
                           cameraGeom.Orientation(0), makeRaft(dewarName))

    return camera
