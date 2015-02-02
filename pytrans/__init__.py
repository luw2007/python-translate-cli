# -*- coding:utf-8 -*-
u"""
    调用goole.com/translate 查询单词
    FEATURE:
        查看单词详细信息
        增加缓存
        python3
        实现解析sparse_array, 移除对simplejson 的hack
        i18n
        支持句子搜索
    TODO:
        增加界面, 方便跳转不同的单词
"""

__version__ = '0.3'
__all__ = ['cli']

import click

from .language import USER_LANG
from .i18n import trans as i18
from .theme import print_menu, make_menu as menu


@click.command()
@click.argument('text', default='')
@click.option('-f', default='auto',
              help=i18('From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.'))
@click.option('-t', default=USER_LANG,
              help=i18('To language (e.g. zh, zh-TW, en, ja, ko). Default is %s') % USER_LANG)
@click.option('--simple', '-s', is_flag=True,
              help=i18('simple mode'))
@click.option('--interface', '-i', is_flag=True,
              help=i18('Interactive mode'))
def cli(text, f, t, simple, interface):
    menu(text, f, t, simple, interface)









