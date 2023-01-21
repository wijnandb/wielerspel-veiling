import os

ENV = os.environ.get('ENV')

if ENV == 'dev':
    from .dev import *  # noqa
    #print(f'\t ENV:\t\t{ENV}\n SETTINGS LOADED')
    #print('*' * 40)

else:
    from .prod import * # noqa
    #print(f'\t ENV:\t\t{ENV}\n SETTINGS LOADED')
    #print('+' * 40)
