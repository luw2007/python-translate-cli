# python-translate-cli
use Google Translate to query word,  like soimort/translate-shell. But verbose info about Definitions, Synonyms, Example

    $ pytrans apple
    苹果
    apple
    [noun]: 2
        苹果
             apple
        苹
             apple

    苹果, 苹果公司, 的苹果, 苹果的, 苹
    See also
        apple pie, apple juice, apple tree, custard apple, apple strudel, apple cake, Adam's apple, crab apple, rose apple, apple-pie

    menu: m: main; n: new word; f: verbose from_lang; t: verbose to_lang; v: more all; q: quit; [q]



## Usage:

    git clone https://github.com/luw2007/pytrans
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