# -*- coding:utf-8 -*-

import click

HEADER_COLOR = 'blue'
VIP_COLOR = 'cyan'
MENU_STYLE_ARGS = dict(bg='blue', nl=False)


def header_style(message, count=None):
    click.secho('[%s]' % message, bold=True, nl=(count is None))
    if count is not None:
        click.secho(': %d' % count, bold=True)


def content_style(content, **kwargs):
    if isinstance(content, (list, tuple)):
        for c in content:
            content_style(c, **kwargs)
    else:
        click.echo('    %s' % content, **kwargs)


def vip_style(content, **kwargs):
    click.secho(content, fg=VIP_COLOR, **kwargs)


def title_style(title, **kwargs):
    click.secho(title, fg=HEADER_COLOR, bold=True, **kwargs)


def summary_style(src, src_, dst, dst_, src_lang, dst_lang):
    # src_lang -> dst_lang
    if src_lang and dst_lang:
        title_style(src_lang, nl=False)
        click.secho(' -> ', nl=False)
        title_style(dst_lang)
    elif src_lang or dst_lang:
        title_style('%s: ' % (src_lang or dst_lang), nl=False)

    # src -> dst
    if src:
        vip_style(src, nl=False)
        click.secho('[%s]' % src_, nl=False)
    src and dst and click.secho(' -> ', nl=False)
    if dst:
        vip_style(dst, nl=False)
        click.secho('[%s]' % dst_, nl=False)
    click.echo()


