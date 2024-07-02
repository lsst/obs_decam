# Enable Kron mags
# 'config' is a SourceMeasurementConfig

try:
    import lsst.meas.extensions.photometryKron  # noqa: F401 required for KronFlux below

    config.plugins.names |= ["ext_photometryKron_KronFlux"]
except ImportError:
    import logging

    logging.getLogger("lsst.obs.decam.config").warning(
        "Cannot import lsst.meas.extensions.photometryKron: disabling Kron measurements"
    )
