# Refcats
config.connections.photometry_ref_cat = "the_monster_20250219"
config.connections.astrometry_ref_cat = "the_monster_20250219"

config.photometry.photoCatName = "the_monster_20250219"
config.photometry_ref_loader.load("filterMap.py")

config.photometry.applyColorTerms = False

config.psf_source_measurement.plugins["base_Jacobian"].pixelScale = 0.263
config.psf_source_measurement.undeblended["base_Jacobian"].pixelScale = 0.263
config.star_measurement.plugins["base_Jacobian"].pixelScale = 0.263
config.star_measurement.undeblended["base_Jacobian"].pixelScale = 0.263
