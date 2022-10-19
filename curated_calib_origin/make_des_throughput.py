#!/usr/bin/env python
"""Convert DES system throughput file into IsrCalibs.
"""
import argparse
import numpy as np
import os
import sys
import astropy.io.fits
import astropy.table
import astropy.units as units
from collections import OrderedDict

from lsst.obs.decam.decamFilters import DECAM_FILTER_DEFINITIONS
from lsst.obs.decam import DarkEnergyCamera
from lsst.utils import getPackageDir


DECAM_BEGIN = "2012-09-12T00:00:00"  # Initial date for DECam first light.
DECAM_CREATION_DATE = "2012-09-12"
DECAM_CREATION_TIME = "00:00:00"


def get_transmission_dir():
    """Get transmission directory in obs package for outputting data."""
    return os.path.join(getPackageDir("obs_decam"), "decam", "transmission_system")


def read_transmission_file(filename, band):
    """Read a transmission file and get a dict of tables.

    Parameters
    ----------
    filename : `str`
        Filename to read.
    band : `str`
        Name of band.

    Returns
    -------
    detector_dict : `dict` [`str`, `astropy.table.Table`]
        Dictionary keyed by detector name, each element is an astropy
        table with columns ``wavelength`` and ``throughput``.
    physical_filter : `str`
        Physical filter name, with spaces replaced with underscores.
    """
    input_table = astropy.io.fits.getdata(filename)

    camera = DarkEnergyCamera().getCamera()

    physical_filter = None
    for filter_def in DECAM_FILTER_DEFINITIONS:
        if band.lower() == filter_def.band:
            physical_filter = filter_def.physical_filter
            break

    if physical_filter is None:
        raise RuntimeError(f"Band {band} not found in filter definitions.")

    detector_dict = {}
    for index in range(input_table["throughput_ccd"].shape[1]):
        # The DECam detector numbering starts at 1.
        detector = camera[index + 1]

        tput_table = astropy.table.Table(
            data={
                "wavelength": input_table["lambda"].astype(np.float64)*units.angstrom,
                "throughput": input_table["throughput_ccd"][:, index].astype(np.float64),
            }
        )

        metadata = OrderedDict({
            "MODE": "DETECTOR",
            "TYPE": "transmission_system",
            "CALIBDATE": DECAM_BEGIN,
            "INSTRUME": camera.getName(),
            "OBSTYPE": "transmission_system",
            "CALIBCLS": "lsst.ip.isr.IntermediateSystemTransmissionCurve",
            "DETECTOR": detector.getId(),
            "DETECTOR_NAME": detector.getName(),
            "SOURCE": filename,
            "FILTER": physical_filter,
            "CALIB_CREATION_DATE": DECAM_CREATION_DATE,
            "CALIB_CREATION_TIME": DECAM_CREATION_TIME,
        })

        tput_table.meta = metadata

        detector_dict[detector.getName()] = tput_table

    return detector_dict, physical_filter.replace(" ", "_")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert DES system transmission info into LSST IntermediateTramissionCurves.")
    parser.add_argument("-d", "--desfile", help="DES transmission file.", required=True)
    parser.add_argument("-b", "--band", help="Band name.", required=True)
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing transmission curves.")
    cmd = parser.parse_args()

    out_dict, physical_filter = read_transmission_file(cmd.desfile, cmd.band)

    transmission_dir = get_transmission_dir()
    if not os.path.exists(transmission_dir):
        os.makedirs(transmission_dir)

    for det_name in out_dict:
        out_dir = os.path.join(transmission_dir, det_name.lower(), physical_filter.lower())
        if os.path.exists(out_dir):
            if not cmd.force:
                print(f"Output directory {out_dir} exists; use --force to replace.")
                sys.exit(1)
        else:
            os.makedirs(out_dir)
        out_table = out_dict[det_name]
        outfile = os.path.join(out_dir, f"{out_table.meta['CALIBDATE']}.ecsv")
        out_table.write(outfile, overwrite=cmd.force)
