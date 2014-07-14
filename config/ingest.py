from lsst.obs.decam.ingest import DecamParseTask
root.parse.retarget(DecamParseTask)
root.parse.hdu = 1
root.parse.translation = {'visit': 'EXPNUM',
                          'taiObs': 'DATE-OBS', 
                          'expTime': 'EXPTIME',
                          }
root.parse.translators = {'date': 'translate_date',
                          'filter': 'translate_filter',
                          'side': 'translate_side',
                          'ccd': 'translate_ccd',
                          }
root.parse.extnames = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13',
                       'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22', 'S23', 'S24', 'S25',
                       'S26', 'S27', 'S28', 'S29', 'S30', 'S31', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7',
                       'N8', 'N9', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15', 'N16', 'N17', 'N18', 'N19',
                       'N20', 'N21', 'N22', 'N23', 'N24', 'N25', 'N26', 'N27', 'N28', 'N29', 'N30', 'N31',
                       ]
root.register.columns = {'visit':    'int',
                         'side':     'text',
                         'ccd':      'int',
                         'filter':   'text',
                         'date':     'text',
                         'taiObs':   'text',
                         'expTime':  'double',
                         'instCal':  'text',
                         'dqmask':   'text',
                         'wtmap':    'text'
                         }
root.register.unique = ['visit', 'side', 'ccd']
