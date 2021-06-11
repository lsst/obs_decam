"""
DECam-specific overrides for CalibrateTask
"""
import os.path

obsConfigDir = os.path.join(os.path.dirname(__file__))

# This sets the reference catalog name for Gen2.
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
    # Note the u-band results may not be useful without a color term
    refObjLoader.filterMap['u'] = 'g'
    refObjLoader.filterMap['Y'] = 'y'
    refObjLoader.filterMap['N708'] = 'i'

# This sets up the reference catalog for Gen3.
config.connections.astromRefCat = "ps1_pv3_3pi_20170110"
config.connections.photoRefCat = "ps1_pv3_3pi_20170110"
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

# The Task default was reduced from 4 to 2 on RFC-577. We believe that 4 is
# more appropriate for use with DECam data until a Jointcal-derived distortion
# model is available (DM-24431); at that point, this override should likely be
# removed.
# See Slack: https://lsstc.slack.com/archives/C2B6X08LS/p1586468459084600
config.astrometry.wcsFitter.order = 4

config.measurement.load(os.path.join(obsConfigDir, "hsm.py"))
