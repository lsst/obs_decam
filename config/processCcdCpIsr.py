"""
DECam-specific overrides for ProcessCcdTask/Community Pipeline products
"""
import os.path

obsConfigDir = os.path.dirname(__file__)

config.isr.load(os.path.join(obsConfigDir, 'isr.py'))
config.charImage.load(os.path.join(obsConfigDir, 'characterizeImage.py'))
config.calibrate.load(os.path.join(obsConfigDir, 'calibrate.py'))
