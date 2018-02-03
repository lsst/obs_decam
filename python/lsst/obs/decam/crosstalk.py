#
# LSST Data Management System
# Copyright 2018 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

"""Apply crosstalk corrections to raw DECam images.

Some of this code is based on DECam_crosstalk.py, used for the THELI pipeline
and written by Thomas Erben (private communication, 2018)
"""

from __future__ import absolute_import, division, print_function

from collections import defaultdict
from astropy.io import fits
import datetime as dt
import os
import argparse
import re
import numpy as np

import lsst.log
import lsst.pipe.base as pipeBase
import lsst.pex.config as pexConfig
from lsst.ip.isr import CrosstalkConfig, CrosstalkTask
from lsst.obs.decam import DecamMapper
from lsst.utils import getPackageDir
import lsst.afw.math as afwMath
from lsst.obs.base import exposureFromImage
#from .isr import DecamIsrTask

__all__ = ["DecamCrosstalkTask", "runCrosstalkAlone"]


class DecamCrosstalkConfig(CrosstalkConfig):
    """Configuration for DECam crosstalk removal
    """
    extensions = pexConfig.DictField(
        keytype=str, itemtype=int,
        doc="FITS extension of given chip position from CCDNUM header",
        default={'25': 1, '26': 2, '27': 3, '32': 4, '33': 5, '34': 6, '19': 7,
                 '20': 8, '13': 9, '14': 10, '08': 11, '04': 12, '39': 13,
                 '40': 14, '45': 15, '46': 16, '51': 17, '56': 18, '21': 19,
                 '22': 20, '23': 21, '24': 22, '17': 23, '18': 24, '15': 25,
                 '16': 26, '09': 27, '10': 28, '11': 29, '12': 30, '05': 31,
                 '06': 32, '07': 33, '01': 34, '02': 35, '03': 36, '35': 37,
                 '36': 38, '37': 39, '38': 40, '28': 41, '29': 42, '30': 43,
                 '31': 44, '41': 45, '42': 46, '43': 47, '44': 48, '49': 49,
                 '50': 50, '47': 51, '48': 52, '52': 53, '53': 54, '54': 55,
                 '55': 56, '57': 57, '58': 58, '59': 59, '60': 60, '61': 61,
                 '62': 62},
    )

    def getSourcesAndCoeffsFile(self, filename='DECam_xtalk_20130606.txt'):
        """Return directory containing the DECam_xtalk_20130606.txt file.

        File containing DECam crosstalk coefficients. This text file is
        provided by NOAO in a particular format with information
        about the DECam crosstalk coefficients. It is available at
        http://www.ctio.noao.edu/noao/content/DECam-Calibration-Files
        """
        mapper = DecamMapper()
        packageName = mapper.getPackageName()
        packageDir = getPackageDir(packageName)
        return os.path.join(packageDir, 'decam', filename)

    def getSourcesAndCoeffs(self):
        """Read crosstalk sources and coefficients from DECam-specific file
        """
        crosstalk_file = self.getSourcesAndCoeffsFile()
        sources = defaultdict(list)
        coeffs = {}
        log = lsst.log.Log.getLogger('obs.decam.DecamCrosstalkConfig')
        log.info('Reading crosstalk coefficient data')
        for line in open(crosstalk_file):
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

    @pipeBase.timeMethod
    def run(self, exposure, dataRef):
        """Perform crosstalk correction on a DECam exposure and a corresponding dataRef

        Parameters
        ----------
        exposure : `lsst.afw.image.Exposure`
            Exposure to correct
        dataRef : `lsst.daf.persistence.butlerSubset.ButlerDataRef`
            DataRef of exposure to correct which must include a dataId
            with at least one visit and ccdnum

        Returns
        -------
        `pipeBase.Struct`
            Struct contains field "exposure," which is the exposure after
            crosstalk correction has been applied
        """
        self.log.info('Applying crosstalk correction')
        sources, coeffs = self.config.getSourcesAndCoeffs()
        corrected = self.subtractCrosstalk(dataRef, sources, coeffs, self.config.extensions)
        corrected = exposureFromImage(corrected)
        metadata = corrected.getMetadata()
        metadata.set('CROSSTALK', 'Crosstalk corrected on {0}'.format(
                        dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))
        corrected.setMetadata(metadata)
        return pipeBase.Struct(
            exposure=corrected,
        )

        # TODO: decide what needs returning where
        #       ensure crosstalk is actually being corrected
        #       write some tests
        #       plug this into the DECam ISR workflow and try it out
        #       -> there is dataRef vs. exposure problem in isr.py
        #       -> apparently I'm not using the Butler "properly"

    def subtractCrosstalk(self, dataRef, sources, coeffs, extensions):
        """Remove crosstalk from an overscan-corrected raw DECam image.

        Parameters
        ----------
        exposure : `lsst.afw.image.Exposure`
            Exposure to correct
        dataRef : `lsst.daf.persistence.butlerSubset.ButlerDataRef`
            DataRef of exposure to process which must include a dataId
            with at least one visit and ccdnum
        sources : `defaultdict`
            Crosstalk source areas affecting flux in a certain victim area
        coeffs : `list`
            Linear crosstalk coefficients

        Returns
        -------
        `lsst.afw.image.Exposure`
            Exposure containing image data that has been crosstalk corrected
        """
        log = lsst.log.Log.getLogger('obs.decam.subtractCrosstalk')
        #import ipdb; ipdb.set_trace()
        butler = dataRef.getButler()  # needed to load a different exposure later
        dataId = dataRef.dataId
        image = exposure.getMaskedImage().getImage()
        ccdnum = int(dataId['ccdnum'])
        visit = dataId['visit']
        ccdnum_str = '%02d' % ccdnum

        for amp in exposure.getDetector():
            if not exposure.getMetadata().exists('OVERSCAN'):
                # Check to see if overscan has been corrected, and if not, correct it
                from .isr import DecamIsrTask
                decamisr = DecamIsrTask()
                decamisr.overscanCorrection(exposure, amp)
                log.info('Correcting overscan before crosstalk')
            section = amp.getName()
            victim = ccdnum_str + section

        for amp in exposure.getDetector():
            section = amp.getName()
            victim = ccdnum_str + section
            dataBBox = amp.getRawDataBBox()
            victim_data = image.Factory(image, dataBBox)
            for source in sources[victim]:
                source_ccdnum = extensions[source[:2]]
                source_exposure = butler.get('raw', dataId={'visit': visit, 'ccdnum': source_ccdnum})
                source_image = source_exposure.getMaskedImage().getImage()
                if 'A' in source:
                    source_dataBBox = source_exposure.getDetector()[0].getRawDataBBox()
                elif 'B' in source:
                    source_dataBBox = source_exposure.getDetector()[1].getRawDataBBox()
                source_data = source_image.Factory(source_image, source_dataBBox)
                if victim_data.getX0() != source_data.getX0():
                    # Occurs with amp A and B mismatch; need to flip horizontally
                    source_data = afwMath.flipImage(source_data, flipLR=True, flipTB=False)
                # Perform linear crosstalk correction
                source_data *= coeffs[(victim, source)]
                victim_data -= source_data
                log.info('Correcting victim %s from crosstalk source %s for CCDNUM %s' %
                         (victim, source, ccdnum))
        return image


class DecamCrosstalkIO(pipeBase.Task):
    """Remove crosstalk from a raw DECam Multi-Extension FITS file.

    This must be done after the overscan is corrected but before it is trimmed.
    NOTE: This version of crosstalk removal assumes you want to do it as an
    standalone file operation, not as part of a regular stack-ISR workflow.
    """
    ConfigClass = DecamCrosstalkConfig
    _DefaultName = 'decamCrosstalkIO'

    def parseCrosstalkIOArgs(self):
        """Parse command-line arguments to run the crosstalk correction alone

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
        """Utility for crosstalk correction directly on a DECam MEF file
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
        One DECam Multi-Extension FITS image
    sources : `defaultdict`
        Crosstalk source areas affecting flux in a certain victim area
    coeffs : `list`
        Linear crosstalk coefficients

    Returns
    -------
    mef : `astropy.io.fits.hdu.hdulist.HDUList`
        New MEF image with crosstalk corrected data and updated header
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
