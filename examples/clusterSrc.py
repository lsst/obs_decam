import sys
from lsst.obs.decam.decamMapper import DecamInstcalMapper as Mapper
import lsst.daf.persistence as dafPersist
import lsst.daf.base as dafBase
import lsst.afw.detection as afwDet
import lsst.ap.cluster as apCluster
import lsst.afw.table as afwTable
import numpy as np
import matplotlib.pyplot as plt

doPlot = False

def getSrc(visit, ccdnum, butler):
    dataId = {"visit": visit, "ccdnum": ccdnum}

if __name__ == "__main__":
    import pdb; pdb.set_trace()
    root   = sys.argv[1]
    mapper = Mapper(root = root, calibRoot = None, outputRoot = None)
    butler = dafPersist.ButlerFactory(mapper = mapper).create()

    # Master source catalog
    cat    = None
    
    if doPlot:
        fig = plt.figure()

    colors = ["r", "b"]
    cidx = -1
    for visit in sys.argv[2:]:
        cidx += 1
        visitKeys = mapper.registry.executeQuery(["visit", "ccdnum"], ["raw",], [("visit", "?")], None, (visit,))
        for key in visitKeys:
            visit, ccdnum = key
            if ccdnum != 10: continue
            dataId = {"visit": visit, "ccdnum": ccdnum}
            if butler.datasetExists(datasetType="src", dataId=dataId):
                print "READING", dataId
                src = butler.get(datasetType="src", dataId=dataId)
                calexp = butler.get(datasetType="calexp", dataId=dataId)
                fmagzero = calexp.getCalib().getFluxMag0()[0]
                tc = calexp.getCalib().getMidTime().get(dafBase.DateTime.MJD, dafBase.DateTime.TAI)
                if cat is None:
                    # Extract original source schema, which we will add to
                    schema = src.getSchema()

                    # Define what we will add to the schema for
                    # calibrated aperture and psf fluxes.  NOTE: when
                    # using lightcurves we always want to e.g. average
                    # in fluxes and convert to mags afterwards
                    apCalKey = schema.addField("flux.ap.cal", type=np.float)
                    psfCalKey = schema.addField("flux.psf.cal", type=np.float)
                    visitKey = schema.addField("visit", type=np.int)
                    taiKey = schema.addField("mjd.tai", type=np.double)
                    print apCalKey, psfCalKey, visitKey, taiKey
                    
                    # Extract deblender keys
                    nChildKey = schema.find("deblend.nchild").key
                    tooManyKey = schema.find("deblend.too-many-peaks").key
                    failedKey = schema.find("deblend.failed").key
                    print nChildKey, tooManyKey, failedKey

                    # Create a source table with the modified source schema
                    st = afwTable.SourceTable.make(schema)

                    # Define what we intend to use for the aperture and psf fluxes
                    st.defineApFlux("flux.sinc")
                    st.definePsfFlux("flux.psf")
                    psfKey = st.getPsfFluxKey()
                    apKey = st.getApFluxKey()

                    # Create a source catalog with this modified schema
                    cat = afwTable.SourceCatalog(st)

                for s in src:
                    # Skip deblending errors
                    print "DEBLEND"
                    if s.get(tooManyKey) or s.get(failedKey) or (s.get(nChildKey)>0):
                        continue
                    print "DEBLEND DONE"

                    if doPlot:
                        plt.plot(s.getCoord()[0], s.getCoord()[1], "%so"%(colors[cidx]))

                    # Provide calibrated fluxes
                    s.set(apCalKey, s.get(apKey)/fmagzero)
                    s.set(psfCalKey, s.get(psfKey)/fmagzero)
                    s.set(visitKey, visit)
                    s.set(taiKey, tc)
                    print "APPENDING"
                    cat.append(s)
                print "DONE"
            else:
                print "UNABLE TO FIND", dataId

    if len(cat) == 0:
        print "NO DATA!"
        sys.exit(1)
    nepochs = len(sys.argv)-2
    cfg = apCluster.ClusteringConfig()
    cfg.minNeighbors = int(0.80 * nepochs + 0.5)
    cfg.epsilonArcsec = 1.0
    clusters = apCluster.cluster(cat, cfg.makeControl())

    for c, cluster in enumerate(clusters):
        if len(cluster) == 1:
            continue
        afluxes= []
        pfluxes= []
        for s, src in enumerate(cluster):
            print "Cluster %d, source %d, flux = %.3f %.3f" % (c, s, src.get(apKey), src.get(psfKey))
            afluxes.append(src.get(apCalKey))
            pfluxes.append(src.get(psfCalKey))

        aMed = np.median(afluxes)
        aStd = 0.741 * (np.percentile(afluxes, 75) - np.percentile(afluxes, 25))
        pMed = np.median(pfluxes)
        pStd = 0.741 * (np.percentile(pfluxes, 75) - np.percentile(pfluxes, 25))
        print aMed, aStd, pMed, pStd
        print "Cluster %d, mean ap mag = %.3f, std = %.3f, mean psf mag = %.3f +/- %.3f" % (c, -2.5*np.log10(aMed), 2.5/np.log(10.0)*aStd/aMed,
                                                                                               -2.5*np.log10(pMed), 2.5/np.log(10.0)*pStd/pMed)
