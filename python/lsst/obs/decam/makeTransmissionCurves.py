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

import os
import astropy.io.fits
import numpy as np

from lsst.afw.image import TransmissionCurve
from lsst.utils import getPackageDir
from .decamFilters import DECAM_FILTER_DEFINITIONS

__all__ = ("getDESSystemTransmission", "getDESAtmosphereTransmission")

DATA_DIR = os.path.join(getPackageDir("obs_decam_data"), "decam", "transmission_curves")

DECAM_BEGIN = "2012-09-12"  # Initial date for DECam first light.


def getDESAtmosphereTransmission():
    """Return a dictionary of TransmissionCurves describing the atmospheric
    throughput at CTIO.

    Dictionary keys are string dates (YYYY-MM-DD) indicating the beginning of
    the validity period for the curve stored as the associated dictionary
    value.  The curve is guaranteed not to be spatially-varying.
    """
    table = astropy.io.fits.getdata(os.path.join(DATA_DIR, "des", "des_atm_std.fits"))

    atm = TransmissionCurve.makeSpatiallyConstant(
        throughput=table["throughput_atm"].astype(np.float64),
        wavelengths=table["lambda"].astype(np.float64),
        throughputAtMin=table["throughput_atm"][0],
        throughputAtMax=table["throughput_atm"][-1],
    )

    return {DECAM_BEGIN: atm}


def getDESSystemTransmission():
    """Return a nested dictionary of TransmissionCurves describing the
    system throughput (optics + filter + detector) at the location of
    each detector.

    Outer dictionary keys are string dates (YYYY-MM-DD).  The next level
    dictionary maps the physical filter name to another dict.  The inner
    dict is keyed by detector number.
    """
    # We have DES detector throughputs for the grizy bands.

    bands = ["g", "r", "i", "z", "Y"]

    filter_dict = {}
    for band in bands:
        for filter_def in DECAM_FILTER_DEFINITIONS:
            if band == filter_def.band:
                physical_filter = filter_def.physical_filter
                break

        table = astropy.io.fits.getdata(
            os.path.join(DATA_DIR, "des", f"{band}_band_per_detector_throughput.fits"),
        )

        detector_dict = {}
        for index in range(table['throughput_ccd'].shape[1]):
            # The DECam detector starts at 1.
            detector = index + 1

            tput = TransmissionCurve.makeSpatiallyConstant(
                throughput=table["throughput_ccd"][:, index].astype(np.float64),
                wavelengths=table["lambda"].astype(np.float64),
                throughputAtMin=0.0,
                throughputAtMax=0.0,
            )

            detector_dict[detector] = tput

        filter_dict[physical_filter] = detector_dict

    return {DECAM_BEGIN: filter_dict}
