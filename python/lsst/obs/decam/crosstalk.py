#
# This file is part of obs_decam.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# Copyright 2018 LSST Corporation.
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
#

"""Apply crosstalk corrections to DECam images.

Some of this code is based on DECam_crosstalk.py, used for the THELI pipeline
and written by Thomas Erben (private communication, 2018)
"""


from collections import defaultdict
from astropy.io import fits
import datetime as dt
import os
import argparse
import re
import numpy as np

import lsst.log
import lsst.pipe.base as pipeBase
from lsst.ip.isr import CrosstalkConfig, CrosstalkTask, IsrTask
from lsst.obs.decam import DecamMapper
from lsst.utils import getPackageDir


__all__ = ["DecamCrosstalkTask"]


class DecamCrosstalkConfig(CrosstalkConfig):
    """Configuration for DECam crosstalk removal.
    """

    def getSourcesAndCoeffsFile(self, filename='DECam_xtalk_20130606.txt'):
        """File containing DECam crosstalk coefficients.

        This text file is provided by NOAO in a particular format with
        information about the DECam crosstalk coefficients. It is available at
        http://www.ctio.noao.edu/noao/content/DECam-Calibration-Files

        Parameters
        ----------
        filename : `str`, optional
            File containing the decam crosstalk coefficients, from NOAO.

        Returns
        -------
        result : `str`
            Full path to filename.
        """
        mapper = DecamMapper()
        packageName = mapper.getPackageName()
        packageDir = getPackageDir(packageName)
        return os.path.join(packageDir, 'decam', filename)

    def getSourcesAndCoeffs(self):
        """Read crosstalk sources and coefficients from DECam-specific file.

        Returns
        -------
        sources : `defaultdict`
            Sources of crosstalk read from crosstalk_file.
        coeffs : `dict`
            Linear crosstalk coefficients corresponding to sources.
        """
        crosstalk_file = self.getSourcesAndCoeffsFile()
        sources = defaultdict(list)
        coeffs = {}
        log = lsst.log.Log.getLogger('obs.decam.DecamCrosstalkConfig')
        log.info('Reading crosstalk coefficient data')
        with open(crosstalk_file) as f:
            for line in f:
                li = line.strip()
                if not li.startswith('#'):
                    elem = li.split()
                    # The xtalk file has image areas like 'ccd01A'; preserve only '01A'
                    sources[elem[0][3:]].append(elem[1][3:])
                    # The linear crosstalk coefficients
                    coeffs[(elem[0][3:], elem[1][3:])] = float(elem[2])
        return sources, coeffs


class DecamCrosstalkTask(CrosstalkTask):
    """Remove crosstalk from a raw DECam image.

    This must be done after the overscan is corrected but before it is trimmed.
    This version of crosstalk removal assumes you want to do it as part of a
    regular stack-ISR workflow.
    """
    ConfigClass = DecamCrosstalkConfig
    _DefaultName = 'decamCrosstalk'

    def prepCrosstalk(self, dataRef, crosstalk=None):
        """Retrieve source image data and coefficients to prepare for crosstalk correction.

        This is called by readIsrData. The crosstalkSources land in isrData.

        Parameters
        ----------
        dataRef : `lsst.daf.persistence.butlerSubset.ButlerDataRef`
            DataRef of exposure to correct which must include a dataId with
            at least one visit and a ccdnum corresponding to the detector id.
        crosstalk : `lsst.ip.isr.CrosstalkCalib`
            Crosstalk calibration that will be used.

        Returns
        -------
        crosstalkSources : `defaultdict`
            Contains image data and corresponding crosstalk coefficients for
            each crosstalk source of the given dataRef victim.
        """
        # Define a butler to prepare for accessing crosstalk 'source' image data
        try:
            butler = dataRef.getButler()
        except RuntimeError:
            self.log.fatal('Cannot get a Butler from the dataRef provided')

        # If there is no interChip CT, then we're done.
        if crosstalk.interChip is None or len(crosstalk.interChip) == 0:
            return None

        # Retrieve visit and ccdnum from 'victim' so we can look up 'sources'
        visit = dataRef.dataId['visit']
        crosstalkSources = defaultdict(list)

        decamisr = IsrTask()  # needed for source_exposure overscan correction
        for sourceDet in crosstalk.interChip:
            try:
                source_exposure = butler.get('raw', dataId={'visit': visit, 'ccd': sourceDet})
            except RuntimeError:
                self.log.warn('Cannot access source %s, SKIPPING IT' % sourceDet)
            else:
                self.log.info('Correcting victim %s from crosstalk source %s' %
                              (crosstalk._detectorName, sourceDet))

                for amp in source_exposure.getDetector():
                    decamisr.overscanCorrection(source_exposure, amp)

                # Do not assemble here, as DECam CT is corrected before assembly.
                crosstalkSources[sourceDet] = source_exposure
        return crosstalkSources


class DecamCrosstalkIO(pipeBase.Task):
    """Remove crosstalk from a raw DECam Multi-Extension FITS file.

    This must be done after the overscan is corrected but before it is trimmed.
    NOTE: This version of crosstalk removal assumes you want to do it as an
    standalone file operation, not as part of a regular stack-ISR workflow.
    """
    ConfigClass = DecamCrosstalkConfig
    _DefaultName = 'decamCrosstalkIO'

    def parseCrosstalkIOArgs(self):
        """Parse command-line arguments to run the crosstalk correction alone.

        Examples
        --------
        runCrosstalkAlone.py -f decam0411673.fits.fz -o decam0411673_xtalk_corrected.fits.fz
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--filename',
                            help='Location on disk of the DECam MEF file you wish to crosstalk correct')
        parser.add_argument('-o', '--outfile',
                            help='Location on disk where crosstalk-corrected DECam MEF file will be saved')
        args = parser.parse_args()
        parsed = {'filename': args.filename, 'outfile': args.outfile}
        return parsed

    def runCrosstalkAlone(self):
        """Utility for crosstalk correction directly on a DECam MEF file.
        """
        log = lsst.log.Log.getLogger('obs.decam.DecamCrosstalkIO')
        parsed = self.parseCrosstalkIOArgs()
        filename = parsed['filename']
        outfile = parsed['outfile']
        mef = fits.open(filename)
        sources, coeffs = self.config.getSourcesAndCoeffs()
        corrected = subtractCrosstalkIO(mef, sources, coeffs)

        if outfile:
            corrected.writeto(outfile, overwrite=True)
        else:
            log.warning('No outfile specified, not writing corrected image to disk')


def subtractCrosstalkIO(mef, sources, coeffs):
    """Remove crosstalk from a DECam Multi-Extension FITS raw image.

    This version uses astropy I/O rather than the Butler due to the cross-amp
    crosstalk and ease of accessing Multi-Extension FITS data. It does not
    integrate with isr and does not use the Butler.

    WARNING: this will run fine on a non-overscan-corrected raw image, but the
    crosstalk coefficients were computed post-overscan-correction. Therefore,
    **the input raw image should be overscan corrected before this is run.**

    Parameters
    ----------
    mef : `astropy.io.fits.hdu.hdulist.HDUList`
        One DECam Multi-Extension FITS image.
    sources : `defaultdict`
        Crosstalk source areas affecting flux in a certain victim area.
    coeffs : `list`
        Linear crosstalk coefficients.

    Returns
    -------
    mef : `astropy.io.fits.hdu.hdulist.HDUList`
        New MEF image with crosstalk corrected data and updated header.
    """
    log = lsst.log.Log.getLogger('obs.decam.subtractCrosstalkIO')
    lowx = {}  # Lower x pixel index of given chip region
    highx = {}  # Upper x pixel index of given chip region
    extension = {}  # FITS extension of given chip position from CCDNUM header
    corrected = [0] * 63  # placeholder for corrected data

    for i in range(1, 63):
        ccd = '%02d' % mef[i].header['CCDNUM']
        extension[ccd] = i
        for section in 'AB':
            ccdsec_str = mef[i].header['DATASEC' + section]
            ccdsec_list = re.findall(r"[\w']+", ccdsec_str)
            lowx[ccd + section] = int(ccdsec_list[0]) - 1
            highx[ccd + section] = int(ccdsec_list[1])
        corrected[i] = mef[i].data.astype(np.float32)
    for ccd in ['%02d' % i for i in range(1, 63)]:
        for section in 'AB':
            victim = ccd + section
            victim_data = corrected[extension[ccd]][:, lowx[victim]:highx[victim]]
            for source in sources[victim]:
                source_data = mef[extension[source[:2]]].data[:, lowx[source]:highx[source]]
                if lowx[victim] != lowx[source]:
                    # If regions were read out on different sides of the CCD
                    # (i.e., an A and B mismatch) flip data in the x-direction
                    source_data = np.fliplr(source_data)
                # Perform linear crosstalk correction
                victim_data[:, :] = victim_data - coeffs[(victim, source)] * source_data
                log.info('Correcting victim %s from crosstalk source %s for HDU %s' % (victim, source, ccd))

    for i in range(1, 63):
        mef[i].header['HISTORY'] = 'Crosstalk corrected on {0}'.format(
            dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        mef[i] = fits.ImageHDU(header=mef[i].header, data=corrected[i])

    return mef
