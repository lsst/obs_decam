from lsst.obs.sst.isr import SstIsrTask
root.isr.retarget(SstIsrTask)

root.isr.doBias = False
root.isr.doDark = True
root.isr.doFlat = True
root.isr.assembleCcd.setGain = False
