# -*- coding:utf-8 -*-

from .sparse_array import loads as sparse_array_loads
from .util import is_chinese, make_safe_list
from .request import get_sparse_array_from_google
from .language import USER_LANG, get_lang_info, get_lang_code, DEFAULT_LANG_CODE

def get_translate_from_google(text, from_lang, to_lang):
    u"""
        按照 text, from_lang, to_lang 访问google translate 接口,
        解析 javascript  sparse_array 格式的字符串,
        返回 列表
    """

    from_lang, to_lang = map(get_lang_code, (from_lang, to_lang))
    if text and to_lang == USER_LANG \
            and all(map(lambda x: is_chinese(x), text)):
        to_lang = DEFAULT_LANG_CODE

    body = get_sparse_array_from_google(text, from_lang, to_lang)
    response_array = sparse_array_loads(body)
    return parse_translate(response_array, text, from_lang, to_lang)


def parse_translate(array, text, from_lang, to_lang):
    get_index = make_safe_list(array).get
    trans = {
        'translate': {
            'from': get_index(0, 0, 1, default=text),
            'to': get_index(0, 0, 0, default=''),
            'from_phonetic': get_index(0, 1, 3, default=''),
            'to_phonetic': get_index(0, 1, 2, default=''),
            'text': text,
        },
        'from': {
            'lang': {},
             'def': {},
            'synonyms': {},
            'example': []
        },
        'to': {
            'lang': {},
            'def': {},
            'also': []
        },
    }
    from_map = trans['from']
    to_map = trans['to']
    from_map['lang'] = get_lang_info(get_index(2, default=from_lang))
    to_map['lang'] = get_lang_info(to_lang)

    # 翻译后单词的定义 Definitions
    for row in get_index(1, default=[]):
        category = row[0]
        to_map['def'][category] = [item[:2] for item in row[2]]

    # 翻译后单词的更多 see also
    to_map['also'] = [item[0] for item in get_index(5, 0, 2, default=[])]

    # 定义 Definitions
    for row in get_index(12, default=[]):
        category = row[0]
        for item in row[1]:
            from_map['def'].setdefault(category, []).append(item.get(0, default=''))
            from_map['def'].setdefault(category, []).append(item.get(2, default=''))

    # 同义词 Synonyms
    for row in get_index(11, default=[]):
        category = row[0]
        rows = []
        for _row in row[1]:
            rows.extend(_row[0])
        from_map['synonyms'][category] = rows

    # 示例 Examples
    from_map['example'] = [row[0].strip() for row in get_index(13, 0, default=[])]

    # 更多 see also
    from_map['also'] = [row for row in get_index(14, 0, default=[])]

    return trans
