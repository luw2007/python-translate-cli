# -*- coding:utf-8 -*-
u"""
    界面主题, 包含 菜单和显示内容
"""
import threading
import click
import traceback

from .compat import OrderedDict
from pytrans.google_images_search import search_image
from .style import summary_style, title_style, header_style, content_style, vip_style, MENU_STYLE_ARGS
from .util import ujoin
from .parse import get_translate_from_google
from .i18n import trans as i18

width, hight = click.get_terminal_size()

MENU_QUIT = i18('quit')
MENU_SINGLE = i18('single')
MENU_INDEX = i18('main')
MENU_NEW = i18('new word')
MENU_FROM = i18('verbose from_lang')
MENU_TO = i18('verbose to_lang')
MENU_PICTRUE = i18('show picture')
MENU_VERBOSE = i18('verbose all')

KEY_MAPS = OrderedDict([
    ('n', MENU_NEW),
    ('f', MENU_FROM),
    ('t', MENU_TO),
    ('v', MENU_VERBOSE),
    ('p', MENU_PICTRUE),
    ('q', MENU_QUIT)
])


def print_menu():
    click.secho('%s: ' % i18('MENU'), **MENU_STYLE_ARGS)
    for key, info in KEY_MAPS.items():
        click.secho('[', **MENU_STYLE_ARGS)
        vip_style(key, **MENU_STYLE_ARGS)
        click.secho(']%s; ' % info, **MENU_STYLE_ARGS)
    click.secho('%s:%s?' % (i18('default'), i18(MENU_QUIT)), **MENU_STYLE_ARGS)
    click.secho('')


def make_menu(text, f, t, simple, interface):
    menu = MENU_SINGLE if simple or interface else MENU_INDEX
    body = None
    while True:
        if not body and text:
            body = get_translate_from_google(text, f, t)

        if body:
            if not interface:
                click.clear()
            print_translate(body, menu)
            if interface:
                menu = MENU_NEW
            elif simple:
                return
            else:
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

def show_picture(text):
    """
        show picture
    """
    status, pictures = search_image(text)
    if status and pictures:
        try:
            from PIL import Image
        except ImportError as e:
            print(u'need install PIL first. like `pip install Pillow`')
            traceback.print_exc()
            raise e
        # FIXME: 换一种实现
        for picture in pictures:
            Image.open(picture).show()

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

    src, src_p = trans['translate']['from'], trans['translate']['from_phonetic']
    dst, dst_p = trans['translate']['to'], trans['translate']['to_phonetic']
    src_lang, dst_lang = trans['from']['lang']['name'], trans['to']['lang']['name']

    if menu == MENU_FROM:
        dst, dst_p, dst_lang = None, None, None
    elif menu == MENU_TO:
        src, src_p, src_lang = None, None, None
    elif menu == MENU_SINGLE:
        src, src_p, src_lang = None, None, None

    summary_style(src, src_p, dst, dst_p, src_lang, dst_lang)

    end = 5
    if menu not in [MENU_FROM]:
        if menu == MENU_VERBOSE:
            end = 99
        # 翻译
        title_style(i18('Definitions'))
        for cate, row in trans['to']['def'].items():
            header_style(cate, len(row))
            for (key, words) in row[:end]:
                content_style(ujoin(key, words))

    if menu not in [MENU_FROM, MENU_SINGLE]:
        # 另请参阅
        title_style(i18('See also'))

        content_style(', '.join(trans['to']['also']))

    if menu in [MENU_FROM, MENU_VERBOSE]:
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

    if menu == MENU_PICTRUE:
        p = threading.Thread(target=show_picture, args=(trans['translate']['text'], ))
        p.start()
        p.join()