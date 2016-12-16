import os

from lsst.utils import getPackageDir

config.processCcd.load(os.path.join(getPackageDir("obs_decam"), "config", "processCcdCpIsr.py"))
config.ccdKey = 'ccdnum'

config.processCcd.isr.doFringe=False
