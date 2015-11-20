# -*- coding: utf-8 -*-
import os
from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'roboconf.db'),
    }
}
