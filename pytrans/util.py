import logging

import requests

try:
    from urllib import quote
except:
    from urllib.parse import quote

from pytrans.cache import CACHE


TIMEOUT = 3
RETRY = 2

after_exit = CACHE.dump
is_chinese = lambda uchar: u'\u4e00' <= uchar <= u'\u9fa5'


def use_cache(func):
    def swapper(*a):
        key = '_'.join(a)
        if key not in CACHE:
            CACHE[key] = func(*a)
        else:
            logging.debug('hide cache')
        return CACHE[key]

    return swapper


@use_cache
def get_sparse_array_from_google(text, from_lang, to_lang):
    """
         http://translate.google.cn/translate_a/single?client=t&ie=UTF-8&oe=UTF-8
          &sl=en&tl=zh-CN&hl=zh-cn
          &dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at
          &prev=btn&srcrom=1&ssel=0&tsel=0&tk=517377|509613&q=see
    """
    escaped_source = quote(text.encode('utf8'), '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
    url = "http://translate.google.cn/translate_a/single?client=t&ie=UTF-8&oe=UTF-8" \
          "&prev=btn&srcrom=1&ssel=0&tsel=0" \
          "&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at" \
          "&sl=%s&tl=%s&q=%s" % (from_lang, to_lang, escaped_source)
    r = requests.get(url, verify=False, headers=headers, timeout=TIMEOUT)
    return r.text


def make_safe_list(item):
    """
        >>> z = make_safe_list([[0]])
        >>> hasattr(z[0], 'get')
        True
    """
    if isinstance(item, SafeIndexlist):
        return item
    if isinstance(item, (list, tuple)):
        return SafeIndexlist(map(make_safe_list, item))
    else:
        if item is None:
            return SafeIndexlist()
        return item


class SafeIndexlist(list):
    """
        >>> z = SafeIndexlist([[[0, 1, 2], 1, 2], 1, 2])
        >>> z.get(0, 0, 0)
        0
        >>> z.get(6, default='')
        ''
        >>> z.get(0, 1)
        1
    """

    def get(self, *indexs, **kwargs):
        assert all(map(lambda index: isinstance(index, int), indexs))
        assert isinstance(indexs, (list, tuple))
        default = kwargs.pop('default', None)
        tmp = self
        try:
            for index in indexs:
                assert isinstance(tmp, (list, tuple))
                tmp = tmp[index]
        except (IndexError, AssertionError):
            return default
        return tmp