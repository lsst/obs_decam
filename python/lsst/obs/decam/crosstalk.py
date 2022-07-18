#
# This file is part of obs_decam.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# Copyright 2018 LSST Corporation.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Apply crosstalk corrections to DECam images.

Deprecated, see ip_isr crosstalk correction.
"""
from lsst.ip.isr import CrosstalkConfig, CrosstalkTask

from deprecated.sphinx import deprecated


__all__ = ["DecamCrosstalkTask"]


@deprecated(reason="This method is no longer used.  Please use lsst.ip.isr.CrosstalkConfig",
            version="v24.0", category=FutureWarning)
class DecamCrosstalkConfig(CrosstalkConfig):
    """Configuration for DECam crosstalk removal.
    """
    pass


@deprecated(reason="This method is no longer used.  Please use lsst.ip.isr.CrosstalkTask",
            version="v24.0", category=FutureWarning)
class DecamCrosstalkTask(CrosstalkTask):
    """Remove crosstalk from a raw DECam image.

    This was a gen2-only task, as crosstalk code is all in ip_isr.
    """
    ConfigClass = DecamCrosstalkConfig
    _DefaultName = 'decamCrosstalk'

    pass
