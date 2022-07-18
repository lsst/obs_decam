#!/usr/bin/env python
"""Convert a DECam official linearity FITS table into LSST linearizers
"""
import argparse
import sys
import os.path

import numpy as np
import astropy.io.fits as fits

import lsst.obs.decam
from lsst.ip.isr import Linearizer
from lsst.utils import getPackageDir


def makeLinearizerDecam(fromFile, force=False, verbose=False):
    """Convert the specified DECam linearity FITS table to standard LSST format

    Parameters
    ----------
    fromFile : `str`
        Filename to read linearity data from.
    force : `bool`, optional
        Overwrite existing outputs?
    verbose : `bool`, optional
        Control message verbosity.

    Raises
    ------
    RuntimeError :
        Raised if the ADU values are not contiguous.

    Notes
    -----

    This script generates LSST linearity stand-alone LookupTables, as
    well as middleware gen-3 `ip_isr` Linearizers.  These products are
    written to ${OBS_DECAM_DIR}/decam/calib/linearizer/ for gen3 products.

    The input file format is one table per CCD, with the HDU indexed
    by amplifier number.  Each table has 3 columns: ADU, ADU_LINEAR_A,
    ADU_LINEAR_B, and the values of ADU are contiguous (0, 1, 2...).
    The values of the last two columns are replacements (0+delta0,
    1+delta1, 2+delta2...) for each of the two amplifiers, and this is
    converted to offsets for the LSST linearization tables (delta0,
    delta1, delta2...).  Output is a set of LinearizeLookupTable
    instances, one per CCD, saved as dataset type "linearizer" - The
    row indices for the linearization lookup table are (row index=amp
    name): 0=A, 1=B.  These linearization lookup tables are also
    stored in the gen3 Linearizers, as are the appropriate row indices
    and column offsets.
    """
    print("Making DECam linearizers from %r" % (fromFile,))

    instrument = lsst.obs.decam.DarkEnergyCamera()
    camera = instrument.getCamera()

    fromHDUs = fits.open(fromFile)[1:]  # HDU 0 has no data
    assert len(fromHDUs) == len(camera)
    for ccdind, (detector, hdu) in enumerate(zip(camera, fromHDUs)):
        ccdnum = ccdind + 1
        if verbose:
            print("ccdnum=%s; detector=%s" % (ccdnum, detector.getName()))
        fromData = hdu.data
        assert len(fromData.dtype) == 3
        lsstTable = np.zeros((2, len(fromData)), dtype=np.float32)
        uncorr = fromData["ADU"]
        if not np.allclose(uncorr, np.arange(len(fromData))):
            raise RuntimeError("ADU data not a range of integers starting at 0")
        for i, ampName in enumerate("AB"):
            # convert DECam replacement table to LSST offset table
            if verbose:
                print("DECam table for %s=%s..." % (ampName, fromData["ADU_LINEAR_" + ampName][0:5],))
            lsstTable[i, :] = fromData["ADU_LINEAR_" + ampName] - uncorr
            if verbose:
                print("LSST  table for %s=%s..." % (ampName, lsstTable[i, 0:5],))

        # Generate gen3 files into local directory.
        myLinearity = Linearizer(table=lsstTable)
        for i, ampName in enumerate("AB"):
            myLinearity.ampNames.append(ampName)
            myLinearity.linearityType[ampName] = 'LookupTable'
            myLinearity.linearityCoeffs[ampName] = np.array([i, 0])
            myLinearity.linearityBBox[ampName] = detector.getAmplifiers()[i].getBBox()
            myLinearity.fitParams[ampName] = np.array([])
            myLinearity.fitParamsErr[ampName] = np.array([])
            myLinearity.fitChiSq[ampName] = np.nan
            myLinearity.fitResiduals[ampName] = np.array([])
            myLinearity.linearFit[ampName] = np.array([])
        calibDate = '1970-01-01T00:00:00'
        myLinearity.updateMetadata(camera=camera, detector=detector,
                                   CALIBDATE=calibDate, setCalibId=True)
        myLinearity.hasLinearity = True

        outDir = os.path.join(getPackageDir('obs_decam'), 'decam', 'CALIB', 'linearity',
                              detector.getName().lower())
        if os.path.exists(outDir) and not force:
            print("Output directory %r exists; use --force to replace" % (outDir, ))
            sys.exit(1)
        else:
            os.makedirs(outDir)

        filename = calibDate + ".yaml"
        myLinearity.writeText(os.path.join(outDir, filename))

    print("Wrote %s linearizers" % (ccdind+1,))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a DECam linearity FITS file into LSST linearizers")
    parser.add_argument(dest="fromFile", help="DECam linearity FITS file")
    parser.add_argument("-v", "--verbose", action="store_true", help="print data about each detector")
    parser.add_argument("--force", action="store_true", help="overwrite existing data")
    cmd = parser.parse_args()

    makeLinearizerDecam(fromFile=cmd.fromFile, force=cmd.force, verbose=cmd.verbose)
