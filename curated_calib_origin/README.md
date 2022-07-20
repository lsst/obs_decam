obs_decam/curated_calib_origin
==============================

This directory includes amplifier characteristics data that is used to create the "linearizer" and "crosstalk" curated calibration data products.
The linearity table `linearity_table_v*.fits` is a standard DECam calibration file from
[DECam Community Pipeline Calibration Files](https://noirlab.edu/science/programs/ctio/instruments/Dark-Energy-Camera/Calibration-Files).

To convert inputs to the format suitable for [obs_decam_data](https://github.com/lsst/obs_decam_data), run `makeLinearizer.py linearity_table_v0.4.fits` and `makeCrosstalkDecam.py DECam_xtalk_20130606.txt`.
