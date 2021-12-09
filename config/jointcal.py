import os.path

# `load()` appends to the filterMaps: we need them to be empty, so that
# only the specified filter mappings are used.
config.photometryRefObjLoader.filterMap = {}
filterMapFile = os.path.join(os.path.dirname(__file__), "filterMap.py")
config.photometryRefObjLoader.load(filterMapFile)
# We have PS1 colorterms
config.applyColorTerms = True
config.colorterms.load(os.path.join(os.path.dirname(__file__), "colorterms.py"))
