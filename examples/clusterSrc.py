import sys
from lsst.obs.decam.decamMapper import DecamInstcalMapper as Mapper
import lsst.daf.persistence as dafPersist
import lsst.afw.detection as afwDet
import lsst.ap.cluster as apCluster
import lsst.afw.table as afwTable
import numpy as np

def getSrc(visit, ccdnum, butler):
    dataId = {"visit": visit, "ccdnum": ccdnum}

if __name__ == "__main__":
    root   = sys.argv[1]
    mapper = Mapper(root = root, calibRoot = None, outputRoot = None)
    butler = dafPersist.ButlerFactory(mapper = mapper).create()

    # Master source catalog
    cat    = None
    
    for visit in sys.argv[2:]:
        visitKeys = mapper.registry.executeQuery(["visit", "ccdnum"], ["raw",], [("visit", "?")], None, (visit,))
        for key in visitKeys:
            visit, ccdnum = key
            dataId = {"visit": visit, "ccdnum": ccdnum}
            if butler.datasetExists(datasetType="src", dataId=dataId):
                src = butler.get(datasetType="src", dataId=dataId)
                calexp = butler.get(datasetType="calexp", dataId=dataId)
                fmagzero = calexp.getCalib().getFluxMag0()[0]
                if cat is None:
                    # Create a source table with the default source schema
                    st = afwTable.SourceTable.make(src.getSchema())

                    # Define what we intend to use for the aperture and psf fluxes
                    st.defineApFlux("flux.sinc")
                    st.definePsfFlux("flux.psf")
                    psfKey = st.getPsfFluxKey()
                    apKey = st.getApFluxKey()

                    # Define what we will add to the schema for
                    # calibrated aperture and psf fluxes.  NOTE: when
                    # using lightcurves we always want to e.g. average
                    # in fluxes and convert to mags afterwards
                    apCalKey = st.schema.addField("flux.ap.cal", type="D")
                    psfCalKey = st.schema.addField("flux.psf.cal", type="D")

                    # Create a source catalog with this modified schema
                    cat = afwTable.SourceCatalog(st)
                for s in src:
                    # Provide calibrated fluxes
                    s.set(apCalKey, s.get(apKey)/fmagzero)
                    s.set(psfCalKey, s.get(psfKey)/fmagzero)
                    cat.append(s)

    nepochs = len(sys.argv)-2
    cfg = apCluster.ClusteringConfig()
    cfg.minNeighbors = int(0.80 * nepochs + 0.5)
    cfg.epsilonArcsec = 0.5
    clusters = apCluster.cluster(cat, cfg.makeControl())

    for c, cluster in enumerate(clusters):
        mags = []
        for s, src in enumerate(cluster):
            print "Cluster %d, source %d, flux = %.3f" % (c, s, src.get(psfKey))
            mags.append(-2.5 * np.log10(src.get(psfCalKey)))
        print "Cluster %d, mean mag = %.3f, std = %.3f" % (c, np.mean(mags), np.std(mags))
