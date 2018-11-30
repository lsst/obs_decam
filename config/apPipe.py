# Config override for lsst.ap.pipe.ApPipeTask
import os.path
from lsst.utils import getPackageDir

decamConfigDir = os.path.join(getPackageDir('obs_decam'), 'config')

# This default processCcd config assumes calibration products are from the
# DECam Community Pipeline (CP). The config file to use for stack-built
# calibs is "processCcd.py" instead.
config.ccdProcessor.load(os.path.join(decamConfigDir, "processCcdCpIsr.py"))
