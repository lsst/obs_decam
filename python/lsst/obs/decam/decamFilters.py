# This file is part of obs_decam.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

# lambdaMin and lambda max are chosen to be where the filter rises above 1%
# from http://www.ctio.noao.edu/noao/sites/default/files/DECam/DECam_filters_transmission.txt
DECAM_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(physical_filter="u DECam c0006 3500.0 1000.0",
                     band="u"),
    FilterDefinition(physical_filter="g DECam SDSS c0001 4720.0 1520.0",
                     band="g"),
    FilterDefinition(physical_filter="r DECam SDSS c0002 6415.0 1480.0",
                     band="r"),
    FilterDefinition(physical_filter="i DECam SDSS c0003 7835.0 1470.0",
                     band="i"),
    FilterDefinition(physical_filter="z DECam SDSS c0004 9260.0 1520.0",
                     band="z"),
    FilterDefinition(physical_filter="Y DECam c0005 10095.0 1130.0",
                     band="y",
                     alias={'Y'}),
    FilterDefinition(physical_filter="VR DECam c0007 6300.0 2600.0",
                     band="VR",
                     doc='A very broad-band filter, intended for "discovery", not "accurate photometry".'
                         'For details, see: http://www.ctio.noao.edu/noao/content/decam-vr-filter'),
    FilterDefinition(physical_filter="N964 DECam c0008 9645.0 94.0",
                     band="N964"),
    FilterDefinition(physical_filter="solid plate 0.0 0.0",
                     band="opaque",
                     afw_name='SOLID'),
    FilterDefinition(physical_filter="N708 DECam c0012 7080.0 400.0",
                     band="N708"),
    FilterDefinition(physical_filter="N419 DECam c0013 4194.0 75.0",
                     band="N419"),
    FilterDefinition(physical_filter="N540 DECam c0014 5403.2 210.0",
                     band="N540"),
)
