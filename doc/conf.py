"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documenation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.obs.decam


_g = globals()
_g.update(build_package_configs(
    project_name='obs_decam',
    version=lsst.obs.decam.version.__version__))
