"""
DECam-specific overrides for VisitAnalysisTask
"""
import os.path

from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

# Reference catalog
config.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
# config.colorterms.load(os.path.join(getPackageDir("obs_decam"), "config", "colorterms.py"))

config.doApplyColorTerms=False
config.doWriteParquetTables=False
config.doApplyExternalPhotoCalib=False
config.doApplyExternalSkyWcs=False
config.refObjLoader.filterMap={'u': 'g'}
