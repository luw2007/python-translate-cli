import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('pytrans/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='python-translate-cli',
    author='luw2007',
    author_email='luw20007@gmail.com',
    version=version,
    url='http://github.com/luw2007/python-translate-cli',
    license='The MIT License',
    packages=['pytrans'],
    description='use Google Translate to query word, like soimort/translate-shell.'
                'But verbose about Definitions, Synonyms, Example.',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        pytrans=pytrans.main:cli
    ''',

)
