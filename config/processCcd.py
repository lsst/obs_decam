from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
from lsst.obs.decam.isr import DecamIsrTask
config.isr.retarget(DecamIsrTask)

config.isr.doDark = False
config.isr.fringe.filters = ['z', 'y']
config.isr.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                       'TRIMSECA', 'TRIMSECB',
                                       'BIASSECA', 'BIASSECB',
                                       'PRESECA', 'PRESECB',
                                       'POSTSECA', 'POSTSECB']

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
