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
                if cat is None:
                    st = afwTable.SourceTable.make(src.getSchema())
                    cat = afwTable.SourceCatalog(st)
                for s in src:
                    cat.append(s)

    nepochs = len(sys.argv)-2
    cfg = apCluster.ClusteringConfig()
    cfg.minNeighbors = int(0.80 * nepochs + 0.5)
    cfg.epsilonArcsec = 0.5
    clusters = apCluster.cluster(cat, cfg.makeControl())

    for c, cluster in enumerate(clusters):
        mags = []
        for s, src in enumerate(cluster):
            print "Cluster %d, source %d, flux = %.3f" % (c, s, src.getPsfFlux())
            mags.append(-2.5 * np.log10(src.getPsfFlux()))
        print "Cluster %d, mean mag = %.3f, std = %.3f" % (c, np.mean(mags), np.std(mags))
