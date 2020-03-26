Description
===========

This obs_decam package is for interfacing DECam with the LSST Data Management
software.

This package is not a part of the official LSST Data Management stack, and is
hosted by the LSST project only as a courtesy to the astronomical community.
The LSST does not commit to supporting this package, and makes no warranty
about its quality or performance.  It is licensed under the GNU Public License
version 3.

The initial version of this package was provided by Paul Price
(price@astro.princeton.edu), and though he also makes no commitment to
support it, users are welcome to contact him and/or the LSST Data Management
mailing list (lsst-data@lsstcorp.org) with questions.


Copyleft
--------

LSST Data Management System
Copyright 2012-2016 AURA/LSST.

This package is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Use
===

Documentation of the LSST Science Pipelines is at https://pipelines.lsst.io

1. Create a data repository directory:

        $ mkdir /path/to/repo
        $ echo lsst.obs.decam.DecamMapper > /path/to/repo/_mapper

2. Get and build obs_decam:

        $ cd /path/to/work
        $ git clone git://github.com/lsst/obs_decam.git
        $ cd obs_decam
        $ setup -t <CURRENT_TAG> -r .
        $ scons install declare --tag=current

3. Import instcal/dqmask/wtmap data into the data repository:

        $ ingestImagesDecam.py /path/to/repo --filetype instcal --mode=link instcal/*.fits.fz

4. Alternatively, import raw and calibration data into the data repository, for example:

        $ ingestImagesDecam.py /path/to/repo --filetype raw /path/to/raw/*.fits.fz
        $ ingestCalibs.py /path/to/repo/  --calib /path/to/calib/repo/ --calibType defect /path/to/calib/*fits --validity 0
        $ ingestCalibs.py /path/to/repo/  --calib /path/to/calib/repo/ /path/to/bias-and-flat-files/*fits --validity 999
        $ ingestCalibs.py /path/to/repo/  --calib /path/to/calib/repo/ /path/to/fringe-files/*fits --validity 999

   By default, ingesting calibration data only creates a repository database.
   When ingesting biases and flats, if you would like to also link these files (in the same way as images are ingested), use `--mode=link`.
   This functionality is not currently supported for other calibTypes (i.e., defect or fringe).

5. Process data:

        $ processCcd.py /path/to/repo/ --id visit=283453 ccdnum=10 --output /path/to/your/output/repo/ -C /path/to/your/config/override/file --config calibrate.doAstrometry=False calibrate.doPhotoCal=False

6. To read instcal files from the community pipeline, replace the ISR task with `DecamNullIsrTask` by using a config override file containing the following:

        from lsst.obs.decam.decamNullIsr import DecamNullIsrTask
        config.isr.retarget(DecamNullIsrTask)
