# -*- coding:utf-8 -*-
"""
    use pickle cache
"""

import logging
import os
import sys

try:
    import cPickle as pickle
except ImportError:
    import pickle

APP_PATH = os.path.join(os.path.expanduser("~"), '.pytrans')
app_path = lambda path: os.path.join(APP_PATH, path)
if not os.path.isdir(APP_PATH):
    os.mkdir(APP_PATH)

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