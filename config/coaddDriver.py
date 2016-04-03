# Load from sub-configurations
import os.path

from lsst.utils import getPackageDir

for sub in ("makeCoaddTempExp", "backgroundReference", "assembleCoadd", "detectCoaddSources"):
    path = os.path.join(getPackageDir("obs_decam"), "config", sub + ".py")
    if os.path.exists(path):
        getattr(config, sub).load(path)
