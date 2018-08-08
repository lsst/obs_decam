"""
DECam-specific overrides of IsrTask
"""
from lsst.obs.decam.crosstalk import DecamCrosstalkTask
config.crosstalk.retarget(DecamCrosstalkTask)

config.doCrosstalk = True
config.doDark = False
config.doAddDistortionModel = False  # rely on the TPV terms instead
config.fringe.filters = ['z', 'y']
config.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                   'TRIMSECA', 'TRIMSECB',
                                   'BIASSECA', 'BIASSECB',
                                   'PRESECA', 'PRESECB',
                                   'POSTSECA', 'POSTSECB']
