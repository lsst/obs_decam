from lsst.obs.decam.isr import DecamIsrTask
config.isr.retarget(DecamIsrTask)

config.isr.doDark = False
config.isr.fringe.filters = ['z', 'y']
config.isr.assembleCcd.keysToRemove = ['DATASECA', 'DATASECB',
                                       'TRIMSECA', 'TRIMSECB',
                                       'BIASSECA', 'BIASSECB',
                                       'PRESECA', 'PRESECB',
                                       'POSTSECA', 'POSTSECB']

config.charImage.repair.cosmicray.nCrPixelMax = 100000
