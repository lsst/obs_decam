obs_decam/decam
===============

This directory includes camera geometry and amplifier characteristics data
that is used by the butler to create the "camera" and "linearizer" data products.
The linearity table `linearity_table_v*.fits` is a standard DECam calibration file from
[DECam Community Pipeline Calibration Files](http://www.ctio.noao.edu/noao/content/decam-calibration-files).
Building the `obs_decam` package converts the linearity table to LSST linearizers `linearizer/*.fits`
by running `makeLinearizer.py`.

To convert inputs to the format suitable for `obs_decam_data`, run `makeLinearizer.py linearity_table_v0.4.fits` and `makeCrosstalkDecam.py DECam_xtalk_20130606.txt`.

