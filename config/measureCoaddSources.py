import os.path

config.measurement.load(os.path.join(os.path.dirname(__file__), "apertures.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "kron.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "convolvedFluxes.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "hsm.py"))
config.load(os.path.join(os.path.dirname(__file__), "cmodel.py"))

# Set reference catalog for Gen2.
config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
# Set reference catalog for Gen3.
config.connections.refCat = "ps1_pv3_3pi_20170110"

config.match.refObjLoader.load(os.path.join(os.path.dirname(__file__), "filterMap.py"))

config.doWriteMatchesDenormalized = True

config.measurement.plugins.names |= ["base_InputCount"]
