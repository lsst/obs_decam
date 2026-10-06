"""
DECam-specific overrides for CalibrateTask
"""
from lsst.meas.algorithms import ColorLimit

config.photoRefObjLoader.load("filterMap.py")

# Photometric calibration: use color terms
config.photoCal.applyColorTerms = True
colors = config.photoCal.match.referenceSelection.colorLimits
# The following two color limits are adopted from obs_subaru for the HSC
# SSP survey.
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
config.photoCal.match.referenceSelection.doMagLimit = True
config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
config.photoCal.match.referenceSelection.magLimit.maximum = 22.0
config.photoCal.colorterms.load("colorterms.py")

# The Task default was reduced from 4 to 2 on RFC-577. We believe that 4 is
# more appropriate for use with DECam data until a Jointcal-derived distortion
# model is available (DM-24431); at that point, this override should likely be
# removed.
# See Slack: https://lsstc.slack.com/archives/C2B6X08LS/p1586468459084600
config.astrometry.wcsFitter.order = 4

config.measurement.load("apertures.py")
config.measurement.load("kron.py")
config.measurement.load("hsm.py")

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.263
