# Config override for lsst.ap.pipe.ApPipeTask
import os.path

decamConfigDir = os.path.dirname(__file__)

config.ccdProcessor.load(os.path.join(decamConfigDir, "processCcd.py"))
