import sys
from lsst.utils import getPackageDir
from lsst.daf.persistence import Butler
from lsst.ip.isr.isr import updateVariance, makeThresholdMask, maskPixelsFromDefectList
from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask
import os
import pdb

def setupButler():
    datadir= getPackageDir('testdata_mosaic')
    repoPath=os.path.join(datadir, 'rawData')
    butler=Butler(root=repoPath)
    dataId={"field":'F2', "subfield":'p23', "filter":"R", "dateObs":'2003-01-04', "objname":'obj074', 'hdu':1, 'ccdnum':1}
    exp=butler.get('exp', dataId)
    return {"butler":butler, "exp":exp, "dataId":dataId}

def updateVar(exp):
    ccd=exp.getDetector()[0]
    gain=ccd.getGain()
    readNoise=ccd.getReadNoise()
    readNoise_ADU=readNoise/gain
    updateVariance(exp.getMaskedImage(), gain, readNoise_ADU)


def charIm(butler,exp, dataId):
    dataRef=butler.dataRef('exp', dataId=dataId)
    charIm=CharacterizeImageTask()
    charIm.run(dataRef, exposure=exp, doUnpersist=False)

def run(uV=False, cI=True):
    setupOut=setupButler()
    butler=setupOut['butler']
    exp=setupOut['exp']
    dataId=setupOut['dataId']
    if uV==True:
        print "updating variance plane"
        updateVar(exp)
    if cI==True:
        print "characterizing image"
        charIm(butler, exp, dataId)

if __name__ == '__main__':
    if len(sys.argv)<=1:
        run()
    else:
        if sys.argv[1]=='True':
            uV_bool=True
        else:
            uV_bool=False
        if sys.argv[2]=='True':
            cI_bool=True
        else:
            cI_bool=False

        run(uV=uV_bool, cI=cI_bool)
