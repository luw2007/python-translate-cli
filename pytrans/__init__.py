# -*- coding:utf-8 -*-
"""
    调用goole.com/translate 查询单词
    FEATURE:
        查看单词详细信息
        增加缓存
        python3
        实现解析sparse_array, 移除对simplejson 的hack
    TODO:
        移除 requests 依赖
        支持句子搜索
        增加界面, 方便跳转不同的单词
"""

__version__ = '0.1'
__all__ = ['cli']

import click
from collections import OrderedDict

from .main import get_translate_from_google, print_translate, \
    MENU_INDEX, MENU_NEW, MENU_FROM, MENU_TO, MENU_VERBOSE, MENU_QUIT, \
    DEFAULT_TO_LANG

from .util import after_exit

width, hight = click.get_terminal_size()

KEY_MAPS = OrderedDict([
    ('m', MENU_INDEX),
    ('n', MENU_NEW),
    ('f', MENU_FROM),
    ('t', MENU_TO),
    ('v', MENU_VERBOSE),
    ('q', MENU_QUIT)
])

MENU = "menu: %s ?[q]\n#%s#\n" % ('; '.join('[%s]%s' % (k, v) for (k, v) in KEY_MAPS.items()), "=" * (width - 2))
NEW_WORD_PROMPT = 'Please input word'


@click.command()
@click.argument('text', default='')
@click.option('-f', default='auto',
              help='From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.')
@click.option('-t', default=DEFAULT_TO_LANG,
              help='To language (e.g. zh, zh-TW, en, ja, ko). Default is zh')
def cli(text, f, t):
    try:
        make_menu(text, f, t)
    finally:
        after_exit()


def make_menu(text, f, t):
    menu = MENU_INDEX
    body = None
    while True:
        if not body and text:
            body = get_translate_from_google(text, f, t)

        if menu != MENU_NEW:
            click.clear()

        if body:
            print_translate(body, menu)
            click.echo(MENU, nl=False)
            op = click.getchar()
            menu = KEY_MAPS.get(op, MENU_QUIT)
        else:
            menu = MENU_NEW

        if menu == MENU_NEW:
            text = click.prompt(NEW_WORD_PROMPT)
            if text: body = None

        elif menu == MENU_QUIT:
            break