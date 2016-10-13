from lsst.obs.decam.decamCpIsr import DecamCpIsrTask
config.processCcd.isr.retarget(DecamCpIsrTask)
from lsst.meas.algorithms.loadIndexedReferenceObjects import LoadIndexedReferenceObjectsTask
config.processCcd.calibrate.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.processCcd.calibrate.refObjLoader.filterMap = {"g": "phot_g_mean_mag", "i": "phot_g_mean_mag", "Y": "phot_g_mean_mag", "r": "phot_g_mean_mag", "z": "phot_g_mean_mag"}


config.processCcd.isr.doDark = False
config.processCcd.isr.fringe.filters=['z', 'y']
config.processCcd.isr.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                       'TRIMSECA', 'TRIMSECB',
                                       'BIASSECA', 'BIASSECB',
                                       'PRESECA', 'PRESECB',
                                       'POSTSECA', 'POSTSECB']

config.processCcd.charImage.repair.cosmicray.nCrPixelMax = 100000
config.processCcd.isr.assembleCcd.setGain=False
