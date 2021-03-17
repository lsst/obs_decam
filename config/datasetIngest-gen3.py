# Config override for lsst.ap.verify.Gen3DatasetIngestTask

from lsst.obs.decam import DecamRawIngestTask

config.ingester.retarget(DecamRawIngestTask)
