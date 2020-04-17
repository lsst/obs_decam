"""
DECam-specific overrides for RunIsrTask/Community Pipeline products
"""
import os.path

obsConfigDir = os.path.join(os.path.dirname(__file__))

config.isr.load(os.path.join(obsConfigDir, "isr.py"))
