# flake8: noqa
import os

from .base import *

# Application definition
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

# MIDDLEWARE += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

# used for Django Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]