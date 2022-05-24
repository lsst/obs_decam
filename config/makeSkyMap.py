config.skyMap = "rings"

# Configuration for DiscreteSkyMap
# 0: ACTJ0022M0036
# 1: M31
config.skyMap["discrete"].raList = [5.5, 10.7]  # degrees
config.skyMap["discrete"].decList = [-0.6, 41.3]  # degrees
config.skyMap["discrete"].radiusList = [0.5, 0.8]  # degrees
config.skyMap["discrete"].pixelScale = 0.262  # arcsec/pixel

# Configuration for RingsSkyMap
config.skyMap["rings"].numRings = 120
config.skyMap["rings"].projection = "TAN"
config.skyMap["rings"].tractOverlap = 1.0/60  # Overlap between tracts (degrees)
config.skyMap["rings"].pixelScale = 0.262  # arcsec/pixel
