# Set up aperture photometry
# 'config' should be a SourceMeasurementConfig

# Use a large aperture to be independent of seeing in calibration
# This config matches obs_subaru, to facilitate 1:1 comparisons between
# DECam and HSC.
config.plugins["base_CircularApertureFlux"].maxSincRadius = 12.0
