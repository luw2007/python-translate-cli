import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('pytrans/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='pytrans',
    author='luw2007',
    author_email='luw20007@gmail.com',
    version=version,
    url='http://github.com/luw2007/python-translate-cli',
    license='The MIT License',
    packages=['pytrans'],
    description='use Google Translate to query word, like soimort/translate-shell.'
                'But verbose about Definitions, Synonyms, Example.',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        pytrans=pytrans:cli
    ''',

)
