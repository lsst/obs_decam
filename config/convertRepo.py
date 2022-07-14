# Config overrides for converting gen2 to gen3 repos.

# DECam names its detectors differently in the registry
config.ccdKey = "ccdnum"

# Community Pipeline-produced calibrations are all Images.
config.storageClasses['cpBias'] = "ExposureF"
config.storageClasses['cpFlat'] = "ExposureF"
config.storageClasses['cpIllumcor'] = "ExposureF"
config.storageClasses['fringe'] = "ExposureF"

# And define the specialist formatter
config.formatterClasses['cpBias'] = "lsst.obs.decam.DarkEnergyCameraCPCalibFormatter"
config.formatterClasses['cpFlat'] = "lsst.obs.decam.DarkEnergyCameraCPCalibFormatter"

# and multi extension fits handler
config.targetHandlerClasses['cpFlat'] = "lsst.obs.base.gen2to3.repoWalker.handlers.MultiExtensionFileHandler"
config.targetHandlerClasses['cpBias'] = "lsst.obs.base.gen2to3.repoWalker.handlers.MultiExtensionFileHandler"
