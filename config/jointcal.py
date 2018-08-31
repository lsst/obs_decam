for refObjLoader in (config.astrometryRefObjLoader,
                     config.photometryRefObjLoader):
    if hasattr(refObjLoader, "ref_dataset_name"):
        refObjLoader.ref_dataset_name = 'ps1_pv3_3pi_20170110'
    # Note the u-band results may not be useful without a color term
    refObjLoader.filterMap['u'] = 'g'
    refObjLoader.filterMap['Y'] = 'y'
