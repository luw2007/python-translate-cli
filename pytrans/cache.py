# -*- coding:utf-8 -*-
"""
    use pickle cache
"""

import os
from .util import app_path
from .compat import pickle, version_info

cache_file = app_path('cache.pick%d' % version_info.major)


class Cache(dict):
    def __init__(self):
        if os.path.exists(cache_file) and len(self) == 0:
            with open(cache_file, 'rb') as f:
                try:
                    jsons = pickle.load(f)
                except EOFError:
                    try:
                        os.remove(cache_file)
                    except (OSError, IOError):
                        pass
                    return
                super(Cache, self).__init__(jsons)

    def dump(self):
        with open(cache_file, 'wb') as f:
            pickle.dump(dict(self), f)


CACHE = Cache()


def use_cache(func):
    def swapper(*a):
        key = '_'.join(a)
        if key not in CACHE:
            CACHE[key] = func(*a)
            CACHE.dump()
        return CACHE[key]

    return swapper