#!/usr/bin/env python

import os
import pwd

import lsst.afw.geom as afwGeom
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils

from lsst.daf.butlerUtils import CameraMapper
import lsst.pex.policy as pexPolicy

class SstMapper(CameraMapper):
    def __init__(self, outputRoot=None, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile("obs_sst", "SstMapper.paf", "policy")
        super(SstMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)

        afwImageUtils.defineFilter('OPEN', lambdaEff=650)

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        pathId = self._transformId(dataId)
        year = pathId['year']
        doy = pathId['doy']
        sod = pathId['frac']
        ccd = pathId['ccd']
        return 0 # XXX FIXME

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 32 # not really, but this leaves plenty of space for sources

    def _computeStackExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a Stack exposure.

        @param dataId (dict) Data identifier with stack, patch, filter
        """
        nPatches = 1000000
        return (long(dataId["stack"]) * nPatches + long(dataId["patch"]))

    def bypass_stackExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeStackExposureId(dataId)

    def bypass_stackExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 32 # not really, but this leaves plenty of space for sources

    def _setTimes(self, mapping, item, dataId):
        """Set the exposure time and exposure midpoint in the calib object in an Exposure.

        @param mapping (lsst.daf.butlerUtils.Mapping)
        @param[in,out] item (lsst.afw.image.Exposure)
        @param dataId (dict) Dataset identifier
        """

        year = pathId['year']
        doy = pathId['doy']
        frac = pathId['frac']

        exptime = 1.0 # XXX FIXME

        calib = item.getCalib()
        calib.setExptime(exptime)

        mjd = 51544.0 + int((year - 2000) * 365.25) + doy + frac/10**6 + exptime / 2.0
        obsMidpoint = dafBase.DateTime(mjd, dafBase.DateTime.MJD, dafBase.DateTime.UTC)
        calib.setMidTime(obsMidpoint)

    def std_raw(self, raw, dataId):
        # XXX Not really an efficient means of reading a sub-image
        ccd = dataId['ccd']
        x, y = ccd % 6, ccd // 6
        xSize, ySize = 2048, 4096
        bbox = afwGeom.Box2I(afwGeom.Point2I(x * xSize, y * ySize), afwGeom.ExtentI(xSize, ySize))
        ccdRaw = raw.Factory(raw, bbox, True)
        return ccdRaw
        
