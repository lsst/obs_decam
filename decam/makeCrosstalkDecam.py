#!/usr/bin/env python3
"""Convert a DECam crosstalk text table into LSST CrosstalkCalibs.
"""
import argparse
import numpy as np
import os.path
import sys

import lsst.ip.isr as ipIsr
from lsst.daf.base import PropertyList
from lsst.obs.decam import DecamMapper


def makeDetectorCrosstalk(dataDict, force=False):
    """Generate and write CrosstalkCalib from dictionary.

    Parameters
    ----------
    dataDict : `dict`
        Dictionary from ``readFile`` containing crosstalk definition.
    """
    dataDict['coeffs'] = dataDict['coeffs'].transpose()

    decamCT = ipIsr.crosstalk.CrosstalkCalib.fromDict(dataDict)
    # Supply a date prior to all data, to ensure universal use.
    decamCT.updateMetadata(setDate=False, CALIBDATE='1970-01-01T00:00:00')

    detName = dataDict['DETECTOR_NAME']
    outDir = os.path.join(DecamMapper.getCrosstalkDir(), detName.lower())
    if os.path.exists(outDir):
        if not force:
            print("Output directory %r exists; use --force to replace" % (outDir, ))
            sys.exit(1)
    else:
        os.makedirs(outDir)
    decamCT.writeText(f"{outDir}/1970-01-01T00:00:00.yaml")


def readFile(crosstalkInfile):
    """Construct crosstalk dictionary-of-dictionaries from crosstalkInfile.

    Parameters
    ----------
    crosstalkInfile : `str`
        File containing crosstalk coefficient information.

    Results
    -------
    outDict : `dict` [`str` : `dict`]
        Output dictionary, keyed on victim detector names, containing
        `lsst.ip.isr.CrosstalkCalib`'s expected dictionary format.

    Raises
    ------
    RuntimeError :
        Raised if the detector is not known.
    """
    ampIndexMap = {'A': 0, 'B': 1}
    detMap = {f"ccd{key:02d}": value for key, value in DecamMapper.detectorNames.items()}
    detMap['ccd61'] = 'N30'
    detSerialMap = {value: key for key, value in DecamMapper.detectorNames.items()}
    detSerialMap['N30'] = 61

    outDict = dict()
    with open(crosstalkInfile) as f:
        for line in f:
            li = line.strip()
            if not li.startswith('#'):
                elem = li.split()

                victimDetAmp = elem[0]
                sourceDetAmp = elem[1]
                coeff = float(elem[2])

                if 'A' in victimDetAmp:
                    victimAmp = 'A'
                elif 'B' in victimDetAmp:
                    victimAmp = 'B'
                else:
                    raise RuntimeError(f"Unknown amp: {victimDetAmp}")

                if 'A' in sourceDetAmp:
                    sourceAmp = 'A'
                elif 'B' in sourceDetAmp:
                    sourceAmp = 'B'
                else:
                    raise RuntimeError(f"Unknown amp: {sourceDetAmp}")

                victimDet = victimDetAmp.replace(victimAmp, "")
                sourceDet = sourceDetAmp.replace(sourceAmp, "")
                victimDet = detMap[victimDet]
                sourceDet = detMap[sourceDet]

                victimAmp = ampIndexMap[victimAmp]
                sourceAmp = ampIndexMap[sourceAmp]

                if victimDet not in outDict:
                    outDict[victimDet] = dict()
                    outDict[victimDet]['metadata'] = PropertyList()
                    outDict[victimDet]['metadata']['OBSTYPE'] = 'CROSSTALK'
                    outDict[victimDet]['metadata']['INSTRUME'] = 'DECam'
                    outDict[victimDet]['interChip'] = dict()
                    outDict[victimDet]['crosstalkShape'] = (2, 2)
                    outDict[victimDet]['hasCrosstalk'] = True
                    outDict[victimDet]['nAmp'] = 2
                    if 'coeffs' not in outDict[victimDet]:
                        # shape=outDict[victimDet]['crosstalkShape'])
                        outDict[victimDet]['coeffs'] = np.zeros_like([], shape=(2, 2))

                if sourceDet == victimDet:
                    outDict[victimDet]['metadata']['DETECTOR_NAME'] = victimDet
                    outDict[victimDet]['metadata']['DETECTOR_SERIAL'] = detSerialMap[victimDet]
                    outDict[victimDet]['metadata']['DETECTOR'] = detSerialMap[victimDet]
                    outDict[victimDet]['DETECTOR_NAME'] = victimDet
                    outDict[victimDet]['DETECTOR_SERIAL'] = detSerialMap[victimDet]
                    outDict[victimDet]['DETECTOR'] = detSerialMap[victimDet]
                    outDict[victimDet]['coeffs'][victimAmp][sourceAmp] = coeff
                else:
                    if sourceDet not in outDict[victimDet]['interChip']:
                        outDict[victimDet]['interChip'][sourceDet] = np.zeros_like([], shape=(2, 2))
                    outDict[victimDet]['interChip'][sourceDet][victimAmp][sourceAmp] = coeff
    return outDict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a DECam crosstalk file into LSST CrosstalkCalibs.")
    parser.add_argument(dest="crosstalkInfile", help="DECam crosstalk file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print data about each detector.")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing CrosstalkCalibs.")
    cmd = parser.parse_args()

    outDict = readFile(crosstalkInfile=cmd.crosstalkInfile)

    crosstalkDir = DecamMapper.getCrosstalkDir()
    if os.path.exists(crosstalkDir):
        if not cmd.force:
            print("Output directory %r exists; use --force to replace" % (crosstalkDir, ))
            sys.exit(1)
        print("Replacing data in crosstalk directory %r" % (crosstalkDir, ))
    else:
        print("Creating crosstalk directory %r" % (crosstalkDir, ))
        os.makedirs(crosstalkDir)
    for detName in outDict:
        if cmd.verbose:
            print(f"{detName}: has crosstalk? {outDict[detName]['hasCrosstalk']}")
            print(f"COEFF:\n{outDict[detName]['coeffs']}")
            for source in outDict[detName]['interChip']:
                print(f"INTERCHIP {source}:\n{outDict[detName]['interChip'][source]}")
        makeDetectorCrosstalk(dataDict=outDict[detName], force=cmd.force)
