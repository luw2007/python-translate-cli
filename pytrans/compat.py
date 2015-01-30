"""
    Python 3 compatibility shims
    help: <https://github.com/simplejson/simplejson>
"""
import sys
if sys.version_info[0] < 3:
    PY3 = False
    def b(s):
        return s
    def u(s):
        return unicode(s, 'unicode_escape')
    import cStringIO as StringIO
    StringIO = BytesIO = StringIO.StringIO
    text_type = unicode
    binary_type = str
    string_types = (basestring,)
    integer_types = (int, long)
    unichr = unichr
    reload_module = reload
    def fromhex(s):
        return s.decode('hex')
    from urllib import quote, urlencode
    from urlparse import urlparse
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    if sys.version_info[1] >= 7:
        from collections import OrderedDict
        from sys import version_info
    else:
        from ordereddict import OrderedDict
        from collections import namedtuple
        VERSION_INFO = namedtuple('version_info', 'major minor micro releaselevel serial')
        sys.version_info = version_info = VERSION_INFO(*sys.version_info)
    from httplib import HTTPConnection, HTTPSConnection
else:
    PY3 = True
    if sys.version_info[:2] >= (3, 4):
        from importlib import reload as reload_module
    else:
        from imp import reload as reload_module
    import codecs
    def b(s):
        return codecs.latin_1_encode(s)[0]
    def u(s):
        return s
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO
    text_type = str
    binary_type = bytes
    string_types = (str,)
    integer_types = (int,)

    def unichr(s):
        return u(chr(s))

    def fromhex(s):
        return bytes.fromhex(s)
    from urllib.parse import quote, urlparse, urlencode
    import pickle
    from collections import OrderedDict
    from http.client import HTTPConnection, HTTPSConnection
long_type = integer_types[-1]