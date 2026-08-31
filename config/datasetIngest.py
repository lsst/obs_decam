# Config override for lsst.ap.verify.DatasetIngestTask
import os.path
from lsst.utils import getPackageDir
from lsst.obs.decam.ingest import DecamIngestTask

config.curatedCalibPaths = []
for calibType in {"defects", "crosstalk"}:
    config.curatedCalibPaths.append(
        os.path.join(getPackageDir("obs_decam_data"), "decam", calibType)
    )
config.dataIngester.retarget(DecamIngestTask)
config.dataIngester.load("ingest.py")
config.calibIngester.load("ingestCalibs.py")
config.curatedCalibIngester.load("ingestCuratedCalibs.py")
config.curatedCalibIngester.parse.extnames = []
