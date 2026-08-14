# Mapping of camera filter name: reference catalog filter name
# This file is appropriate for the_monster.
# It is adapted from obs_lsst/config/lsstCam/filterMap.py for DECam.

for source, target in [
    ("u", "monster_SDSS_u"),
    ("g", "monster_DES_g"),
    ("r", "monster_DES_r"),
    ("i", "monster_DES_i"),
    ("z", "monster_DES_z"),
    ("Y", "monster_DES_y"),
    ("N419", "monster_DES_g"),
    ("N540", "monster_DES_g"),
    ("N708", "monster_DES_i"),
    ("N964", "monster_DES_z"),
]:
    config.filterMap[source] = target
