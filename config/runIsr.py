"""
DECam-specific overrides for RunIsrTask
"""
import os.path

from lsst.utils import getPackageDir
from lsst.obs.decam.isr import DecamIsrTask

obsConfigDir = os.path.join(getPackageDir("obs_decam"), "config")

config.isr.retarget(DecamIsrTask)
config.isr.load(os.path.join(obsConfigDir, "isr.py"))
