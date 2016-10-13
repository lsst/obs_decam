from lsst.obs.decam.decamCpIsr import DecamCpIsrTask
config.isr.retarget(DecamCpIsrTask)

from lsst.meas.algorithms.loadIndexedReferenceObjects import LoadIndexedReferenceObjectsTask
config.calibrate.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.refObjLoader.filterMap = {"g": "phot_g_mean_mag", "i": "phot_g_mean_mag", "Y": "phot_g_mean_mag", "r": "phot_g_mean_mag", "z": "phot_g_mean_mag"}

config.isr.doDark = False
config.isr.fringe.filters=['z', 'y']
config.isr.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                       'TRIMSECA', 'TRIMSECB',
                                       'BIASSECA', 'BIASSECB',
                                       'PRESECA', 'PRESECB',
                                       'POSTSECA', 'POSTSECB']

config.charImage.repair.cosmicray.nCrPixelMax = 100000
