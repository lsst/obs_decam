"""
DECam-specific overrides for CalibrateTask
"""

# Testing DM-30994 with crowded Bulge Saha data

import os.path

from lsst.meas.algorithms import ColorLimit

config_dir = os.path.dirname(__file__)

# Overrides to improved astrometry matching.
config.astrometry.doFiducialZeroPointCull = True
config.astrometry.load(os.path.join(config_dir, "fiducialZeroPoint.py"))

# Use PS1 for both astrometry and photometry.
config.connections.astrometry_ref_cat = "ps1_pv3_3pi_20170110"
config.astrometry_ref_loader.load(os.path.join(config_dir, "filterMap.py"))
# Use the filterMap instead of the "any" filter (as is used for Gaia).
config.astrometry_ref_loader.anyFilterMapsToThis = None
config.photometry_ref_loader.load(os.path.join(config_dir, "filterMap.py"))

# Use colorterms for photometric calibration, with color limits on the refcat.
config.photometry.applyColorTerms = True
config.photometry.photoCatName = "ps1_pv3_3pi_20170110"
colors = config.photometry.match.referenceSelection.colorLimits
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
config.photometry.colorterms.load(os.path.join(config_dir, "colorterms.py"))

# import os.path

# from lsst.meas.algorithms import ColorLimit

# obsConfigDir = os.path.join(os.path.dirname(__file__))

# config.photoRefObjLoader.load(os.path.join(obsConfigDir, "filterMap.py"))

# # Photometric calibration: use color terms
# config.photoCal.applyColorTerms = True
# colors = config.photoCal.match.referenceSelection.colorLimits
# # The following two color limits are adopted from obs_subaru for the HSC
# # SSP survey.
# colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
# colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
# config.photoCal.match.referenceSelection.doMagLimit = True
# config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
# config.photoCal.match.referenceSelection.magLimit.maximum = 22.0
# config.photoCal.colorterms.load(os.path.join(obsConfigDir, "colorterms.py"))

# The Task default was reduced from 4 to 2 on RFC-577. We believe that 4 is
# more appropriate for use with DECam data until a Jointcal-derived distortion
# model is available (DM-24431); at that point, this override should likely be
# removed.
# See Slack: https://lsstc.slack.com/archives/C2B6X08LS/p1586468459084600
config.astrometry.wcsFitter.order = 4

config.measurement.load(os.path.join(obsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(obsConfigDir, "kron.py"))
config.measurement.load(os.path.join(obsConfigDir, "hsm.py"))

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.263
