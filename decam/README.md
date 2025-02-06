obs_decam/decam
===============

This directory contains DECam camera geometry data including amplifier info tables for each detector, as well as information about how the DECam filters map to various reference catalogs (in `refcats.json`).

Reference catalog data
----------------------

Average color terms for the DECam filters are calculated using the Pickles stellar spectra atlas. The following values are provided by Song Huang
(Tsinghua University; dr.guangtou@gmail.com).
Color terms for u, Y, N419 and N964 bands are not currently available.

The values for DECam g, r & z-bands are calculated independently and are different to the values at: https://www.legacysurvey.org/dr9/description/

A Jupyter notebook to reproduce these values is available at:
https://github.com/MerianSurvey/caterpillar/blob/main/notebook/photocal/merian_filter_color_terms.ipynb

The DECam colorterms are appropriate for the following color ranges:

SDSS:

- g: `-1.0 < g-r < 1.8`
- r: `-1.0 < r-i < 2.2`
- i: `-1.0 < i-z < 1.2`
- z: `-1.0 < z-i < 0.5`
- N540: `-1.0 < g-r < 1.5`
- N708: `-1.0 < r-i < 2.0`

HSC:

- g: `-1.0 < g-r < 1.4`
- r: `-1.0 < r-i < 2.2`
- i: `-1.0 < i-z < 1.0`
- z: `-1.0 < z-y < 0.5`
- N540: `-1.0 < g-r < 1.5`
- N708: `-1.0 < r-i < 2.0`

PS1:

- g: `-1.0 < g-r < 1.2`
- r: `-1.0 < r-i < 2.2`
- i: `-1.0 < i-z < 1.4`
- z: `-1.0 < z-y < 1.0`
- N540: `-1.0 < g-r < 1.5`
- N708: `-1.0 < r-i < 2.0`
