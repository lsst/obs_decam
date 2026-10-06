config.measurement.load("apertures.py")
config.measurement.load("kron.py")
config.measurement.load("convolvedFluxes.py")
config.measurement.load("hsm.py")
config.load("cmodel.py")
config.measurement.plugins.names |= ["base_InputCount"]
