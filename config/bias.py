import os.path

config.isr.load(os.path.join(os.path.dirname(__file__), "isr.py"))
config.isr.doBias = False
config.isr.doFlat = False
config.isr.doDark = False
config.isr.doFringe = False

config.dateObs = "date"
config.ccdKeys = ["ccdnum"]
