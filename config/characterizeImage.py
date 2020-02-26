"""
DECam-specific overrides for CharacterizeImageTask
"""
config.repair.cosmicray.nCrPixelMax = 100000

# This sets the reference catalog name for Gen2.
# Note that in Gen3, we've stopped pretending (which is what Gen2 does,
# for backwards compatibility) that charImage uses a reference catalog.
config.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
# Note the u-band results may not be useful without a color term
config.refObjLoader.filterMap['u'] = 'g'
config.refObjLoader.filterMap['Y'] = 'y'
