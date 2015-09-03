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
Copyright 2012 LSST Corporation.

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

Documentation for this can be found at:
        $ https://confluence.lsstcorp.org/display/LSWUG/Process+DECam+Images
Currently, there is only support for "instcal" (plus dqmask and wtmap) processing.

1. Create a data repository directory:

        $ mkdir /path/to/repo
        $ echo lsst.obs.decam.DecamMapper > /path/to/repo/_mapper

2. Get and build obs_decam:

        $ cd /path/to/work
        $ git clone git://github.com/lsst/obs_decam.git
        $ cd obs_decam
        $ setup -t <CURRENT_TAG> -r .
        $ scons install declare --tag=current

3. Import data into the data repository:

        $ cd /path/to/data
        $ setup -t <CURRENT_TAG> pipe_tasks
        $ setup -k -t <CURRENT_TAG> obs_decam
        $ ingestImagesDecam.py /path/to/repo --mode=link instcal/*.fits.fz

4. Process data

        $ setup -t <CURRENT_TAG> pipe_tasks
        $ setup -k -t <CURRENT_TAG> obs_decam
        $ processCcdDecam.py /path/to/repo --id visit=283453 ccdnum=10 --config calibrate.doPhotoCal=False calibrate.doAstrometry=False calibrate.measurePsf.starSelector.name="secondMoment" doWriteCalibrateMatches=False --clobber-config

5. Import raw data into the data repository: 

        $  ingestImagesDecam.py /path/to/repo --mode=link --filetype="raw" raw/*.fits.fz 
