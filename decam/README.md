obs_decam/decam
===============

This directory includes camera geometry and amplifier characteristics data
that is used by the butler to create the "camera" and "linearizer" data products.

The `camera` directory, containing the camera geometry FITS binary tables, is built when soncs run by running `makeDecamCameraRepository.py` on `segmentfile.txt` and `chipcenters.txt`.

The linearity table `linearity_table_v*.fits` is a standard DECam calibration file from
[DECam Community Pipeline Calibration Files](http://www.ctio.noao.edu/noao/content/decam-calibration-files).
Building the `obs_decam` package converts the linearity table to LSST linearizers `linearizer/*.fits` by running `makeLinearizer.py`.
