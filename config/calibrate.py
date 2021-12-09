"""
DECam-specific overrides for CalibrateTask
"""
import os.path

from lsst.meas.algorithms import ColorLimit
from lsst.meas.astrom import MatchOptimisticBConfig

obsConfigDir = os.path.join(os.path.dirname(__file__))

# Astrometry/Photometry
# This sets the reference catalog name for Gen2.
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
    # Note the u-band results may not be useful without a color term
    refObjLoader.filterMap['u'] = 'g'
    refObjLoader.filterMap['Y'] = 'y'
    refObjLoader.filterMap['N419'] = 'g'
    refObjLoader.filterMap['N540'] = 'g'
    refObjLoader.filterMap['N708'] = 'i'
    refObjLoader.filterMap['N964'] = 'z'

# This sets up the reference catalog for Gen3.
config.connections.astromRefCat = "ps1_pv3_3pi_20170110"
config.connections.photoRefCat = "ps1_pv3_3pi_20170110"

# Photometric calibration: use color terms
config.photoCal.applyColorTerms = True
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"
colors = config.photoCal.match.referenceSelection.colorLimits
# The following two color limits are adopted from obs_subaru for the HSC SSP survey
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
config.photoCal.match.referenceSelection.doMagLimit = True
config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
config.photoCal.match.referenceSelection.magLimit.maximum = 22.0
config.photoCal.colorterms.load(os.path.join(obsConfigDir, 'colorterms.py'))

# Number of bright stars to use. Sets the max number of patterns that can be tested.
# This config matches obs_subaru, to facilitate 1:1 comparisons between DECam and HSC
config.astrometry.matcher.numBrightStars = 150

# The Task default was reduced from 4 to 2 on RFC-577. We believe that 4 is
# more appropriate for use with DECam data until a Jointcal-derived distortion
# model is available (DM-24431); at that point, this override should likely be
# removed.
# See Slack: https://lsstc.slack.com/archives/C2B6X08LS/p1586468459084600
config.astrometry.wcsFitter.order = 4

for matchConfig in (config.astrometry,
                    ):
    matchConfig.sourceFluxType = 'Psf'
    matchConfig.sourceSelector.active.sourceFluxType = 'Psf'
    matchConfig.matcher.maxOffsetPix = 250
    if isinstance(matchConfig.matcher, MatchOptimisticBConfig):
        matchConfig.matcher.allowedNonperpDeg = 0.2
        matchConfig.matcher.maxMatchDistArcSec = 2.0
        matchConfig.sourceSelector.active.excludePixelFlags = False

# Set to match defaults currently used in HSC production runs (e.g. S15B+)
config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio = 0.95

# Demand astrometry and photoCal succeed
config.requireAstrometry = True
config.requirePhotoCal = True

config.doWriteMatchesDenormalized = True

# Detection
# This config matches obs_subaru, to facilitate 1:1 comparisons between DECam and HSC
config.detection.isotropicGrow = True

config.measurement.load(os.path.join(obsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(obsConfigDir, "kron.py"))
config.measurement.load(os.path.join(obsConfigDir, "hsm.py"))

# Deblender
# These configs match obs_subaru, to facilitate 1:1 comparisons between DECam and HSC
config.deblend.maxFootprintSize = 0
config.deblend.maskLimits["NO_DATA"] = 0.25  # Ignore sources that are in the vignetted region
config.deblend.maxFootprintArea = 10000

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.263
