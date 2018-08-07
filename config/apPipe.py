# Config override for lsst.ap.pipe.ApPipeTask
import os.path
from lsst.utils import getPackageDir

decamConfigDir = os.path.join(getPackageDir('obs_decam'), 'config')

config.ccdProcessor.load(os.path.join(decamConfigDir, "processCcd.py"))
config.associator.load(os.path.join(decamConfigDir, "association.py"))

