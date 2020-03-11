# Config overrides for converting gen2 to gen3 repos.

from lsst.obs.base.gen2to3 import Translator, AbstractToPhysicalFilterKeyHandler
import lsst.obs.decam

# Use the specialized Decam ingest task to handle multi-HDU FITS files.
config.raws.retarget(lsst.obs.decam.DecamRawIngestTask)

# DECam names its detectors differently in the registry
config.ccdKey = "ccdnum"

# Community Pipeline-produced calibrations are all Images.
config.storageClasses['cpBias'] = "ExposureF"
config.storageClasses['cpFlat'] = "ExposureF"
config.storageClasses['cpIllumcor'] = "ExposureF"

# DECam calibRegistry entries are abstract_filters, but we need physical_filter
# in the gen3 registry.
Translator.addRule(AbstractToPhysicalFilterKeyHandler(lsst.obs.decam.DarkEnergyCamera.filterDefinitions),
                   instrument=lsst.obs.decam.DarkEnergyCamera.getName(),
                   gen2keys=("filter",),
                   consume=("filter",),
                   datasetTypeName="cpFlat")
