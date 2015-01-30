# -*- coding:utf-8 -*-
import os


TIMEOUT = 3
RETRY = 2

APP_PATH = os.path.join(os.path.expanduser("~"), '.pytrans')
app_path = lambda path: os.path.join(APP_PATH, path)
if not os.path.isdir(APP_PATH):
    os.mkdir(APP_PATH)

is_chinese = lambda uchar: u'\u4e00' <= uchar <= u'\u9fa5'
is_chinese.__doc__ = u'判断一个unicode是否是汉字'

is_number = lambda uchar: u'\u0030' <= uchar <= u'\u0039'
is_number.__doc__ = u'判断一个unicode是否是数字'

is_alphabet = lambda uchar: (u'\u0041' <= uchar <= u'\u005a') \
                            or (u'\u0061' <= uchar <= u'\u007a')
is_alphabet.__doc__ = u'判断一个unicode是否是英文字母'

is_other = lambda uchar: not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar))
is_other.__doc__ = u'判断是否非汉字，数字和英文字符'

len_gbk_word = lambda u: 1 if is_number(u) or is_alphabet(u) else 2
len_gbk_word.__doc__ = u'gbk宽度可用于对齐，中文占两个字符位置'
len_gbk_words = lambda uw: sum(map(len_gbk_word, uw))
len_gbk_words.__doc__ = u'计算文本显示宽度'


def ujoin(key, words):
    spaces = ' ' * (10 - len_gbk_words(key))
    content = '%s%s%s' % (key, spaces, ', '.join(words))
    return content


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
        if default is not None and isinstance(tmp, list):
            return tmp or default
        return tmp