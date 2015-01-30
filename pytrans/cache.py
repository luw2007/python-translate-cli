# -*- coding:utf-8 -*-
"""
    use pickle cache
"""

import os
import sys
from .util import app_path
from .compat import pickle

cache_file = app_path('cache.pick%d' % sys.version_info.major)


class Cache(dict):
    def __init__(self):
        if os.path.exists(cache_file) and len(self) == 0:
            with open(cache_file, 'rb') as f:
                super(Cache, self).__init__(pickle.load(f))

    def dump(self):
        with open(cache_file, 'wb') as f:
            pickle.dump(dict(self), f)

CACHE = Cache()
after_exit = CACHE.dump