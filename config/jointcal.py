# `load()` appends to the filterMaps: we need them to be empty, so that
# only the specified filter mappings are used.
config.photometryRefObjLoader.filterMap = {}
config.photometryRefObjLoader.load("filterMap.py")
# We have PS1 colorterms
config.applyColorTerms = True
config.colorterms.load("colorterms.py")
