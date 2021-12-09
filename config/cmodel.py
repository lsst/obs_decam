# Enable CModel mags (unsetup meas_modelfit to disable)
# 'config' is a SourceMeasurementConfig.
try:
    import lsst.meas.modelfit
    config.measurement.plugins.names |= ["modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]
    config.measurement.slots.modelFlux = 'modelfit_CModel'
    config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio = 0.985
except (KeyError, ImportError):
    import logging
    logging.getLogger("lsst.obs.decam.config").warning("Cannot import lsst.meas.modelfit:"
                                                       " disabling CModel measurements")
