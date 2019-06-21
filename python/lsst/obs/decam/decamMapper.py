#
# LSST Data Management System
# Copyright 2012-2016 LSST Corporation.
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
import os
import re

import numpy as np

from lsst.utils import getPackageDir
from astro_metadata_translator import fix_header, DecamTranslator
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils
from lsst.afw.fits import readMetadata
from lsst.afw.geom import makeSkyWcs
from lsst.obs.base import CameraMapper
from lsst.daf.persistence import ButlerLocation, Storage, Policy
from .makeDecamRawVisitInfo import MakeDecamRawVisitInfo

np.seterr(divide="ignore")

__all__ = ["DecamMapper"]


class DecamMapper(CameraMapper):
    packageName = 'obs_decam'

    MakeRawVisitInfoClass = MakeDecamRawVisitInfo

    detectorNames = {
        1: 'S29', 2: 'S30', 3: 'S31', 4: 'S25', 5: 'S26', 6: 'S27', 7: 'S28', 8: 'S20', 9: 'S21',
        10: 'S22', 11: 'S23', 12: 'S24', 13: 'S14', 14: 'S15', 15: 'S16', 16: 'S17', 17: 'S18',
        18: 'S19', 19: 'S8', 20: 'S9', 21: 'S10', 22: 'S11', 23: 'S12', 24: 'S13', 25: 'S1', 26: 'S2',
        27: 'S3', 28: 'S4', 29: 'S5', 30: 'S6', 31: 'S7', 32: 'N1', 33: 'N2', 34: 'N3', 35: 'N4',
        36: 'N5', 37: 'N6', 38: 'N7', 39: 'N8', 40: 'N9', 41: 'N10', 42: 'N11', 43: 'N12', 44: 'N13',
        45: 'N14', 46: 'N15', 47: 'N16', 48: 'N17', 49: 'N18', 50: 'N19', 51: 'N20', 52: 'N21',
        53: 'N22', 54: 'N23', 55: 'N24', 56: 'N25', 57: 'N26', 58: 'N27', 59: 'N28', 60: 'N29',
        62: 'N31'}

    def __init__(self, inputPolicy=None, **kwargs):
        policyFile = Policy.defaultPolicyFile(self.packageName, "DecamMapper.yaml", "policy")
        policy = Policy(policyFile)

        super(DecamMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        # lambdaMin and lambda max are chosen to be where the filter rises above 1%
        # from http://www.ctio.noao.edu/noao/sites/default/files/DECam/DECam_filters_transmission.txt
        afwImageUtils.defineFilter('u', lambdaEff=350, lambdaMin=305, lambdaMax=403,
                                   alias=['u DECam c0006 3500.0 1000.0'])
        afwImageUtils.defineFilter('g', lambdaEff=450, lambdaMin=394, lambdaMax=555,
                                   alias=['g DECam SDSS c0001 4720.0 1520.0'])
        afwImageUtils.defineFilter('r', lambdaEff=600, lambdaMin=562, lambdaMax=725,
                                   alias=['r DECam SDSS c0002 6415.0 1480.0'])
        afwImageUtils.defineFilter('i', lambdaEff=750, lambdaMin=699, lambdaMax=870,
                                   alias=['i DECam SDSS c0003 7835.0 1470.0'])
        afwImageUtils.defineFilter('z', lambdaEff=900, lambdaMin=837, lambdaMax=1016,
                                   alias=['z DECam SDSS c0004 9260.0 1520.0'])
        afwImageUtils.defineFilter('y', lambdaEff=1000, lambdaMin=941, lambdaMax=1080,
                                   alias=['Y DECam c0005 10095.0 1130.0', 'Y'])
        afwImageUtils.defineFilter('VR', lambdaEff=630, lambdaMin=490, lambdaMax=765,
                                   alias=['VR DECam c0007 6300.0 2600.0'])
        afwImageUtils.defineFilter('N964', lambdaEff=964, alias=['N964 DECam c0008 9645.0 94.0'])
        afwImageUtils.defineFilter('SOLID', lambdaEff=0, alias=['solid'])

        # The data ID key ccdnum is not directly used in the current policy
        # template of the raw and instcal et al. datasets, so is not in its
        # keyDict automatically. Add it so the butler know about the data ID key
        # ccdnum.
        # Similarly, add "object" for raws.
        for datasetType in ("raw", "instcal", "dqmask", "wtmap", "cpIllumcor"):
            self.mappings[datasetType].keyDict.update({'ccdnum': int})
        self.mappings["raw"].keyDict.update({'object': str})

        # The number of bits allocated for fields in object IDs
        # TODO: This needs to be updated; also see Trac #2797
        DecamMapper._nbit_tract = 10
        DecamMapper._nbit_patch = 10
        DecamMapper._nbit_filter = 4
        DecamMapper._nbit_id = 64 - (DecamMapper._nbit_tract +
                                     2*DecamMapper._nbit_patch +
                                     DecamMapper._nbit_filter)

    def _extractDetectorName(self, dataId):
        copyId = self._transformId(dataId)
        try:
            return DecamMapper.detectorNames[copyId['ccdnum']]
        except KeyError:
            raise RuntimeError("No name found for dataId: %s"%(dataId))

    def _transformId(self, dataId):
        copyId = CameraMapper._transformId(self, dataId)
        if "ccd" in copyId:
            copyId.setdefault("ccdnum", copyId["ccd"])
        return copyId

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 32  # not really, but this leaves plenty of space for sources

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        Parameters
        ----------
        dataId : `dict`
            Data identifier with visit, ccd.

        Returns
        -------
        result : `int`
            Integer identifier for a CCD exposure.
        """
        copyId = self._transformId(dataId)
        visit = copyId['visit']
        ccdnum = copyId['ccdnum']
        return int("%07d%02d" % (visit, ccdnum))

    def _computeCoaddExposureId(self, dataId, singleFilter):
        """Compute the 64-bit (long) identifier for a coadd.

        Parameters
        ----------
        dataId : `dict`
            Data identifier with tract and patch.
        singleFilter : `bool`
            True means the desired ID is for a single-filter coadd,
            in which case the dataId must contain filter.

        Returns
        -------
        oid : `int`
            Unique integer identifier.
        """
        tract = int(dataId['tract'])
        if tract < 0 or tract >= 2**DecamMapper._nbit_tract:
            raise RuntimeError('tract not in range [0,%d)' % (2**DecamMapper._nbit_tract))
        patchX, patchY = [int(x) for x in dataId['patch'].split(',')]
        for p in (patchX, patchY):
            if p < 0 or p >= 2**DecamMapper._nbit_patch:
                raise RuntimeError('patch component not in range [0, %d)' % 2**DecamMapper._nbit_patch)
        oid = (((tract << DecamMapper._nbit_patch) + patchX) << DecamMapper._nbit_patch) + patchY
        if singleFilter:
            return (oid << DecamMapper._nbit_filter) + afwImage.Filter(dataId['filter']).getId()
        return oid

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, True)

    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        return 64 - DecamMapper._nbit_id

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, False)

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
        return 64 - DecamMapper._nbit_id

    def bypass_dcrCoaddId(self, datasetType, pythonType, location, dataId):
        return self.bypass_deepCoaddId(datasetType, pythonType, location, dataId)

    def bypass_dcrCoaddId_bits(self, *args, **kwargs):
        return self.bypass_deepCoaddId_bits(*args, **kwargs)

    def bypass_dcrMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self.bypass_deepMergedCoaddId(datasetType, pythonType, location, dataId)

    def bypass_dcrMergedCoaddId_bits(self, *args, **kwargs):
        return self.bypass_deepMergedCoaddId_bits(*args, **kwargs)

    def translate_dqmask(self, dqmask):
        # TODO: make a class member variable that knows the mappings
        # below instead of hard-coding them
        dqmArr = dqmask.getArray()
        mask = afwImage.Mask(dqmask.getDimensions())
        mArr = mask.getArray()
        idxBad = np.where(dqmArr & 1)
        idxSat = np.where(dqmArr & 2)
        idxIntrp = np.where(dqmArr & 4)
        idxCr = np.where(dqmArr & 16)
        idxBleed = np.where(dqmArr & 64)
        idxEdge = np.where(dqmArr & 512)
        mArr[idxBad] |= mask.getPlaneBitMask("BAD")
        mArr[idxSat] |= mask.getPlaneBitMask("SAT")
        mArr[idxIntrp] |= mask.getPlaneBitMask("INTRP")
        mArr[idxCr] |= mask.getPlaneBitMask("CR")
        mArr[idxBleed] |= mask.getPlaneBitMask("SAT")
        mArr[idxEdge] |= mask.getPlaneBitMask("EDGE")
        return mask

    def translate_wtmap(self, wtmap):
        wtmArr = wtmap.getArray()
        idxUndefWeight = np.where(wtmArr <= 0)
        # Reassign weights to be finite but small:
        wtmArr[idxUndefWeight] = min(1e-14, np.min(wtmArr[np.where(wtmArr > 0)]))
        var = 1.0 / wtmArr
        varim = afwImage.ImageF(var)
        return varim

    def bypass_instcal(self, datasetType, pythonType, butlerLocation, dataId):
        # Workaround until I can access the butler
        instcalMap = self.map_instcal(dataId)
        dqmaskMap = self.map_dqmask(dataId)
        wtmapMap = self.map_wtmap(dataId)
        instcalType = getattr(afwImage, instcalMap.getPythonType().split(".")[-1])
        dqmaskType = getattr(afwImage, dqmaskMap.getPythonType().split(".")[-1])
        wtmapType = getattr(afwImage, wtmapMap.getPythonType().split(".")[-1])
        instcal = instcalType(instcalMap.getLocationsWithRoot()[0])
        dqmask = dqmaskType(dqmaskMap.getLocationsWithRoot()[0])
        wtmap = wtmapType(wtmapMap.getLocationsWithRoot()[0])

        mask = self.translate_dqmask(dqmask)
        variance = self.translate_wtmap(wtmap)

        mi = afwImage.MaskedImageF(afwImage.ImageF(instcal.getImage()), mask, variance)
        md = readMetadata(instcalMap.getLocationsWithRoot()[0])
        fix_header(md, translator_class=DecamTranslator)
        wcs = makeSkyWcs(md, strip=True)
        exp = afwImage.ExposureF(mi, wcs)

        exp.setPhotoCalib(afwImage.makePhotoCalibFromCalibZeroPoint(10**(0.4 * md.getScalar("MAGZERO")), 0))
        visitInfo = self.makeRawVisitInfo(md=md)
        exp.getInfo().setVisitInfo(visitInfo)

        for kw in ('LTV1', 'LTV2'):
            md.remove(kw)

        exp.setMetadata(md)
        return exp

    def std_raw(self, item, dataId):
        """Standardize a raw dataset by converting it to an Exposure.

        Raw images are MEF files with one HDU for each detector.

        Parameters
        ----------
        item : `lsst.afw.image.DecoratedImage`
            The image read by the butler.
        dataId : data ID
            Data identifier.

        Returns
        -------
        result : `lsst.afw.image.Exposure`
            The standardized Exposure.
        """
        return self._standardizeExposure(self.exposures['raw'], item, dataId,
                                         trimmed=False)

    def std_dark(self, item, dataId):
        exp = afwImage.makeExposure(afwImage.makeMaskedImage(item))
        rawPath = self.map_raw(dataId).getLocations()[0]
        headerPath = re.sub(r'[\[](\d+)[\]]$', "[0]", rawPath)
        md0 = readMetadata(headerPath)
        fix_header(md0, translator_class=DecamTranslator)
        visitInfo = self.makeRawVisitInfo(md0)
        exp.getInfo().setVisitInfo(visitInfo)
        return self._standardizeExposure(self.calibrations["dark"], exp, dataId, filter=False)

    def std_bias(self, item, dataId):
        exp = afwImage.makeExposure(afwImage.makeMaskedImage(item))
        return self._standardizeExposure(self.calibrations["bias"], exp, dataId, filter=False)

    def std_flat(self, item, dataId):
        exp = afwImage.makeExposure(afwImage.makeMaskedImage(item))
        return self._standardizeExposure(self.calibrations["flat"], exp, dataId, filter=True)

    def std_illumcor(self, item, dataId):
        exp = afwImage.makeExposure(afwImage.makeMaskedImage(item))
        return self._standardizeExposure(self.calibrations["illumcor"], exp, dataId, filter=True)

    def _standardizeCpMasterCal(self, datasetType, item, dataId, setFilter=False):
        """Standardize a MasterCal image obtained from NOAO archive into Exposure

        These MasterCal images are MEF files with one HDU for each detector.
        Some WCS header, eg CTYPE1, exists only in the zeroth extensionr,
        so info in the zeroth header need to be copied over to metadata.

        Parameters
        ----------
        datasetType : `str`
            Dataset type ("bias", "flat", or "illumcor").
        item : `lsst.afw.image.DecoratedImage`
            The image read by the butler.
        dataId : data ID
            Data identifier.
        setFilter : `bool`
            Whether to set the filter in the Exposure.

        Returns
        -------
        result : `lsst.afw.image.Exposure`
            The standardized Exposure.
        """
        mi = afwImage.makeMaskedImage(item.getImage())
        md = item.getMetadata()
        masterCalMap = getattr(self, "map_" + datasetType)
        masterCalPath = masterCalMap(dataId).getLocationsWithRoot()[0]
        headerPath = re.sub(r'[\[](\d+)[\]]$', "[0]", masterCalPath)
        md0 = readMetadata(headerPath)
        fix_header(md0, translator_class=DecamTranslator)
        for kw in ('CTYPE1', 'CTYPE2', 'CRVAL1', 'CRVAL2', 'CUNIT1', 'CUNIT2',
                   'CD1_1', 'CD1_2', 'CD2_1', 'CD2_2'):
            if kw in md0.paramNames() and kw not in md.paramNames():
                md.add(kw, md0.getScalar(kw))
        wcs = makeSkyWcs(md, strip=True)
        exp = afwImage.makeExposure(mi, wcs)
        exp.setMetadata(md)
        return self._standardizeExposure(self.calibrations[datasetType], exp, dataId, filter=setFilter)

    def std_cpBias(self, item, dataId):
        return self._standardizeCpMasterCal("cpBias", item, dataId, setFilter=False)

    def std_cpFlat(self, item, dataId):
        return self._standardizeCpMasterCal("cpFlat", item, dataId, setFilter=True)

    def std_fringe(self, item, dataId):
        exp = afwImage.makeExposure(afwImage.makeMaskedImage(item))
        return self._standardizeExposure(self.calibrations["fringe"], exp, dataId)

    def std_cpIllumcor(self, item, dataId):
        return self._standardizeCpMasterCal("cpIllumcor", item, dataId, setFilter=True)

    @classmethod
    def getLinearizerDir(cls):
        """Directory containing linearizers"""
        packageName = cls.getPackageName()
        packageDir = getPackageDir(packageName)
        return os.path.join(packageDir, "decam", "linearizer")

    def map_linearizer(self, dataId, write=False):
        """Map a linearizer"""
        actualId = self._transformId(dataId)
        location = "%02d.fits" % (dataId["ccdnum"])
        return ButlerLocation(
            pythonType="lsst.ip.isr.LinearizeSquared",
            cppType="Config",
            storageName="PickleStorage",
            locationList=[location],
            dataId=actualId,
            mapper=self,
            storage=Storage.makeFromURI(self.getLinearizerDir())
        )
