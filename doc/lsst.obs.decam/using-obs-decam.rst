.. _lsst.obs.decam.gen3:

#################
The Gen3 workflow
#################

These directions are for users who wish to create their own data repositories independent of any Rubin/LSST-supported shared repositories.
They assume the user has a recent weekly version of ``lsst_distrib`` setup.

Local repository setup
----------------------

Create a Gen3 data repository and write curated calibration products to it (these include crosstalk, linearity, and defects).
The latter step creates the ``DECam/calib`` collection.
In the example here, ``REPO`` refers to the location you choose for the Butler repository.

.. prompt:: bash

   cd REPO
   butler create REPO
   butler register-instrument REPO lsst.obs.decam.DarkEnergyCamera
   butler write-curated-calibrations REPO lsst.obs.decam.DarkEnergyCamera

Check that this worked successfully by querying all the collections currently in the repo, e.g.,

.. prompt:: bash

   butler query-collections REPO --chains=tree

This should print a short list of collections, including several beginning with ``DECam/calib/curated`` and one called ``DECam/raw/all``.

Ingest raw images
-----------------

Ingest raw science and calibration (bias and flat) frames, which creates the ``DECam/raw/all`` collection.
Next, run overscan correction on all the raws via the ``RunIsrForCrosstalkSources.yaml`` pipeline so they may be used as crosstalk sources during ISR (this is a DECam-specific step).

.. prompt:: bash

   butler ingest-raws REPO /path/to/raw/science/*.fits.fz --transfer link
   butler ingest-raws REPO /path/to/raw/calibs/*.fits.fz --transfer link
   pipetask run -b REPO -i DECam/raw/all -o DECam/raw/crosstalk-sources -p $CP_PIPE_DIR/pipelines/DarkEnergyCamera/RunIsrForCrosstalkSources.yaml --register-dataset-types

Check that this worked successfully, e.g.,

.. prompt:: bash

   butler query-dimension-records REPO exposure --where "instrument='DECam' AND exposure.observation_type='zero'"
   butler query-dimension-records REPO exposure --where "instrument='DECam' AND exposure.observation_type='dome flat'"

This should print tables of familiar-looking calibration exposures, with reasonable exposure and detector numbers, filter information, times, sky location, and other metadata.

Use ``cp_pipe`` to build nightly calibs
---------------------------------------

Next, build nightly (or similar) bias and flat frames using :py:mod:`lsst.cp.pipe` and certify them into a calib collection.

This example assumes the user has a single night of observations with bias frames numbered 1-6 and flat frames numbered 7-12, and wants to create nightly calib products valid for 24 hours.
Note the bias building pipeline is camera-agnostic, but the flat-building pipeline has a prerequisite DECam-specific step which correctly handles inter-chip crosstalk.

.. prompt:: bash

   pipetask run -d "exposure IN (1, 2, 3, 4, 5, 6)" -b REPO -i DECam/raw/all,DECam/calib -o u/username/bias-construction-night1 -p $CP_PIPE_DIR/pipelines/cpBias.yaml --register-dataset-types
   butler certify-calibrations REPO u/username/bias-construction-night1 DECam/calib/run1 bias --begin-date 2021-01-01T00:00:00 --end-date 2021-01-01T23:59:59
   pipetask run -d "exposure IN (7, 8, 9, 10, 11, 12)" -b REPO -i DECam/raw/all,DECam/raw/crosstalk-sources,DECam/calib -o u/username/flat-construction-night1 -p $CP_PIPE_DIR/pipelines/DarkEnergyCamera/cpFlat.yaml --register-dataset-types
   butler certify-calibrations REPO u/username/flat-construction-night1 DECam/calib/run1 flat --begin-date 2021-01-01T00:00:00 --end-date 2021-01-01T23:59:59

Science time!
-------------

Now you can proceed with running ISR and other "processCcd" tasks via a Gen3 pipeline.

Some useful pipelines can be found in the ``pipelines/DECam`` directory of the :py:mod:`lsst.ap.pipe` and :py:mod:`lsst.drp.pipe` packages.
