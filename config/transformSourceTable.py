import os.path

# Use the environment var. to prevent hardcoding of paths into quantum graphs.
# TODO: DM-28862: When that ticket is merged, policy files will be moved to a
# central location, likely into pipe_tasks.
config.functorFile = os.path.join('$OBS_DECAM_DIR', 'policy', 'Source.yaml')
