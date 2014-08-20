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

if __name__ == "__main__":
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
                    # Extract original source schema, which we will add to using a schema mapper
                    schema = src.getSchema()
                    smapper = afwTable.SchemaMapper(schema)
                    smapper.addMinimalSchema(schema, True)

                    # Define what we will add to the schema for
                    # calibrated aperture and psf fluxes.  NOTE: when
                    # using lightcurves we always want to e.g. average
                    # in fluxes and convert to mags afterwards
                    apCalKey = smapper.editOutputSchema().addField("flux.ap.cal", type=np.float)
                    psfCalKey = smapper.editOutputSchema().addField("flux.psf.cal", type=np.float)
                    visitKey = smapper.editOutputSchema().addField("visit", type=np.int)
                    taiKey = smapper.editOutputSchema().addField("mjd.tai", type=np.double)
                    
                    # Create a source table with the modified source schema
                    st = afwTable.SourceTable.make(smapper.getOutputSchema())

                    # Extract deblender keys
                    nChildKey = st.schema.find("deblend.nchild").key
                    tooManyKey = st.schema.find("deblend.too-many-peaks").key
                    failedKey = st.schema.find("deblend.failed").key

                    # Define what we intend to use for the aperture and psf fluxes
                    st.defineApFlux("flux.sinc")
                    st.definePsfFlux("flux.psf")
                    psfKey = st.getPsfFluxKey()
                    apKey = st.getApFluxKey()

                    # Create a source catalog with this modified schema
                    cat = afwTable.SourceCatalog(st)

                # Skip deblending errors
                deblendSlice = (~(src.get(tooManyKey) | src.get(failedKey) | src.get(nChildKey)>0))
                subSrc = src[deblendSlice]

                if doPlot:
                    plt.plot([x.getCoord()[0] for x in subSrc], [y.getCoord()[0] for y in subSrc], "%so"%(colors[cidx]))

                # Create a temporary catalog with the new schema, and update the fields
                tmp = afwTable.SourceCatalog(cat.getTable())
                tmp.extend(subSrc, mapper=smapper)
                tmp[taiKey][:] = tc
                tmp[visitKey][:] = visit
                tmp[apCalKey][:] = tmp.get(apKey)/fmagzero
                tmp[psfCalKey][:] = tmp.get(psfKey)/fmagzero

                # Extend the master catalog with this updated data; shallow copy
                cat.extend(tmp, False)

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
            print "Cluster %d, source %d, flux = %.3f %.3f, visit=%d mjd.tai=%f" % (c, s, src.get(apKey), src.get(psfKey), src.get(visitKey), src.get(taiKey))
            afluxes.append(src.get(apCalKey))
            pfluxes.append(src.get(psfCalKey))
        afluxes = np.array(afluxes)
        pfluxes = np.array(pfluxes)

        aIdx = np.isfinite(afluxes)
        aMed = np.median(afluxes[aIdx])
        aStd = 0.741 * (np.percentile(afluxes[aIdx], 75) - np.percentile(afluxes[aIdx], 25))

        pIdx = np.isfinite(pfluxes)
        pMed = np.median(pfluxes[pIdx])
        pStd = 0.741 * (np.percentile(pfluxes[pIdx], 75) - np.percentile(pfluxes[pIdx], 25))

        print "Cluster %d, mean ap mag = %.3f, std = %.3f, mean psf mag = %.3f +/- %.3f" % (c, -2.5*np.log10(aMed), 2.5/np.log(10.0)*aStd/aMed,
                                                                                               -2.5*np.log10(pMed), 2.5/np.log(10.0)*pStd/pMed)
        print
