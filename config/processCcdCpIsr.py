import os.path

from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
from lsst.obs.decam.decamCpIsr import DecamCpIsrTask
config.isr.retarget(DecamCpIsrTask)

decamConfigDir = os.path.join(getPackageDir('obs_decam'), 'config')
config.isr.load(os.path.join(decamConfigDir, 'isr.py'))

config.charImage.repair.cosmicray.nCrPixelMax = 100000

for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     config.charImage.refObjLoader,
                     ):
    refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
    # Note the u-band results may not be useful without a color term
    refObjLoader.filterMap['u'] = 'g'
    refObjLoader.filterMap['Y'] = 'y'

config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"
