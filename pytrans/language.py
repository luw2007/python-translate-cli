# -*- coding:utf-8 -*-
"""
    Initialize all supported locales.
    Mostly ISO 639-1 codes, with a few ISO 639-2 codes (alpha-3).
    See: <https://github.com/soimort/translate-shell/blob/develop/include/Languages.awk>
         <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>
         <http://www.loc.gov/standards/iso639-2/php/code_list.php>

"""

import locale
import re

from .compat import OrderedDict

# FIXME: handle unrecognized language code
DEFAULT_LANG_CODE = "en"

LOCALE_MAP = OrderedDict([
    ('af', {'name': 'Afrikaans', 'message': 'Vertalings van %s', 'endonym': 'Afrikaans'}),
    ('sq', {'name': 'Albanian', 'message': 'Përkthimet e %s', 'endonym': 'Shqip'}),
    ('ar', {'rtl': 'true', 'name': 'Arabic', 'message': 'ترجمات %s', 'endonym': 'العربية'}),
    ('hy', {'name': 'Armenian', 'message': '%s-ի թարգմանությունները', 'endonym': 'Հայերեն'}),
    ('az', {'name': 'Azerbaijani', 'message': '%s sözünün tərcüməsi', 'endonym': 'Azərbaycanca'}),
    ('eu', {'name': 'Basque', 'message': '%s esapidearen itzulpena', 'endonym': 'Euskara'}),
    ('be', {'name': 'Belarusian', 'message': 'Пераклады %s', 'endonym': 'беларуская'}),
    ('bn', {'name': 'Bengali', 'message': '%s এর অনুবাদ', 'endonym': 'বাংলা'}),
    ('bs', {'name': 'Bosnian', 'message': 'Prijevod za: %s', 'endonym': 'Bosanski'}),
    ('bg', {'name': 'Bulgarian', 'message': 'Преводи на %s', 'endonym': 'български'}),
    ('ca', {'name': 'Catalan', 'message': 'Traduccions per a %s', 'endonym': 'Català'}),
    ('ceb', {'name': 'Cebuano', 'message': '%s Mga Paghubad sa PULONG_O_HUGPONG SA PAMULONG', 'endonym': 'Cebuano'}),
    ('zh-CN', {'name': 'Chinese Simplified', 'message': '%s 的翻译', 'endonym': '简体中文'}),
    ('zh-TW', {'name': 'Chinese Traditional', 'message': '「%s」的翻譯', 'endonym': '正體中文'}),
    ('ny', {'name': 'Chichewa', 'message': 'Matanthauzidwe a %s', 'endonym': 'Nyanja'}),
    ('hr', {'name': 'Croatian', 'message': 'Prijevodi riječi ili izraza %s', 'endonym': 'Hrvatski'}),
    ('cs', {'name': 'Czech', 'message': 'Překlad výrazu %s', 'endonym': 'Čeština'}),
    ('da', {'name': 'Danish', 'message': 'Oversættelser af %s', 'endonym': 'Dansk'}),
    ('nl', {'name': 'Dutch', 'message': 'Vertalingen van %s', 'endonym': 'Nederlands'}),
    ('en', {'name': 'English', 'message': 'Translations of %s', 'endonym': 'English'}),
    ('eo', {'name': 'Esperanto', 'message': 'Tradukoj de %s', 'endonym': 'Esperanto'}),
    ('et', {'name': 'Estonian', 'message': 'Sõna(de) %s tõlked', 'endonym': 'Eesti'}),
    ('tl', {'name': 'Filipino', 'message': 'Mga pagsasalin ng %s', 'endonym': 'Tagalog'}),
    ('fi', {'name': 'Finnish', 'message': 'Käännökset tekstille %s', 'endonym': 'Suomi'}),
    ('fr', {'name': 'French', 'message': 'Traductions de %s', 'endonym': 'Français'}),
    ('gl', {'name': 'Galician', 'message': 'Traducións de %s', 'endonym': 'Galego'}),
    ('ka', {'name': 'Georgian', 'message': '%s-ის თარგმანები', 'endonym': 'ქართული'}),
    ('de', {'name': 'German', 'message': 'Übersetzungen für %s', 'endonym': 'Deutsch'}),
    ('el', {'name': 'Greek', 'message': 'Μεταφράσεις του %s', 'endonym': 'Ελληνικά'}),
    ('gu', {'name': 'Gujarati', 'message': '%s ના અનુવાદ', 'endonym': 'ગુજરાતી'}),
    ('ht', {'name': 'Haitian Creole', 'message': 'Tradiksyon %s', 'endonym': 'Kreyòl Ayisyen'}),
    ('ha', {'name': 'Hausa', 'message': 'Fassarar %s', 'endonym': 'Hausa'}),
    ('he', {'rtl': 'true', 'name': 'Hebrew', 'message': 'תרגומים של %s', 'endonym': 'עִבְרִית'}),
    ('hi', {'name': 'Hindi', 'message': '%s के अनुवाद', 'endonym': 'हिन्दी'}),
    ('hmn', {'name': 'Hmong', 'message': 'Lus txhais: %s', 'endonym': 'Hmoob'}),
    ('hu', {'name': 'Hungarian', 'message': '%s fordításai', 'endonym': 'Magyar'}),
    ('is', {'name': 'Icelandic', 'message': 'Þýðingar á %s', 'endonym': 'Íslenska'}),
    ('ig', {'name': 'Igbo', 'message': 'Ntụgharị asụsụ nke %s', 'endonym': 'Igbo'}),
    ('id', {'name': 'Indonesian', 'message': 'Terjemahan dari %s', 'endonym': 'Bahasa Indonesia'}),
    ('ga', {'name': 'Irish', 'message': 'Aistriúcháin ar %s', 'endonym': 'Gaeilge'}),
    ('it', {'name': 'Italian', 'message': 'Traduzioni di %s', 'endonym': 'Italiano'}),
    ('ja', {'name': 'Japanese', 'message': '「%s」の翻訳', 'endonym': '日本語'}),
    ('jv', {'name': 'Javanese', 'message': 'Terjemahan', 'endonym': 'Basa Jawa'}),
    ('kn', {'name': 'Kannada', 'message': '%s ನ ಅನುವಾದಗಳು', 'endonym': 'ಕನ್ನಡ'}),
    ('kk', {'name': 'Kazakh', 'message': '%s аудармалары', 'endonym': 'Қазақ тілі'}),
    ('km', {'name': 'Khmer', 'message': 'ការ\u200bបក\u200bប្រែ\u200bនៃ %s', 'endonym': 'ភាសាខ្មែរ'}),
    ('ko', {'name': 'Korean', 'message': '%s의 번역', 'endonym': '한국어'}),
    ('lo', {'name': 'Lao', 'message': 'ການ\u200bແປ\u200bພາ\u200bສາ\u200bຂອງ %s', 'endonym': 'ລາວ'}),
    ('la', {'name': 'Latin', 'message': 'Versio de %s', 'endonym': 'Latina'}),
    ('lv', {'name': 'Latvian', 'message': '%s tulkojumi', 'endonym': 'Latviešu'}),
    ('lt', {'name': 'Lithuanian', 'message': '„%s“ vertimai', 'endonym': 'Lietuvių'}),
    ('mk', {'name': 'Macedonian', 'message': 'Преводи на %s', 'endonym': 'Македонски'}),
    ('mg', {'name': 'Malagasy', 'message': "Dikan'ny %s", 'endonym': 'Malagasy'}),
    ('ms', {'name': 'Malay', 'message': 'Terjemahan %s', 'endonym': 'Bahasa Melayu'}),
    ('ml', {'name': 'Malayalam', 'message': '%s എന്നതിന്റെ വിവർത്തനങ്ങൾ', 'endonym': 'മലയാളം'}),
    ('mt', {'name': 'Maltese', 'message': "Traduzzjonijiet ta' %s", 'endonym': 'Malti'}),
    ('mi', {'name': 'Maori', 'message': 'Ngā whakamāoritanga o %s', 'endonym': 'Māori'}),
    ('mr', {'name': 'Marathi', 'message': '%s ची भाषांतरे', 'endonym': 'मराठी'}),
    ('mn', {'name': 'Mongolian', 'message': '%s-н орчуулга', 'endonym': 'Монгол'}),
    ('my', {'name': 'Myanmar', 'message': '%s၏ ဘာသာပြန်ဆိုချက်များ', 'endonym': 'မြန်မာစာ'}),
    ('ne', {'name': 'Nepali', 'message': '%sका अनुवाद', 'endonym': 'नेपाली'}),
    ('no', {'name': 'Norwegian', 'message': 'Oversettelser av %s', 'endonym': 'Norsk'}),
    ('fa', {'rtl': 'true', 'name': 'Persian', 'message': 'ترجمه\u200cهای %s', 'endonym': 'فارسی'}),
    ('pa', {'name': 'Punjabi', 'message': 'ਦੇ ਅਨੁਵਾਦ%s', 'endonym': 'ਪੰਜਾਬੀ'}),
    ('pl', {'name': 'Polish', 'message': 'Tłumaczenia %s', 'endonym': 'Polski'}),
    ('pt', {'name': 'Portuguese', 'message': 'Traduções de %s', 'endonym': 'Português'}),
    ('ro', {'name': 'Romanian', 'message': 'Traduceri pentru %s', 'endonym': 'Română'}),
    ('ru', {'name': 'Russian', 'message': '%s: варианты перевода', 'endonym': 'Русский'}),
    ('sr', {'name': 'Serbian', 'message': 'Преводи за „%s“', 'endonym': 'српски'}),
    ('st', {'name': 'Sesotho', 'message': 'Liphetolelo tsa %s', 'endonym': 'Sesotho'}),
    ('si', {'name': 'Sinhala', 'message': '%s හි පරිවර්තන', 'endonym': 'සිංහල'}),
    ('sk', {'name': 'Slovak', 'message': 'Preklady výrazu: %s', 'endonym': 'Slovenčina'}),
    ('sl', {'name': 'Slovenian', 'message': 'Prevodi za %s', 'endonym': 'Slovenščina'}),
    ('so', {'name': 'Somali', 'message': 'Turjumaada %s', 'endonym': 'Soomaali'}),
    ('es', {'name': 'Spanish', 'message': 'Traducciones de %s', 'endonym': 'Español'}),
    ('su', {'name': 'Sundanese', 'message': 'Tarjamahan tina %s', 'endonym': 'Basa Sunda'}),
    ('sw', {'name': 'Swahili', 'message': 'Tafsiri ya %s', 'endonym': 'Kiswahili'}),
    ('sv', {'name': 'Swedish', 'message': 'Översättningar av %s', 'endonym': 'Svenska'}),
    ('tg', {'name': 'Tajik', 'message': 'Тарҷумаҳои %s', 'endonym': 'Тоҷикӣ'}),
    ('ta', {'name': 'Tamil', 'message': '%s இன் மொழிபெயர்ப்புகள்', 'endonym': 'தமிழ்'}),
    ('te', {'name': 'Telugu', 'message': '%s యొక్క అనువాదాలు', 'endonym': 'తెలుగు'}),
    ('th', {'name': 'Thai', 'message': 'คำแปลของ %s', 'endonym': 'ไทย'}),
    ('tr', {'name': 'Turkish', 'message': '%s çevirileri', 'endonym': 'Türkçe'}),
    ('uk', {'name': 'Ukrainian', 'message': 'Переклади слова або виразу "%s"', 'endonym': 'Українська'}),
    ('ur', {'rtl': 'true', 'name': 'Urdu', 'message': 'کے ترجمے %s', 'endonym': 'اُردُو'}),
    ('uz', {'name': 'Uzbek', 'message': '%s tarjimalari', 'endonym': 'Oʻzbek tili'}),
    ('vi', {'name': 'Vietnamese', 'message': 'Bản dịch của %s', 'endonym': 'Tiếng Việt'}),
    ('cy', {'name': 'Welsh', 'message': 'Cyfieithiadau %s', 'endonym': 'Cymraeg'}),
    ('yi', {'rtl': 'true', 'name': 'Yiddish', 'message': 'איבערזעצונגען פון %s', 'endonym': 'ייִדיש'}),
    ('yo', {'name': 'Yoruba', 'message': 'Awọn itumọ ti %s', 'endonym': 'Yorùbá'}),
    ('zu', {'name': 'Zulu', 'message': 'Ukuhumusha i-%s', 'endonym': 'isiZulu'})
])

# Aliases for some locales
# See: <http://www.loc.gov/standards/iso639-2/php/code_changes.php>
LOCALE_ALIAS = {
    "in": "id",  # withdrawn language code for Indonesian
    "iw": "he",  # withdrawn language code for Hebrew
    "ji": "yi",  # withdrawn language code for Yiddish

    "c" : "en"   # docker ubuntu use C.utf8 for english
    "jw": "jv",  # withdrawn language code for Javanese
    "mo": "ro",  # Moldavian or Moldovan considered a variant of the Romanian language
    "sh": "sr",  # Serbo-Croatian: prefer Serbian
    "zh": "zh-CN",  # Chinese: prefer Chinese Simplified
    "zh-cn": "zh-CN",  # lowercase
    "zh-tw": "zh-TW",  # lowercase
}
# TODO: any more aliases supported by Google Translate?


def get_lang_code(code):
    """
       Get locale key by language code or alias.
       return nothing if not found
    """

    # case-insensitive
    code = code.lower()
    if code in LOCALE_MAP or code == "auto":
        return code
    elif code in LOCALE_ALIAS:
        return LOCALE_ALIAS[code]
    else:
        return

def get_lang_info(code):
    return LOCALE_MAP.get(code, LOCALE_MAP[DEFAULT_LANG_CODE])

def parse_lang_code(lang):
    parse_lang_match = re.match('^([a-z][a-z]?[a-z]?)(_|$)', lang.lower())
    group = parse_lang_match.groups()
    code = get_lang_code(group[0])

    # Detect region identifier
    ## Regions using Chinese Simplified: China, Singapore
    if re.match('^zh_(CN|SG)', lang):
        code = "zh-CN"
    ## Regions using Chinese Traditional: Taiwan, Hong Kong
    elif re.match('^zh_(TW|HK)', lang):
        code = "zh-TW"
    return code or DEFAULT_LANG_CODE


def init_user_lang():
    code, encoding = locale.getdefaultlocale()
    user_lang = parse_lang_code(code)
    return user_lang


USER_LANG = init_user_lang()
__all__ = ['USER_LANG']
