# -*- coding:utf-8 -*-

from .compat import OrderedDict
from .parse import get_translate_from_google
from .i18n import I18N_MAP
from .language import DEFAULT_LANG_CODE


def make_i18n(code):
    """
        grep "i18(" *.py |awk -F'i18' '{print $2}'|cut -d"'" -f2 |sort -u
    """
    _map = {}
    for word in OrderedDict(I18N_MAP[DEFAULT_LANG_CODE]):
        z = get_translate_from_google(word, DEFAULT_LANG_CODE, code)
        _map[word] = z['translate']['to']
    print(_map)

