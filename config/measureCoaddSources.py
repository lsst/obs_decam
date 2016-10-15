from lsst.meas.algorithms.loadIndexedReferenceObjects import LoadIndexedReferenceObjectsTask
config.match.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.match.refObjLoader.filterMap = {"g": "phot_g_mean_mag"}
