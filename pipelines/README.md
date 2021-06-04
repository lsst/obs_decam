# This is not a good place for pipelines

If you're looking for DECam-specific ISR-related pipelines,
they have moved to the `ap_pipe` package as of DM-29338.

As RFC-775 is implemented, it is anticipated this `pipelines` directory
will go away. Please put new pipelines in `*_pipe` or some other appropriate
non-obs-package location.
