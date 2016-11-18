#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
"""Convert a Mosaic official linearity FITS table into LSST linearizers
"""
import argparse
import sys
import os.path


import numpy as np
import astropy.io.fits as fits

from lsst.ip.isr import LinearizeLookupTable
from lsst.obs.mosaic import MosaicMapper
from lsst.daf.persistence import Butler


def makeLinearizerMosaic(fromFile, force=False, verbose=False):
    """Convert the specified Mosaic linearity FITS table to standard LSST format

    Details:
    - Input format is one table per CCD, HDU is amplifier number,
        the table has 3 columns: ADU, ADU_LINEAR_A, ADU_LINEAR_B.
        The values of ADU contiguous (0, 1, 2...) but check and error out if not.
        The values of the latter two are replacements (0+delta0, 1+delta1, 2+delta2...)
        and this is converted to offsets for the LSST linearization tables (delta0, delta1, delta2...)
    - Output is a set of LinearizeLookupTable instances, one per CCD, saved as dataset type "linearizer"
    - The row indices for the linearization lookup table are (row index=amp name): 0=A, 1=B

    @param[in] fromFile  path to Mosaic linearity table (a FITS file with one HDU per amplifier)
    """
    print("Making Mosaic linearizers from %r" % (fromFile,))
    butler = Butler(mapper=MosaicMapper)
    linearizerDir = MosaicMapper.getLinearizerDir()
    if os.path.exists(linearizerDir):
        if not force:
            print("Output directory %r exists; use --force to replace" % (linearizerDir,))
            sys.exit(1)
        print("Replacing data in linearizer directory %r" % (linearizerDir,))
    else:
        print("Creating linearizer directory %r" % (linearizerDir,))
        os.makedirs(linearizerDir)

    camera = MosaicMapper().camera
    fromHDUs = fits.open(fromFile)[1:] # HDU 0 has no data
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
            # convert Mosaic replacement table to LSST offset table
            if verbose:
                print("Mosaic table for %s=%s..." % (ampName, fromData["ADU_LINEAR_" + ampName][0:5],))
            lsstTable[i, :] = fromData["ADU_LINEAR_" + ampName] - uncorr
            if verbose:
                print("LSST  table for %s=%s..." % (ampName, lsstTable[i, 0:5],))
        linearizer = LinearizeLookupTable(table=lsstTable, detector=detector)
        butler.put(linearizer, "linearizer", dataId=dict(ccdnum=ccdnum))
    print("Wrote %s linearizers" % (ccdind+1,))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a Mosaic linearity FITS file into LSST linearizers")
    parser.add_argument(dest="fromFile", help="Mosaic linearity FITS file")
    parser.add_argument("-v", "--verbose", action="store_true", help="print data about each detector")
    parser.add_argument("--force", action="store_true", help="overwrite existing data")
    cmd = parser.parse_args()

    makeLinearizerMosaic(fromFile=cmd.fromFile, force=cmd.force, verbose=cmd.verbose)
