obs_decam/curated_calib_origin
==============================

This directory includes amplifier characteristics data that is used to create the "linearizer" and "crosstalk" curated calibration data products.
The linearity table `linearity_table_v*.fits` is a standard DECam calibration file from
[DECam Community Pipeline Calibration Files](https://noirlab.edu/science/programs/ctio/instruments/Dark-Energy-Camera/Calibration-Files).

To convert inputs to the format suitable for [obs_decam_data](https://github.com/lsst/obs_decam_data), run `makeLinearizer.py linearity_table_v0.4.fits` and `makeCrosstalkDecam.py DECam_xtalk_20130606.txt`.

DECam System Transmission Curves
================================

The grizy throughputs in this directory were obtained from https://des.ncsa.illinois.edu/releases/other/instrumental-throughputs on 19 October 2022.
The release notes say:

Prior to use within the FGCM photometric calibration, these throughputs were modified slightly by Eli Rykoff (SLAC). In particular:

* For CCD 31, the scan from the left (B) amplifier was used (as the other amplifier was non-operational).
( For CCD 2, the throughput was taken as the average of the throughputs of CCD 1 and 3.
This captures the spatial variation of the filter, but unfortunately not the differences in throughput due to different anti-reflective coatings, particularly noticeable for the g filter. )

The curves have been renormalized so that the i filter throughput in the wavelength range 7350 A < lambda < 8150 A is 1.0.

These files are distributed as fits files, with each filter cropped to the wavelength range where there is non-zero throughput.
The files have one row for each wavelength step.

* lambda: Wavelength in A.
* throughput_avg: Average throughput across the focal plane (normalized to i filter as described).
* througput_ccd: 62 columns (for ccd 1 through 62) per-ccd throughput.

The files are:

* g_band_per_detector_throughput.fits
* r_band_per_detector_throughput.fits
* i_band_per_detector_throughput.fits
* z_band_per_detector_throughput.fits
* Y_band_per_detector_throughput.fits

To convert inputs to the format suitable for [obs_decam_data](https://github.com/lsst/obs_decam_data), run:

* `python make_des_throughput.py --desfile g_band_per_detector_throughput.fits --band g`
* `python make_des_throughput.py --desfile r_band_per_detector_throughput.fits --band r`
* `python make_des_throughput.py --desfile i_band_per_detector_throughput.fits --band i`
* `python make_des_throughput.py --desfile z_band_per_detector_throughput.fits --band z`
* `python make_des_throughput.py --desfile Y_band_per_detector_throughput.fits --band Y`

DECam Standard Atmosphere
=========================

The fits file `des_atm_std.fits` describes the standard atmosphere used for DES analysis.
This atmosphere has a zenith distance of 33.575731 degrees (airmass of 1.2); precipitable water vapor of 3.0 mm; aerosol tau = 0.03 (at 7750 A) and alpha=1.0; ozone of 263 DU; and barometric pressure of 778 mb.
The files have one row for each wavelength step.

* lambda: Wavelength in A.
* throughput_atm: Standard atmosphere throughput.

To convert inputs to the format suitable for [obs_decam_data](https://github.com/lsst/obs_decam_data), run `make_des_standard_atmosphere.py --desfile des_atm_std.fits`.
