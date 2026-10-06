"""
DECam-specific overrides for CharacterizeImageTask
"""
# PSF determination
# These configs match obs_subaru, to facilitate 1:1 comparisons between
# DECam and HSC.
config.measurePsf.reserve.fraction = 0.2

# Activate calibration of measurements: required for aperture corrections
config.load("cmodel.py")
config.measurement.load("apertures.py")
config.measurement.load("kron.py")
config.measurement.load("convolvedFluxes.py")
config.measurement.load("gaap.py")
config.measurement.load("hsm.py")
if "ext_shapeHSM_HsmShapeRegauss" in config.measurement.plugins:
    # no deblending has been done
    config.measurement.plugins["ext_shapeHSM_HsmShapeRegauss"].deblendNChild = ""

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.263

# Convolved fluxes can fail for small target seeing if the observation seeing
# is larger.
if "ext_convolved_ConvolvedFlux" in config.measurement.plugins:
    names = config.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames()
    config.measureApCorr.allowFailure += names

if "ext_gaap_GaapFlux" in config.measurement.plugins:
    names = config.measurement.plugins["ext_gaap_GaapFlux"].getAllGaapResultNames()
    config.measureApCorr.allowFailure += names

# For aperture correction modeling, only use objects that were used in the
# PSF model and have psf flux signal-to-noise > 200.
# These configs match obs_subaru, to facilitate 1:1 comparisons between
# DECam and HSC.
config.measureApCorr.sourceSelector["science"].doFlags = True
config.measureApCorr.sourceSelector["science"].doUnresolved = False
config.measureApCorr.sourceSelector["science"].doSignalToNoise = True
config.measureApCorr.sourceSelector["science"].flags.good = ["calib_psf_used"]
config.measureApCorr.sourceSelector["science"].flags.bad = []
config.measureApCorr.sourceSelector["science"].signalToNoise.minimum = 200.0
config.measureApCorr.sourceSelector["science"].signalToNoise.maximum = None
config.measureApCorr.sourceSelector["science"].signalToNoise.fluxField = "base_PsfFlux_instFlux"
config.measureApCorr.sourceSelector["science"].signalToNoise.errField = "base_PsfFlux_instFluxErr"
config.measureApCorr.sourceSelector.name = "science"
