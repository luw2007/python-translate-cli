#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    从 simplejson 中剥离 JSONArray, 实现解析sparse_array

"""
from __future__ import absolute_import
import re
import sys
import struct

__all__ = ['loads']

"""Python 3 compatibility shims"""
if sys.version_info[0] < 3:
    PY3 = False

    def b(s):
        return s

    def u(s):
        return unicode(s, 'unicode_escape')

    import cStringIO as StringIO

    StringIO = BytesIO = StringIO.StringIO
    text_type = unicode
    binary_type = str
    string_types = (basestring,)
    integer_types = (int, long)
    unichr = unichr
    reload_module = reload

    def fromhex(s):
        return s.decode('hex')

else:
    PY3 = True
    if sys.version_info[:2] >= (3, 4):
        from importlib import reload as reload_module
    else:
        from imp import reload as reload_module
    import codecs

    def b(s):
        return codecs.latin_1_encode(s)[0]

    def u(s):
        return s

    import io

    StringIO = io.StringIO
    BytesIO = io.BytesIO
    text_type = str
    binary_type = bytes
    string_types = (str,)
    integer_types = (int,)

    def unichr(s):
        return u(chr(s))

    def fromhex(s):
        return bytes.fromhex(s)

long_type = integer_types[-1]

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL

WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
WHITESPACE_STR = ' \t\n\r'

NUMBER_RE = re.compile(r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
                       FLAGS)


def _floatconstants():
    _BYTES = fromhex('7FF80000000000007FF0000000000000')
    # The struct module in Python 2.4 would get frexp() out of range here
    # when an endian is specified in the format string. Fixed in Python 2.5+
    if sys.byteorder != 'big':
        _BYTES = _BYTES[:8][::-1] + _BYTES[8:][::-1]
    nan, inf = struct.unpack('dd', _BYTES)
    return nan, inf, -inf


NaN, PosInf, NegInf = _floatconstants()

_CONSTANTS = {
    '-Infinity': NegInf,
    'Infinity': PosInf,
    'NaN': NaN,
}

STRINGCHUNK = re.compile(r'(.*?)(["\\\x00-\x1f])', FLAGS)
BACKSLASH = {
    '"': u('"'), '\\': u('\u005c'), '/': u('/'),
    'b': u('\b'), 'f': u('\f'), 'n': u('\n'), 'r': u('\r'), 't': u('\t'),
}
DEFAULT_ENCODING = "utf-8"

encoding = DEFAULT_ENCODING
strict = True


def loads(s, idx=0, _w=WHITESPACE.match, _PY3=PY3):
    if _PY3 and isinstance(s, binary_type):
        s = s.decode(encoding)
    obj, end = raw_decode(s)
    end = _w(s, end).end()
    if end != len(s):
        raise JSONDecodeError("Extra data", s, end, len(s))
    return obj


def raw_decode(s, idx=0, _w=WHITESPACE.match, _PY3=PY3):
    if idx < 0:
        # Ensure that raw_decode bails on negative indexes, the regex
        # would otherwise mask this behavior. #98
        raise JSONDecodeError('Expecting value', s, idx)
    if _PY3 and not isinstance(s, text_type):
        raise TypeError("Input string must be text, not bytes")
    # strip UTF-8 bom
    if len(s) > idx:
        ord0 = ord(s[idx])
        if ord0 == 0xfeff:
            idx += 1
        elif ord0 == 0xef and s[idx:idx + 3] == '\xef\xbb\xbf':
            idx += 3
    return scan_once(s, idx=_w(s, idx).end())


def errmsg(msg, doc, pos, end=None):
    lineno, colno = linecol(doc, pos)
    msg = msg.replace('%r', repr(doc[pos:pos + 1]))
    if end is None:
        fmt = '%s: line %d column %d (char %d)'
        return fmt % (msg, lineno, colno, pos)
    endlineno, endcolno = linecol(doc, end)
    fmt = '%s: line %d column %d - line %d column %d (char %d - %d)'
    return fmt % (msg, lineno, colno, endlineno, endcolno, pos, end)


def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos + 1
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return lineno, colno


class JSONDecodeError(ValueError):
    """Subclass of ValueError with the following additional properties:

    msg: The unformatted error message
    doc: The JSON document being parsed
    pos: The start index of doc where parsing failed
    end: The end index of doc where parsing failed (may be None)
    lineno: The line corresponding to pos
    colno: The column corresponding to pos
    endlineno: The line corresponding to end (may be None)
    endcolno: The column corresponding to end (may be None)

    """
    # Note that this exception is used from _speedups
    def __init__(self, msg, doc, pos, end=None):
        ValueError.__init__(self, errmsg(msg, doc, pos, end=end))
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.end = end
        self.lineno, self.colno = linecol(doc, pos)
        if end is not None:
            self.endlineno, self.endcolno = linecol(doc, end)
        else:
            self.endlineno, self.endcolno = None, None

    def __reduce__(self):
        return self.__class__, (self.msg, self.doc, self.pos, self.end)


def _scan_once(string, idx):
    errmsg = 'Expecting value'
    try:
        nextchar = string[idx]
    except IndexError:
        raise JSONDecodeError(errmsg, string, idx)

    if nextchar == '"':
        return parse_string(string, idx + 1, encoding, strict)
    elif nextchar == ',':
        return None, idx
    elif nextchar == ']':
        return None, idx
    elif nextchar == '[':
        return parse_array((string, idx + 1), _scan_once)
    elif nextchar == 'n' and string[idx:idx + 4] == 'null':
        return None, idx + 4
    elif nextchar == 't' and string[idx:idx + 4] == 'true':
        return True, idx + 4
    elif nextchar == 'f' and string[idx:idx + 5] == 'false':
        return False, idx + 5

    m = match_number(string, idx)
    if m is not None:
        integer, frac, exp = m.groups()
        if frac or exp:
            res = parse_float(integer + (frac or '') + (exp or ''))
        else:
            res = parse_int(integer)
        return res, m.end()
    elif nextchar == 'N' and string[idx:idx + 3] == 'NaN':
        return parse_constant('NaN'), idx + 3
    elif nextchar == 'I' and string[idx:idx + 8] == 'Infinity':
        return parse_constant('Infinity'), idx + 8
    elif nextchar == '-' and string[idx:idx + 9] == '-Infinity':
        return parse_constant('-Infinity'), idx + 9
    else:
        raise JSONDecodeError(errmsg, string, idx)


def scan_once(string, idx):
    if idx < 0:
        # Ensure the same behavior as the C speedup, otherwise
        # this would work for *some* negative string indices due
        # to the behavior of __getitem__ for strings. #98
        raise JSONDecodeError('Expecting value', string, idx)
    try:
        return _scan_once(string, idx)
    finally:
        pass
        # memo.clear()


def JSONArray(state, scan_once, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
    (s, end) = state
    values = []
    nextchar = s[end:end + 1]
    if nextchar in _ws:
        end = _w(s, end + 1).end()
        nextchar = s[end:end + 1]
    # Look-ahead for trivial empty array
    if nextchar == ']':
        return values, end + 1
    elif nextchar == '':
        raise JSONDecodeError("Expecting value or ']'", s, end)
    _append = values.append
    while True:
        value, end = scan_once(s, end)
        _append(value)
        nextchar = s[end:end + 1]
        if nextchar in _ws:
            end = _w(s, end + 1).end()
            nextchar = s[end:end + 1]
        end += 1
        if nextchar == ']':
            break
        elif nextchar != ',':
            raise JSONDecodeError("Expecting ',' delimiter or ']'", s, end - 1)

        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()
        except IndexError:
            pass

    return values, end


def py_scanstring(s, end, encoding=None, strict=True,
                  _b=BACKSLASH, _m=STRINGCHUNK.match, _join=u('').join,
                  _PY3=PY3, _maxunicode=sys.maxunicode):
    """Scan the string s for a JSON string. End is the index of the
    character in s after the quote that started the JSON string.
    Unescapes all valid JSON string escape sequences and raises ValueError
    on attempt to decode an invalid string. If strict is False then literal
    control characters are allowed in the string.

    Returns a tuple of the decoded string and the index of the character in s
    after the end quote."""
    if encoding is None:
        encoding = DEFAULT_ENCODING
    chunks = []
    _append = chunks.append
    begin = end - 1
    while 1:
        chunk = _m(s, end)
        if chunk is None:
            raise JSONDecodeError(
                "Unterminated string starting at", s, begin)
        end = chunk.end()
        content, terminator = chunk.groups()
        # Content is contains zero or more unescaped string characters
        if content:
            if not _PY3 and not isinstance(content, text_type):
                content = text_type(content, encoding)
            _append(content)
        # Terminator is the end of string, a literal control character,
        # or a backslash denoting that an escape sequence follows
        if terminator == '"':
            break
        elif terminator != '\\':
            if strict:
                msg = "Invalid control character %r at"
                raise JSONDecodeError(msg, s, end)
            else:
                _append(terminator)
                continue
        try:
            esc = s[end]
        except IndexError:
            raise JSONDecodeError(
                "Unterminated string starting at", s, begin)
        # If not a unicode escape sequence, must be in the lookup table
        if esc != 'u':
            try:
                char = _b[esc]
            except KeyError:
                msg = "Invalid \\X escape sequence %r"
                raise JSONDecodeError(msg, s, end)
            end += 1
        else:
            # Unicode escape sequence
            msg = "Invalid \\uXXXX escape sequence"
            esc = s[end + 1:end + 5]
            escX = esc[1:2]
            if len(esc) != 4 or escX == 'x' or escX == 'X':
                raise JSONDecodeError(msg, s, end - 1)
            try:
                uni = int(esc, 16)
            except ValueError:
                raise JSONDecodeError(msg, s, end - 1)
            end += 5
            # Check for surrogate pair on UCS-4 systems
            # Note that this will join high/low surrogate pairs
            # but will also pass unpaired surrogates through
            if (_maxunicode > 65535 and
                            uni & 0xfc00 == 0xd800 and
                        s[end:end + 2] == '\\u'):
                esc2 = s[end + 2:end + 6]
                escX = esc2[1:2]
                if len(esc2) == 4 and not (escX == 'x' or escX == 'X'):
                    try:
                        uni2 = int(esc2, 16)
                    except ValueError:
                        raise JSONDecodeError(msg, s, end)
                    if uni2 & 0xfc00 == 0xdc00:
                        uni = 0x10000 + (((uni - 0xd800) << 10) |
                                         (uni2 - 0xdc00))
                        end += 6
            char = unichr(uni)
        # Append the unescaped character
        _append(char)
    return _join(chunks), end


parse_string = py_scanstring
parse_int = int
parse_float = float
parse_array = JSONArray
parse_constant = _CONSTANTS.__getitem__

match_number = NUMBER_RE.match

