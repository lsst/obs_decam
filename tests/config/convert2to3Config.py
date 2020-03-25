# Config overrides for `test_convert2to3.py`
# The decam conversion tests use stripped data from `ap_verify_ci_hits2015` in
# testdata_decam, with two refcats in the repo.

config.refCats = ['gaia', 'panstarrs']

# Need to specify runs for each refcat
for refcat in config.refCats:
    config.runs[refcat] = "refcats"
