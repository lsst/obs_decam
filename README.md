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

1. Create a data repository directory:

        $ mkdir /path/to/repo
        $ echo lsst.obs.decam.DecamMapper > /path/to/repo/_mapper

2. Get and build obs_decam:

        $ cd /path/to/work
        $ git clone git://github.com/LSST-nonproject/obs_decam.git
        $ cd obs_decam
        $ setup -t <CURRENT_TAG> -r .
        $ scons install declare

3. Import data into the data repository:

        $ cd /path/to/data
        $ setup -t <CURRENT_TAG> pipe_tasks
        $ setup -k -t <CURRENT_TAG> obs_decam
        $ ingestImages.py /path/to/repo --mode=link *.fits

4. Process data

        $ setup -t <CURRENT_TAG> pipe_tasks
        $ setup -k -t <CURRENT_TAG> obs_decam
        $ processCcd.py /path/to/repo --id visit=12345 ccd=5 side=N

Data identifiers
================

The following keywords are available when specifying a data identifier:
* `proposal`: proposal identifier
* `visit`: exposure number
* `taiObs`: actually UTC, but not very useful for specifying data, as must match exactly
* `expTime`
* `date`
* `filter`
* `side`: `N` or `S`
* `ccd`: CCD number; together with side, specifies a unique CCD
* `object`: object name

`visit`, `side`, `ccd` are required to specify a unique CCD image.
