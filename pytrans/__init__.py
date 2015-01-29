# -*- coding:utf-8 -*-
"""
    调用goole.com/translate 查询单词
    FEATURE:
        查看单词详细信息
        增加缓存
        python3
        实现解析sparse_array, 移除对simplejson 的hack
        i18n
    TODO:
        移除 requests 依赖
        支持句子搜索
        增加界面, 方便跳转不同的单词
"""

__version__ = '0.1'
__all__ = ['cli']

from collections import OrderedDict
import click

from .parse import get_translate_from_google
from .language import USER_LANG
from .util import after_exit, ujoin
from .i18n import trans as i18
from .style import summary_style, title_style, header_style, content_style, vip_style, MENU_STYLE_ARGS

width, hight = click.get_terminal_size()

MENU_QUIT = i18('quit')
MENU_SINGLE = i18('single')
MENU_INDEX = i18('main')
MENU_NEW = i18('new word')
MENU_FROM = i18('verbose from_lang')
MENU_TO = i18('verbose to_lang')
MENU_VERBOSE = i18('verbose all')

KEY_MAPS = OrderedDict([
    ('m', MENU_INDEX),
    ('n', MENU_NEW),
    ('f', MENU_FROM),
    ('t', MENU_TO),
    ('v', MENU_VERBOSE),
    ('q', MENU_QUIT)
])


@click.command()
@click.argument('text', default='')
@click.option('-f', default='auto',
              help=i18('From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.'))
@click.option('-t', default=USER_LANG,
              help=i18('To language (e.g. zh, zh-TW, en, ja, ko). Default is %s') % USER_LANG)
@click.option('--simple', '-s', is_flag=True, help=i18('simple model'))
def cli(text, f, t, simple):
    try:
        make_menu(text, f, t, simple)
    finally:
        after_exit()


def print_menu():
    click.secho('%s: ' % i18('MENU'), **MENU_STYLE_ARGS)
    for key, info in KEY_MAPS.items():
        click.secho('[', **MENU_STYLE_ARGS)
        vip_style(key, **MENU_STYLE_ARGS)
        click.secho(']%s; ' % info, **MENU_STYLE_ARGS)
    click.secho(' [%s]?' % i18(MENU_QUIT), **MENU_STYLE_ARGS)
    click.secho('')


def make_menu(text, f, t, simple):
    menu = MENU_SINGLE if simple else MENU_INDEX
    body = None
    while True:
        if not body and text:
            body = get_translate_from_google(text, f, t)

        if body:
            if not simple:
                click.clear()
            print_translate(body, menu)
            if simple:
                break
            print_menu()
            op = click.getchar()
            menu = KEY_MAPS.get(op, MENU_QUIT)
        else:
            menu = MENU_NEW

        if menu == MENU_NEW:
            text = click.prompt(i18('Please input word'))
            if text: body = None

        elif menu == MENU_QUIT:
            break


def print_translate(trans, menu):
    """
        trans = {
            'translate': {
                'from': '',
                "from_phonetic': '',
                'to': '',
                'to_phonetic': '',
                'text': 'input'
            },
            'from': {
                'lang': {Name, ...},
                'def': {Category:[Sentence], ...},
                'synonyms': {Category:[Word, ...], ...},
                'example': [Sentence, ...]
            },
            'to': {
                'lang': {Name, ...},
                'def': {Category:[(key, [Word], ...), ...], ...},
                'also': [Word, ...]
            },
        }
    """

    # 查询内容

    src, src_p= trans['translate']['from'], trans['translate']['from_phonetic']
    dst, dst_p = trans['translate']['to'], trans['translate']['to_phonetic']
    src_lang, dst_lang = trans['from']['lang']['name'], trans['to']['lang']['name']

    if menu in [MENU_FROM]:
        dst, dst_p, dst_lang = None, None, None

    elif menu in [MENU_TO]:
        src, src_p, src_lang = None, None, None

    summary_style(src, src_p, dst, dst_p, src_lang, dst_lang)

    if menu not in [MENU_FROM]:
        end = 5
        if menu == MENU_VERBOSE:
            end = 99
        # 翻译
        title_style(i18('Definitions'))
        for cate, row in trans['to']['def'].items():
            header_style(cate, len(row))
            for (key, words) in row[:end]:
                content_style(ujoin(key, words))

        # 另请参阅
        title_style(i18('See also'))

        content_style(', '.join(trans['to']['also']))
    if menu in [MENU_FROM, MENU_VERBOSE]:
        end = 5
        if menu == MENU_VERBOSE:
            end = 99

        # 定义 Definitions
        title_style(i18('Definitions'))
        for cate, row in trans['from']['def'].items():
            header_style(cate, len(row))
            content_style(row[:end])


        # 同义词 Synonyms
        title_style(i18('Synonyms'))
        for cate, row in trans['from']['synonyms'].items():
            header_style(cate, len(row))
            content_style(', '.join(row[:end]))

        # 示例 Examples
        title_style(i18('Example'))
        content_style(trans['from']['example'][:end])


if __name__ == '__main__':
    cli('see')