from lsst.obs.decam.decamCpIsr import DecamCpIsrTask
config.isr.retarget(DecamCpIsrTask)

config.isr.doDark = False
config.isr.fringe.filters = ['z', 'y']
config.isr.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                       'TRIMSECA', 'TRIMSECB',
                                       'BIASSECA', 'BIASSECB',
                                       'PRESECA', 'PRESECB',
                                       'POSTSECA', 'POSTSECB']

config.charImage.repair.cosmicray.nCrPixelMax = 100000
config.isr.assembleCcd.setGain=False
config.charImage.refObjLoader.filterMap={'u':'J', 'g':'J', 'r':'J', 'i': 'J', 'z':'J', 'y': 'J'}
config.calibrate.refObjLoader.filterMap={'u':'J', 'g':'J', 'r':'J', 'i': 'J', 'z':'J', 'y': 'J'}
