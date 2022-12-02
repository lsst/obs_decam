#!/usr/bin/env python
"""Convert DES standard atmosphere into IsrCalib.
"""
import argparse
import numpy as np
import os
import sys
import astropy.io.fits
import astropy.table
import astropy.units as units
from collections import OrderedDict

from lsst.obs.decam import DarkEnergyCamera
from lsst.utils import getPackageDir


DECAM_BEGIN = "2012-09-12T00:00:00"  # Initial date for DECam first light.
DECAM_CREATION_DATE = "2012-09-12"
DECAM_CREATION_TIME = "00:00:00"


def get_transmission_dir():
    """Get transmission directory in obs package for outputting data."""
    return os.path.join(getPackageDir("obs_decam"), "decam", "transmission_atmosphere")


def read_transmission_file(filename):
    """Read a transmission file and return a table.

    Parameters
    ----------
    filename : `str`
        Filename to read.

    Returns
    -------
    transmission_table : `astropy.table.Table`
        Astropy table with columns ``wavelength`` and ``throughput``.
    """
    input_table = astropy.io.fits.getdata(filename)

    camera = DarkEnergyCamera().getCamera()

    tput_table = astropy.table.Table(
        data={
            "wavelength": input_table["lambda"].astype(np.float64)*units.angstrom,
            "throughput": input_table["throughput_atm"].astype(np.float64),
        }
    )

    metadata = OrderedDict({
        "TYPE": "transmission_atmosphere",
        "CALIBDATE": DECAM_BEGIN,
        "INSTRUME": camera.getName(),
        "OBSTYPE": "transmission_atmosphere",
        "CALIBCLS": "lsst.ip.isr.IntermediateAtmosphereTransmissionCurve",
        "SOURCE": filename,
        "CALIB_CREATION_DATE": DECAM_CREATION_DATE,
        "CALIB_CREATION_TIME": DECAM_CREATION_TIME,
    })

    tput_table.meta = metadata

    return tput_table


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert DES atmosphere transmission info into LSST IntermediateTramissionCurve.")
    parser.add_argument("-d", "--desfile", help="DES transmission file.", required=True)
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing transmission curves.")
    cmd = parser.parse_args()

    out_table = read_transmission_file(cmd.desfile)

    out_dir = get_transmission_dir()
    if os.path.exists(out_dir):
        if not cmd.force:
            print(f"Output directory {out_dir} exists; use --force to replace.")
            sys.exit(1)
    else:
        os.makedirs(out_dir)

    outfile = os.path.join(out_dir, f"{out_table.meta['CALIBDATE']}.ecsv")
    out_table.write(outfile, overwrite=cmd.force)
