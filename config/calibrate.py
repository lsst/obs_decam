"""
DECam-specific overrides for CalibrateTask
"""

# This sets the reference catalog name for Gen2.
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
    # Note the u-band results may not be useful without a color term
    refObjLoader.filterMap['u'] = 'g'
    refObjLoader.filterMap['Y'] = 'y'

# This sets up the reference catalog for Gen3.
config.connections.astromRefCat = "ps1_pv3_3pi_20170110"
config.connections.photoRefCat = "ps1_pv3_3pi_20170110"
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

# this was the default prior to DM-11521.  New default is 2000.
config.deblend.maxFootprintSize = 0

# Set SIP order to 4, the Task default before RFC-577 to maintain same behavior
config.astrometry.wcsFitter.order = 4
