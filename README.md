# python-translate-cli
use Google Translate to query word,  like soimort/translate-shell. But verbose info about Definitions, Synonyms, Example
    ![Alt screenshots](/../screenshots/pytrans.gif?raw=true "Pytrans apple")


## Usage:

    git clone https://github.com/luw2007/python-translate-cli pytrans
    cd pytrans
    pip install --editable .
    pytrans --help


## FEATURE:
- verbose info about Definitions, Synonyms, Example
- pickle cache
- python3 support
- 实现解析sparse_array, 移除对simplejson 的hack

## TODO:
- 支持句子搜索
- 增加界面, 方便跳转不同的单词