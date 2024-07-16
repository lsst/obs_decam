# Enable measurement of convolved fluxes
# 'config' is a SourceMeasurementConfig
try:
    import lsst.meas.extensions.convolved  # noqa: F401 Required for ConvolvedFlux below
except ImportError as exc:
    import logging

    logging.getLogger("lsst.obs.decam.config").warning(
        "Cannot import lsst.meas.extensions.convolved (%s): disabling convolved flux measurements", exc
    )
else:
    config.plugins.names.add("ext_convolved_ConvolvedFlux")
    config.plugins["ext_convolved_ConvolvedFlux"].seeing.append(8.0)
