config.parse.translation = {'filter': 'FILTER',
                            'ccdnum': 'DETECTOR',
                            'calibDate': 'CALIBDATE',
                            }
config.register.columns = {'filter': 'text',
                           'ccdnum': 'int',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text',
                           }
config.register.tables = ['defects', 'crosstalk']
config.register.detector = ['filter', 'ccdnum']
config.register.unique = ['filter', 'ccdnum', 'calibDate']
config.register.visit = ['calibDate']
