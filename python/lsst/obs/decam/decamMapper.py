#
# LSST Data Management System
# Copyright 2012-2015 LSST Corporation.
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
import re
import numpy as np
import lsst.afw.detection as afwDetection
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils
from lsst.daf.butlerUtils import CameraMapper, exposureFromImage
from lsst.ip.isr import isr
import lsst.pex.policy as pexPolicy

np.seterr(divide="ignore")

class DecamMapper(CameraMapper):
    packageName = 'obs_decam'

    def __init__(self, inputPolicy=None, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile(self.packageName, "DecamMapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)

        super(DecamMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)

        afwImageUtils.defineFilter('u', lambdaEff=350, alias=['u DECam c0006 3500.0 1000.0'])
        afwImageUtils.defineFilter('g', lambdaEff=450, alias=['g DECam SDSS c0001 4720.0 1520.0'])
        afwImageUtils.defineFilter('r', lambdaEff=600, alias=['r DECam SDSS c0002 6415.0 1480.0'])
        afwImageUtils.defineFilter('i', lambdaEff=750, alias=['i DECam SDSS c0003 7835.0 1470.0'])
        afwImageUtils.defineFilter('z', lambdaEff=900, alias=['z DECam SDSS c0004 9260.0 1520.0'])
        afwImageUtils.defineFilter('y', lambdaEff=1000, alias=['Y DECam c0005 10095.0 1130.0'])

        # The data ID key ccdnum is not directly used in the current policy
        # template of the raw dataset, so is not in its keyDict automatically.
        # Add it so raw dataset know about the data ID key ccdnum.
        self.mappings["raw"].keyDict.update({'ccdnum': int})

        # The number of bits allocated for fields in object IDs
        # TODO: This needs to be updated; also see Trac #2797
        DecamMapper._nbit_tract = 10
        DecamMapper._nbit_patch = 10
        DecamMapper._nbit_filter = 4
        DecamMapper._nbit_id = 64 - (DecamMapper._nbit_tract +
                                     2*DecamMapper._nbit_patch +
                                     DecamMapper._nbit_filter)

    def _extractDetectorName(self, dataId):
        nameTuple = self.registry.executeQuery(['side','ccd'], ['raw',], [('ccdnum','?'), ('visit','?')],
                                               None, (dataId['ccdnum'], dataId['visit']))
        if len(nameTuple) > 1:
            raise RuntimeError("More than one name returned")
        if len(nameTuple) == 0:
            raise RuntimeError("No name found for dataId: %s"%(dataId))
        return "%s%i" % (nameTuple[0][0], nameTuple[0][1])

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCcdExposureId(dataId)
    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 32 # not really, but this leaves plenty of space for sources
    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        visit = dataId['visit']
        ccdnum = dataId['ccdnum']
        return int("%07d%02d" % (visit, ccdnum))

    def _computeCoaddExposureId(self, dataId, singleFilter):
        """Compute the 64-bit (long) identifier for a coadd.

        @param dataId (dict)       Data identifier with tract and patch.
        @param singleFilter (bool) True means the desired ID is for a single-
                                   filter coadd, in which case dataId
                                   must contain filter.
        """
        tract = long(dataId['tract'])
        if tract < 0 or tract >= 2**DecamMapper._nbit_tract:
            raise RuntimeError('tract not in range [0,%d)' % (2**DecamMapper._nbit_tract))
        patchX, patchY = map(int, dataId['patch'].split(','))
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

    def translate_dqmask(self, dqmask):
        # TODO: make a class member variable that knows the mappings
        # below instead of hard-coding them
        dqmArr    = dqmask.getArray()
        mask      = afwImage.MaskU(dqmask.getDimensions())
        mArr      = mask.getArray()
        idxBad    = np.where(dqmArr & 1)
        idxSat    = np.where(dqmArr & 2)
        idxIntrp  = np.where(dqmArr & 4)
        idxCr     = np.where(dqmArr & 16)
        idxBleed  = np.where(dqmArr & 64)
        idxEdge   = np.where(dqmArr & 512)
        mArr[idxBad]   |= mask.getPlaneBitMask("BAD")
        mArr[idxSat]   |= mask.getPlaneBitMask("SAT")
        mArr[idxIntrp] |= mask.getPlaneBitMask("INTRP")
        mArr[idxCr]    |= mask.getPlaneBitMask("CR")
        mArr[idxBleed] |= mask.getPlaneBitMask("SAT")
        mArr[idxEdge] |= mask.getPlaneBitMask("EDGE")
        return mask

    def translate_wtmap(self, wtmap):
        wtmArr = wtmap.getArray()
        idxUndefWeight = np.where(wtmArr <= 0)
        #Reassign weights to be finite but small:
        wtmArr[idxUndefWeight] = min(1e-14, np.min(wtmArr[np.where(wtmArr>0)]))
        var   = 1.0 / wtmArr
        varim = afwImage.ImageF(var)
        return varim
        
    def bypass_instcal(self, datasetType, pythonType, butlerLocation, dataId):
        # Workaround until I can access the butler
        instcalMap  = self.map_instcal(dataId)
        dqmaskMap   = self.map_dqmask(dataId)
        wtmapMap    = self.map_wtmap(dataId)
        instcalType = getattr(afwImage, instcalMap.getPythonType().split(".")[-1])
        dqmaskType  = getattr(afwImage, dqmaskMap.getPythonType().split(".")[-1])
        wtmapType   = getattr(afwImage, wtmapMap.getPythonType().split(".")[-1])
        instcal     = instcalType(instcalMap.getLocations()[0])
        dqmask      = dqmaskType(dqmaskMap.getLocations()[0])
        wtmap       = wtmapType(wtmapMap.getLocations()[0])

        mask        = self.translate_dqmask(dqmask)
        variance    = self.translate_wtmap(wtmap)

	mi          = afwImage.MaskedImageF(afwImage.ImageF(instcal.getImage()), mask, variance)
	md          = instcal.getMetadata()
	wcs         = afwImage.makeWcs(md)
	exp         = afwImage.ExposureF(mi, wcs)

        # Set the calib by hand; need to grab the zeroth extension
        header = re.sub(r'[\[](\d+)[\]]$', "[0]", instcalMap.getLocations()[0])
        md0 = afwImage.readMetadata(header)
        calib = afwImage.Calib()
        calib.setExptime(md0.get("EXPTIME"))
        calib.setFluxMag0(10**(0.4 * md0.get("MAGZERO")))
        exp.setCalib(calib)
        
        exp.setMetadata(md) # Do we need to remove WCS/calib info?
        return exp

    def std_raw(self, item, dataId):
        """Standardize a raw dataset by converting it to an Exposure.

        Raw images are MEF files with one HDU for each detector.
        Some useful header keywords, such as EXPTIME and MJD-OBS,
        exist only in the zeroth extensionr.  Here information in
        the zeroth header are copied to metadata.

        @param item: The image read by the butler
        @param dataId: Data identifier
        @return (lsst.afw.image.Exposure) the standardized Exposure
        """
        exp = exposureFromImage(item)
        md = exp.getMetadata()
        rawPath = self.map_raw(dataId).getLocations()[0]
        headerPath = re.sub(r'[\[](\d+)[\]]$', "[0]", rawPath)
        md0 = afwImage.readMetadata(headerPath)
        for kw in md0.paramNames():
            if kw not in md.paramNames():
                md.add(kw, md0.get(kw))
        return self._standardizeExposure(self.exposures['raw'], exp, dataId,
                                         trimmed=False)

    def _standardizeMasterCal(self, datasetType, item, dataId, setFilter=False):
        """Standardize a MasterCal image obtained from NOAO archive into Exposure

        These MasterCal images are MEF files with one HDU for each detector.
        Some WCS header, eg CTYPE1, exists only in the zeroth extensionr,
        so info in the zeroth header need to be copied over to metadata.

        @param datasetType: Dataset type ("bias" or "flat")
        @param item: The image read by the butler
        @param dataId: Data identifier
        @param setFilter: Whether to set the filter in the Exposure
        @return (lsst.afw.image.Exposure) the standardized Exposure
        """
        mi = afwImage.makeMaskedImage(item.getImage())
        md = item.getMetadata()
        masterCalMap = getattr(self, "map_" + datasetType)
        masterCalPath = masterCalMap(dataId).getLocations()[0]
        headerPath = re.sub(r'[\[](\d+)[\]]$', "[0]", masterCalPath)
        md0 = afwImage.readMetadata(headerPath)
        for kw in md0.paramNames():
            if kw not in md.paramNames():
                md.add(kw, md0.get(kw))
        wcs = afwImage.makeWcs(md, True)
        exp = afwImage.makeExposure(mi, wcs)
        exp.setMetadata(md)
        return self._standardizeExposure(self.calibrations[datasetType], exp, dataId, filter=setFilter)

    def std_bias(self, item, dataId):
        return self._standardizeMasterCal("bias", item, dataId, setFilter=False)

    def std_flat(self, item, dataId):
        return self._standardizeMasterCal("flat", item, dataId, setFilter=True)

    def std_fringe(self, item, dataId):
        exp = afwImage.makeExposure(afwImage.makeMaskedImage(item))
        return self._standardizeExposure(self.calibrations["fringe"], exp, dataId)

    def map_defects(self, dataId, write=False):
        """Map defects dataset with the calibration registry.

        Overriding the method so to use CalibrationMapping policy,
        instead of looking up the path in defectRegistry as currently
        implemented in CameraMapper.

        @param dataId (dict) Dataset identifier
        @return daf.persistence.ButlerLocation
        """
        return self.mappings["defects"].map(self, dataId=dataId, write=write)

    def bypass_defects(self, datasetType, pythonType, butlerLocation, dataId):
        """Return a defect list based on butlerLocation returned by map_defects.

        Use all nonzero pixels in the Community Pipeline Bad Pixel Masks.

        @param[in] butlerLocation: Butler Location with path to defects FITS
        @param[in] dataId: data identifier
        @return meas.algorithms.DefectListT
        """
        bpmFitsPath = butlerLocation.locationList[0]
        bpmImg = afwImage.ImageU(bpmFitsPath)
        bpmArr = bpmImg.getArray()
        idxBad = np.nonzero(bpmArr)
        workImg = afwImage.ImageU(bpmImg.getDimensions())
        workImg.getArray()[idxBad] = 1
        ds = afwDetection.FootprintSet(workImg, afwDetection.Threshold(0.5))
        fpList = ds.getFootprints()
        return isr.defectListFromFootprintList(fpList, growFootprints=0)

    def std_defects(self, item, dataId):
        """Return the defect list as it is.

        Do not standardize it to Exposure.
        """
        return item
