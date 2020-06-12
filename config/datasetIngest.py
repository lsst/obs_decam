# Config override for lsst.ap.verify.DatasetIngestTask
import os.path

from lsst.utils import getPackageDir
from lsst.obs.decam.ingest import DecamIngestTask

decamConfigDir = os.path.dirname(__file__)

# Can't refer to os.path.join inside list comprehension
config.curatedCalibPaths = []
for calibType in {'defects', 'crosstalk'}:
    config.curatedCalibPaths.append(os.path.join(getPackageDir('obs_decam_data'), 'decam', calibType))
config.dataIngester.retarget(DecamIngestTask)
config.dataIngester.load(os.path.join(decamConfigDir, 'ingest.py'))
config.calibIngester.load(os.path.join(decamConfigDir, 'ingestCalibs.py'))
config.curatedCalibIngester.load(os.path.join(decamConfigDir, 'ingestCuratedCalibs.py'))
config.curatedCalibIngester.parse.extnames = []
