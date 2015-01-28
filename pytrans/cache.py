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

cache_file = '/tmp/pytrans.pick%d' % sys.version_info.major


class Cache(dict):
    def __init__(self):
        if os.path.exists(cache_file) and len(self) == 0:
            super(Cache, self).__init__(pickle.load(open(cache_file, 'rb')))
            logging.debug('loading cache [%d]' % len(self))

    def dump(self):
        pickle.dump(dict(self), open(cache_file, 'wb'))


CACHE = Cache()