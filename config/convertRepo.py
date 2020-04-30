# Config overrides for converting gen2 to gen3 repos.

import lsst.obs.decam

# Use the specialized Decam ingest task to handle multi-HDU FITS files.
config.raws.retarget(lsst.obs.decam.DecamRawIngestTask)

# Override the instrument class name in the configuration.  We probably got
# here from the command-line script, which sets this anyway, but it's better to
# set it twice than set it never.
config.instrument = "lsst.obs.decam.DarkEnergyCamera"

# DECam names its detectors differently in the registry
config.ccdKey = "ccdnum"

# Community Pipeline-produced calibrations are all Images.
config.storageClasses['cpBias'] = "ExposureF"
config.storageClasses['cpFlat'] = "ExposureF"
config.storageClasses['cpIllumcor'] = "ExposureF"

# And define the specialist formatter
config.formatterClasses['cpBias'] = "lsst.obs.decam.DarkEnergyCameraCPCalibFormatter"
config.formatterClasses['cpFlat'] = "lsst.obs.decam.DarkEnergyCameraCPCalibFormatter"

# and multi extension fits handler
config.targetHandlerClasses['cpFlat'] = "lsst.obs.base.gen2to3.repoWalker.handlers.MultiExtensionFileHandler"
config.targetHandlerClasses['cpBias'] = "lsst.obs.base.gen2to3.repoWalker.handlers.MultiExtensionFileHandler"
