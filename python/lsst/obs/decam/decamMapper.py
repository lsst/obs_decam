#!/usr/bin/env python

import os
import pwd

import lsst.daf.base as dafBase
import lsst.afw.geom as afwGeom
import lsst.afw.coord as afwCoord
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils

from lsst.daf.butlerUtils import CameraMapper, exposureFromImage
import lsst.pex.policy as pexPolicy

class DecamMapper(CameraMapper):
    def __init__(self, outputRoot=None, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile("obs_decam", "DecamMapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)
        super(DecamMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)

        afwImageUtils.defineFilter('u', lambdaEff=350)
        afwImageUtils.defineFilter('g', lambdaEff=450)
        afwImageUtils.defineFilter('r', lambdaEff=600)
        afwImageUtils.defineFilter('i', lambdaEff=750)
        afwImageUtils.defineFilter('z', lambdaEff=900)
        afwImageUtils.defineFilter('y', lambdaEff=1000, alias='Y') # Urgh!

    def _extractDetectorName(self, dataId):
        ccd = dataId['ccd']
        side = dataId['side'].upper()
        return "%s%d" % (side, ccd)

    def _defectLookup(self, dataId, ccdSerial):
        """Find the defects for a given CCD.
        @param dataId (dict) Dataset identifier
        @param ccdSerial (string) CCD serial number
        @return (string) path to the defects file or None if not available
        """
        return None # XXX FIXME

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = pathId['ccd']
        side = pathId['side']
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

    def std_raw(self, image, dataId):
        """Pull out WCS header keywords wcslib doesn't understand"""
        md = image.getMetadata()

        def remove(md, key):
            if md.exists(key):
                md.remove(key)

        remove(md, 'CTYPE1')
        remove(md, 'CTYPE2')
        remove(md, 'RADESYS')
        remove(md, 'EQUINOX')
        remove(md, 'CUNIT1')
        remove(md, 'CUNIT2')

        return super(DecamMapper, self).std_raw(image, dataId)
