"""
DECam-specific overrides for ProcessCcdTask/Community Pipeline products
"""
import os.path
import warnings

obsConfigDir = os.path.dirname(__file__)

config.load(os.path.join(obsConfigDir, 'processCcd.py'))

warnings.warn(
    'processCcdCpIsr.py is no longer needed, use processCcd.py instead. Will '
    'be removed after release 21.0',
    category=FutureWarning)
