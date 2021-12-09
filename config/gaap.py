# Enable GAaP (Gaussian Aperture and PSF) colors
# 'config' is typically a SourceMeasurementConfig
try:
    import lsst.meas.extensions.gaap  # noqa
    config.plugins.names.add("ext_gaap_GaapFlux")
    config.plugins["ext_gaap_GaapFlux"].sigmas = [0.5, 0.7, 1.0, 1.5, 2.5, 3.0]
    # Enable PSF photometry after PSF-Gaussianization in the `ext_gaap_GaapFlux` plugin
    config.plugins["ext_gaap_GaapFlux"].doPsfPhotometry = True
except ImportError as exc:
    import logging
    logging.getLogger("lsst.obs.decam.config").warning("Cannot import lsst.meas.extensions.gaap (%s):"
                                                       " disabling GAaP flux measurements", exc)
