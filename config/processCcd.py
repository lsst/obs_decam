"""
DECam-specific overrides for ProcessCcdTask
"""
import os.path

from lsst.utils import getPackageDir

obsConfigDir = os.path.join(getPackageDir('obs_decam'), 'config')

config.isr.load(os.path.join(obsConfigDir, 'isr.py'))
config.charImage.load(os.path.join(obsConfigDir, 'characterizeImage.py'))

# This sets the reference catalog name for Gen2.
for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     ):
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
    # Note the u-band results may not be useful without a color term
    refObjLoader.filterMap['u'] = 'g'
    refObjLoader.filterMap['Y'] = 'y'

# This sets up the reference catalog for Gen3.
config.calibrate.connections.astromRefCat = "ps1_pv3_3pi_20170110"
config.calibrate.connections.photoRefCat = "ps1_pv3_3pi_20170110"

config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"
# this was the default prior to DM-11521.  New default is 2000.
config.calibrate.deblend.maxFootprintSize = 0

# Set SIP order to 4, the Task default before RFC-577 to maintain same behavior
config.calibrate.astrometry.wcsFitter.order = 4
