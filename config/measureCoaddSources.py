from lsst.meas.algorithms.loadIndexedReferenceObjects import LoadIndexedReferenceObjectsTask
config.match.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.match.refObjLoader.filterMap = {"g": "phot_g_mean_mag", "i": "phot_g_mean_mag", "Y": "phot_g_mean_mag", "r": "phot_g_mean_mag", "z": "phot_g_mean_mag"}
