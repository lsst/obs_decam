# Config override for lsst.ap.verify.DatasetIngestTask
import os.path

from lsst.utils import getPackageDir
from lsst.obs.decam.ingest import DecamIngestTask

decamConfigDir = os.path.join(getPackageDir('obs_decam'), 'config')

config.textDefectPath = os.path.join(getPackageDir('obs_decam_data'), 'decam', 'defects')
config.dataIngester.retarget(DecamIngestTask)
config.dataIngester.load(os.path.join(decamConfigDir, 'ingest.py'))
config.calibIngester.load(os.path.join(decamConfigDir, 'ingestCalibs.py'))
config.defectIngester.load(os.path.join(decamConfigDir, 'ingestStdTextCalibs.py'))
config.defectIngester.parse.extnames = []

