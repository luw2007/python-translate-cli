# -*- coding:utf-8 -*-
from .language import DEFAULT_LANG_CODE, USER_LANG

__al__ = ['trans']

I18N_MAP = {
    DEFAULT_LANG_CODE:
        {
            "definitions"             :     "Definitions",
            "see also"                :     "See also",
            "synonyms"                :     "Synonyms",
            "example"                 :     "Example",
            "translations of "        :     "Translations of ",

            "please input word"       :      "Please input word",
            "main"                    :      "main",
            "default"                 :      "Default",
            "menu"                    :      "MENU",
            "new word"                :      "new word",
            "quit"                    :      "quit",
            "verbose all"             :      "verbose all",
            "verbose from_lang"       :      "verbose from_lang",
            "verbose to_lang"         :      "verbose to_lang",
            "show picture"            :      "show picture",

            "simple mode"             :      "simple mode",
            "interactive mode"        :      "Interactive mode",
            "from language (e.g. zh, zh-tw, en, ja, ko). default is auto.":
                "From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.",
            "to language (e.g. zh, zh-tw, en, ja, ko). default is %s":
                "To language (e.g. zh, zh-TW, en, ja, ko). Default is %s",
        },
    'zh-CN':
        {
            "definitions"             :     u"定义",
            "see also"                :     u"另请参阅",
            "synonyms"                :     u"同义词",
            "example"                 :     u"例子",
            "translations of "        :     u"翻译于 ",
            "please input word"       :     u"请您输入",
            "main"                    :     u"主页",
            "default"                 :     u"默认",
            "menu"                    :     u"菜单",
            "new word"                :     u"查询新单词",
            "quit"                    :     u"退出",
            "verbose all"             :     u"查看全部",
            "verbose from_lang"       :     u"源单词解释",
            "verbose to_lang"         :     u"查看翻译",
            "show picture"            :     U"看图",

            "simple mode"             :     u"简单查询",
            "interactive mode"        :     u"交互模式",
            "from language (e.g. zh, zh-tw, en, ja, ko). default is auto.":
                u"来自什么语言 (e.g. zh, zh-TW, en, ja, ko). 默认 auto.",
            "to language (e.g. zh, zh-tw, en, ja, ko). default is %s":
                u"翻译成什么语言 (e.g. zh, zh-TW, en, ja, ko). 默认 %s",
        },
    'ja':
        {
            "definitions"             :     "定義",
            "see also"                :     "参照",
            "synonyms"                :     "同義語",
            "example"                 :     "例",
            "translations of "        :     "の翻訳 ",
        },
}


def trans(text):
    _i18n = I18N_MAP.get(USER_LANG, I18N_MAP[DEFAULT_LANG_CODE])

    return _i18n.get(text.lower(), text)

