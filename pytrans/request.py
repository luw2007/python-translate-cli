# -*- coding:utf-8 -*-


from .cache import use_cache
from .util import TIMEOUT
from .compat import quote, urlparse, urlencode, HTTPConnection, HTTPSConnection


@use_cache
def get_sparse_array_from_google(text, from_lang, to_lang):
    """
         http://translate.google.cn/translate_a/single?client=t&ie=UTF-8&oe=UTF-8
          &sl=en&tl=zh-CN&hl=zh-cn
          &dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at
          &prev=btn&srcrom=1&ssel=0&tsel=0&tk=517377|509613&q=see
    """
    body = ''
    escaped_source = quote(text.encode('utf8'), '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
    url = "http://translate.google.cn/translate_a/single?client=t&ie=UTF-8&oe=UTF-8" \
          "&prev=btn&srcrom=1&ssel=0&tsel=0" \
          "&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at" \
          "&sl=%s&tl=%s&q=%s" % (from_lang, to_lang, escaped_source)

    r = HTTPHelper(url, headers=headers)
    try:
        _, body = r.get()
    finally:
        r.close()
    return body


class HTTPHelper(object):
    def __init__(self, url, headers=None, timeout=TIMEOUT):
        self.url = url
        self.headers = headers or {}
        url_pares = urlparse(url)

        if url_pares.scheme == "http":
            connect_func = HTTPConnection
        elif url_pares.scheme == "https":
            connect_func = HTTPSConnection
        else:
            raise KeyError(url_pares.scheme)

        self.conn = connect_func(url_pares.hostname, url_pares.port, timeout=timeout)


    def post(self, params):
        data = urlencode(params)
        self.conn.request('POST', self.url, data, headers=self.headers)
        httpres = self.conn.getresponse()
        result = httpres.read()
        return True, result

    def get(self):
        self.conn.request('GET', self.url, headers=self.headers)
        httpres = self.conn.getresponse()
        result = httpres.read()
        return True, result

    def close(self):
        self.conn.close()
