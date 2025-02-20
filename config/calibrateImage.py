import os.path

from lsst.meas.algorithms import ColorLimit

config_dir = os.path.dirname(__file__)

# Astrometry
config.astrometry_ref_loader.anyFilterMapsToThis = "phot_g_mean"

# Photometry
config.photometry_ref_loader.load(os.path.join(config_dir, "filterMap.py"))

# Use colorterms for photometric calibration, with color limits on the refcat
config.photometry.applyColorTerms = True
config.photometry.photoCatName = "ps1_pv3_3pi_20170110"
colors = config.photometry.match.referenceSelection.colorLimits
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
config.photometry.colorterms.load(os.path.join(config_dir, "colorterms.py"))

config.psf_source_measurement.plugins["base_Jacobian"].pixelScale = 0.263
config.psf_source_measurement.undeblended["base_Jacobian"].pixelScale = 0.263
config.star_measurement.plugins["base_Jacobian"].pixelScale = 0.263
config.star_measurement.undeblended["base_Jacobian"].pixelScale = 0.263
