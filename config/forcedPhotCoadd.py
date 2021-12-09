import os.path

from lsst.meas.base import CircularApertureFluxAlgorithm

config.measurement.load(os.path.join(os.path.dirname(__file__), "apertures.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "kron.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "convolvedFluxes.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "gaap.py"))
config.load(os.path.join(os.path.dirname(__file__), "cmodel.py"))

# These configs match obs_subaru, to facilitate 1:1 comparisons between DECam and HSC
config.catalogCalculation.plugins.names = ["base_ClassificationExtendedness"]
config.measurement.slots.psfFlux = "base_PsfFlux"

def doUndeblended(config, algName, fluxList=None):
    """Activate undeblended measurements of algorithm

    Parameters
    ----------
    algName : `str`
        Algorithm name.
    fluxList : `list` of `str`, or `None`
        List of flux columns to register for aperture correction. If `None`,
        then this will be the `algName` appended with `_instFlux`.
    """
    if algName not in config.measurement.plugins:
        return
    if fluxList is None:
        fluxList = [algName + "_instFlux"]
    config.measurement.undeblended.names.add(algName)
    config.measurement.undeblended[algName] = config.measurement.plugins[algName]
    for flux in fluxList:
        config.applyApCorr.proxies["undeblended_" + flux] = flux


# These configs match obs_subaru, to facilitate 1:1 comparisons between DECam and HSC
doUndeblended(config, "base_PsfFlux")
doUndeblended(config, "ext_photometryKron_KronFlux")
doUndeblended(config, "base_CircularApertureFlux", [])  # No aperture correction for circular apertures
doUndeblended(config, "ext_convolved_ConvolvedFlux",
              config.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames())
doUndeblended(config, "ext_gaap_GaapFlux",
              config.measurement.plugins["ext_gaap_GaapFlux"].getAllGaapResultNames())
# Disable registration for apCorr of undeblended convolved; apCorr will be done through the deblended proxy
config.measurement.undeblended["ext_convolved_ConvolvedFlux"].registerForApCorr = False
config.measurement.undeblended["ext_gaap_GaapFlux"].registerForApCorr = False
