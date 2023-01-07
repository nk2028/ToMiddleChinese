# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

if not path.exists(path.join(here, 'src/ToMiddleChinese/dict/pos.dict.yaml')):
	raise Exception('Please run preprocess.js by `npm ci` first.')

with open(path.join(here, 'README.md')) as f:
	long_description = f.read()

with open(path.join(here, 'src/ToMiddleChinese/version.py')) as f:
	exec(f.read())

setup(
	name='ToMiddleChinese',
	version=__version__,
	description='中古漢語自動標註工具 Middle Chinese Pronunciation Automatic Labeling Tool',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/nk2028/ToMiddleChinese',
	author='Ngiox Khyen 2028 Project',
	author_email='support@mail.nk2028.shn.hk',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Text Processing :: Linguistic',
		'Natural Language :: Chinese (Simplified)',
		'Natural Language :: Chinese (Traditional)',
		'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11'
	],
	keywords='chinese middle-chinese linguistics nlp natural-language-processing',
	packages=find_packages('src'),
	package_dir={'': 'src'},
	package_data={
		'ToMiddleChinese': ['dict/*'],
	},
	include_package_data=True,
	python_requires='>=3.5, <4',
	install_requires=['pygtrie', 'opencc!=1.1.1', 'jieba'],
	entry_points={},
	project_urls={
		'Bug Reports': 'https://github.com/nk2028/ToMiddleChinese/issues',
		'Source': 'https://github.com/nk2028/ToMiddleChinese',
	},
	zip_safe=False
)
