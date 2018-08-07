# Config override for lsst.ap.association.AssociationTask
from lsst.ap.association import AssociationDBSqliteTask

config.level1_db.retarget(AssociationDBSqliteTask)
config.level1_db.filter_names = ['u', 'g', 'r', 'i', 'z', 'y', 'VR']

