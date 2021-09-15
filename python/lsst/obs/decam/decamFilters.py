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
                     band="u",
                     lambdaEff=350, lambdaMin=305, lambdaMax=403),
    FilterDefinition(physical_filter="g DECam SDSS c0001 4720.0 1520.0",
                     band="g",
                     lambdaEff=450, lambdaMin=394, lambdaMax=555),
    FilterDefinition(physical_filter="r DECam SDSS c0002 6415.0 1480.0",
                     band="r",
                     lambdaEff=600, lambdaMin=562, lambdaMax=725),
    FilterDefinition(physical_filter="i DECam SDSS c0003 7835.0 1470.0",
                     band="i",
                     lambdaEff=750, lambdaMin=699, lambdaMax=870,),
    FilterDefinition(physical_filter="z DECam SDSS c0004 9260.0 1520.0",
                     band="z",
                     lambdaEff=900, lambdaMin=837, lambdaMax=1016),
    FilterDefinition(physical_filter="Y DECam c0005 10095.0 1130.0",
                     band="y",
                     lambdaEff=1000, lambdaMin=941, lambdaMax=1080,
                     alias={'Y'}),
    FilterDefinition(physical_filter="VR DECam c0007 6300.0 2600.0",
                     band="VR",
                     doc='A very broad-band filter, intended for "discovery", not "accurate photometry".'
                         'For details, wee: http://www.ctio.noao.edu/noao/content/decam-vr-filter',
                     lambdaEff=630, lambdaMin=490, lambdaMax=765),
    FilterDefinition(physical_filter="N964 DECam c0008 9645.0 94.0",
                     band="N964",
                     lambdaEff=964),
    FilterDefinition(physical_filter="solid plate 0.0 0.0",
                     band="opaque",
                     afw_name='SOLID', lambdaEff=0),
    FilterDefinition(physical_filter="N708 DECam c0012 7080.0 400.0",
                     band="N708",
                     lambdaEff=708),
    FilterDefinition(physical_filter="N540 DECam c0014 5403.2 210.0",
                     band="N540",
                     lambdaEff=540),
    FilterDefinition(physical_filter="N419 DECam c0013 4194.0 75.0",
                     band="N419",
                     lambdaEff=419),
)
