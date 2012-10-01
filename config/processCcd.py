from lsst.obs.decam.isr import DecamIsrTask
root.isr.retarget(DecamIsrTask)
root.isr.doBias = False
root.isr.doDark = False
root.isr.doFlat = False # Just for now...
root.isr.doWrite = False
root.isr.assembleCcd.setGain = False


root.calibrate.repair.doCosmicRay = False # Currently troublesome: lots of pixels that need to be masked first
root.calibrate.repair.cosmicray.nCrPixelMax = 100000
