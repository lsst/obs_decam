import os.path

config.load(os.path.join(os.path.dirname(__file__), "srcSchemaMap.py"))
config.load(os.path.join(os.path.dirname(__file__), "extinctionCoeffs.py"))
from lsst.obs.decam.decamFilters import DECAM_FILTER_DEFINITIONS
config.physicalToBandFilterMap = DECAM_FILTER_DEFINITIONS.physical_to_band