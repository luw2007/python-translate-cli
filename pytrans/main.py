#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    调用goole.com/translate 查询单词
    FEATURE:
        查看单词详细信息
        增加缓存
        python3
        实现解析sparse_array, 移除对simplejson 的hack
    TODO:
        支持句子搜索
        增加界面, 方便跳转不同的单词
"""

import os
import sys
import logging

import click
import requests
from html2text import html2text

import pytrans.sparse_array

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from urllib import quote
except:
    from urllib.parse import quote

width, hight = click.get_terminal_size()
is_chinese = lambda uchar: u'\u4e00' <= uchar <= u'\u9fa5'
MENU = "menu: m: main; n: new word; f: verbose from_lang; t: verbose to_lang; v: more all; q: quit; [q]\n" \
       + '#%s#' % ("=" * (width - 2 ))
cache_file = '/tmp/pytrans.pick%d' % sys.version_info.major
TIMEOUT = 3
RETRY = 2


class Cache(dict):
    def __init__(self):
        if os.path.exists(cache_file) and len(self) == 0:
            super(Cache, self).__init__(pickle.load(open(cache_file, 'rb')))
            logging.debug('loading cache [%d]' % len(self))

    def dump(self):
        pickle.dump(dict(self), open(cache_file, 'wb'))


CACHE = Cache()


def use_cache(func):
    def swapper(*a):
        key = '_'.join(a)
        if key not in CACHE:
            CACHE[key] = func(*a)
        else:
            logging.debug('hide cache')
        return CACHE[key]

    return swapper


def menu(text, f, t):
    menu = 'main'
    result_json = None
    while True:
        if not result_json and text:
            body = get_sparse_array_from_google(text, f, t)
            result_json = decode_sparse_array(body)
        if menu != 'new':
            click.clear()
        if result_json:
            print_tranlate(result_json, menu)
            click.echo(MENU, nl=False)
            op = click.getchar()
            if op == 'v':
                menu = 'all'
            elif op == 'f':
                menu = 'from'
            elif op == 't':
                menu = 'to'
            elif op == 'm':
                menu = 'main'
            elif op in ['q', '\r']:
                menu = 'quit'
            elif op == 'n':
                menu = 'new'
            else:
                menu = 'quit'
            click.echo()
        else:
            menu = 'new'

        if menu == 'quit':
            return
        elif menu == 'new':
            text = click.prompt('Please input words')
            if text:
                result_json = None


def print_tranlate(result_json, menu):
    has_index = lambda idx: len(result_json) > idx and result_json[idx]
    end = 5
    if menu == 'all' or menu == 'to':
        end = 99
    # 查询内容
    for row in result_json[0][0]:
        if row:
            click.secho(row, bold=True)
    # 不同词性
    if len(result_json) > 1 and result_json[1]:
        for row in result_json[1]:
            click.secho('[%s]: %d' % (row[0], len(row[2])), bold=True)
            list(map(click.echo, ['    %s\n         %s' % (item[0], ', '.join(item[1])) for item in row[2][:end]]))

    # 翻译
    if has_index(5):
        click.echo('\n%s' % ', '.join([item[0] for item in result_json[5][0][2]]))

    if menu == 'from' or menu == 'all':
        end = 5
        if menu == 'all':
            end = 99

        # 定义 Definitions
        if has_index(12):
            click.secho('Definitions', fg='blue')
            for row in result_json[12]:
                click.secho('  [%s]: %d' % (row[0], len(row[1])), bold=True)
                for item in row[1]:
                    try:
                        click.echo('    %s\n         %s' % (item[0], item[2]))
                    except:
                        pass


        # 同义词 Synonyms
        if has_index(11):
            click.secho('Synonyms', fg='blue')
            for row in result_json[11]:
                rows = []
                for _row in row[1]:
                    rows.extend(_row[0])
                click.secho('  [%s]: %d' % (row[0], len(rows)), bold=True)
                click.echo('    %s' % ', '.join(rows[:end]))



        # 示例 Examples
        if has_index(13):
            click.secho('Example', fg='blue')
            for row in result_json[13][0][:end]:
                click.echo('   %s' % (html2text(row[0]).strip()))

    # 另请参阅
    if has_index(14):
        click.secho('See also', fg='blue')
        click.echo('    %s' % ', '.join([row for row in result_json[14][0]]))
    click.echo()


def decode_sparse_array(source):
    """ 将'[,]'类型的字符串转换成列表[None,None]"""
    return pytrans.sparse_array.loads(source)


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


@click.command()
@click.argument('text', default='')
@click.option('-f', default='auto',
              help='From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.')
@click.option('-t', default='zh',
              help='To language (e.g. zh, zh-TW, en, ja, ko). Default is zh')
def cli(text, f, t):
    if text and all(map(lambda x: is_chinese(x), text)) and t == 'zh':
        t = 'en'
    try:
        menu(text, f, t)
    finally:
        CACHE.dump()
