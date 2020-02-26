"""
DECam-specific overrides for ProcessCcdTask
"""
import os.path

from lsst.utils import getPackageDir

obsConfigDir = os.path.join(getPackageDir('obs_decam'), 'config')

config.isr.load(os.path.join(obsConfigDir, 'isr.py'))
config.charImage.load(os.path.join(obsConfigDir, 'characterizeImage.py'))
config.calibrate.load(os.path.join(obsConfigDir, 'calibrate.py'))
