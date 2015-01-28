#!/usr/bin/env python
# -*- coding:utf-8 -*-
import click

import pytrans.sparse_array
from pytrans.util import get_sparse_array_from_google, is_chinese, make_safe_list


DEFAULT_TO_LANG = 'zh'

MENU_QUIT = 'quit'
MENU_INDEX = 'main'
MENU_NEW = 'new word'
MENU_FROM = 'verbose from_lang'
MENU_TO = 'verbose to_lang'
MENU_VERBOSE = 'verbose all'


def get_translate_from_google(text, from_lang, to_lang):
    """
        按照 text, from_lang, to_lang 访问google translate 接口,
        解析 javascript  sparse_array 格式的字符串,
        返回 列表
    """

    if text and to_lang == DEFAULT_TO_LANG \
            and all(map(lambda x: is_chinese(x), text)):
        to_lang = 'en'
    body = get_sparse_array_from_google(text, from_lang, to_lang)
    response_array = pytrans.sparse_array.loads(body)
    return parse_translate(response_array)


def parse_translate(array):
    get_index = make_safe_list(array).get
    trans = {
        'translate': [],
        'from': {
            'def': {},
            'synonyms': {},
            'example': []
        },
        'to': {
            'def': {},
            'also': []
        },
    }
    from_map = trans['from']
    to_map = trans['to']

    # 查询内容 Definitions
    for row in get_index(0, 0):
        if row:
            trans['translate'].append(row)

    # 翻译后单词的定义 Definitions
    for row in get_index(1):
        category = row[0]
        to_map['def'][category] = [item[:2] for item in row[2]]

    # 翻译后单词的更多 see also
    to_map['also'] = [item[0] for item in get_index(5, 0, 2)]

    # 定义 Definitions
    for row in get_index(12):
        category = row[0]
        for item in row[1]:
            from_map['def'].setdefault(category, []).append(item.get(0, default=''))
            from_map['def'].setdefault(category, []).append(item.get(2, default=''))

    # 同义词 Synonyms
    for row in get_index(11):
        category = row[0]
        rows = []
        for _row in row[1]:
            rows.extend(_row[0])
        from_map['synonyms'][category] = rows

    # 示例 Examples
    from_map['example'] = [row[0].strip() for row in get_index(13, 0, default=[])]

    # 更多 see also
    from_map['also'] = [row for row in get_index(14, 0)]

    return trans


def print_translate(trans, menu):
    """
        trans = {
            'translate': [],
            'from': {
                'def': {},
                'synonyms': {},
                'example': []
            },
            'to': {
                'def': {},
                'also': []
            },
        }
    """
    end = 5
    if menu in [MENU_VERBOSE, MENU_TO]:
        end = 99

    # 查询内容
    for row in trans['translate']:
        click.secho(row, bold=True)

    if menu not in [MENU_FROM]:
        # 翻译
        click.secho('Definitions', fg='blue', bold=True)
        for cate, row in trans['to']['def'].items():
            click.secho('[%s]: %d' % (cate, len(row)), bold=True)
            for (key, words) in row[:end]:
                click.echo('    %s\n         %s' % (key, ', '.join(words)))

        # 另请参阅
        click.secho('See also', fg='blue', bold=True)
        click.echo('    %s' % ', '.join(trans['to']['also']))
    if menu in [MENU_FROM, MENU_VERBOSE]:
        end = 5
        if menu == MENU_VERBOSE:
            end = 99

        # 定义 Definitions
        click.secho('Definitions', fg='blue', bold=True)
        for cate, row in trans['from']['def'].items():
            click.secho('[%s]: %d' % (cate, len(row)), bold=True)
            for item in row[:end]:
                click.echo('    %s' % item)


        # 同义词 Synonyms
        click.secho('Synonyms', fg='blue', bold=True)
        for cate, row in trans['from']['synonyms'].items():
            click.secho('[%s]: %d' % (cate, len(row)), bold=True)
            click.echo('    %s' % ', '.join(row[:end]))

        # 示例 Examples
        click.secho('Example', fg='blue')
        for row in trans['from']['example']:
            click.echo('   %s' % row)

    click.echo()
