obs_decam/curated_calib_origin
==============================

This directory includes amplifier characteristics data
that is used by the butler to create the "camera" and "linearizer" data products.
The linearity table `linearity_table_v*.fits` is a standard DECam calibration file from
[DECam Community Pipeline Calibration Files](http://www.ctio.noao.edu/noao/content/decam-calibration-files).

To convert inputs to the format suitable for `obs_decam_data`, run `makeLinearizer.py linearity_table_v0.4.fits` and `makeCrosstalkDecam.py DECam_xtalk_20130606.txt`.
