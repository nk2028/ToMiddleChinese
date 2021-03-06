# -*- coding: utf-8 -*-

from os import path
from urllib import request

here = path.abspath(path.dirname(__file__))

def download_file_if_not_exist(url, file_path):
	'''Download the dictionary file to the current folder if not exists.'''
	if not path.exists(path.join(here, file_path)):
		request.urlretrieve(url, path.join(here, file_path))

download_file_if_not_exist('https://raw.githubusercontent.com/biopolyhedron/rime-middle-chinese/542245ed087988b28e1e94a2a3d352865fb8e963/zyenpheng.dict.yaml', 'zyenpheng.dict.yaml')
download_file_if_not_exist('https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/dict.txt.big', 'src/ToMiddleChinese/dict/dict.big.txt')
download_file_if_not_exist('https://cdn.jsdelivr.net/npm/opencc-data@1.0.3/data/HKVariantsRev.txt', 'src/ToMiddleChinese/dict/HKVariantsRev.txt')
download_file_if_not_exist('https://cdn.jsdelivr.net/npm/opencc-data@1.0.3/data/HKVariantsRevPhrases.txt', 'src/ToMiddleChinese/dict/HKVariantsRevPhrases.txt')

def freq_str_to_float(s):
	'''Convert frequency data in the dictionary file to float.
	>>> freq_str_to_float('2')
	2.0
	>>> freq_str_to_float('2%')
	0.02
	'''
	if s[-1] == '%':
		return float(s[:-1]) * 0.01
	else:
		return float(s)

DEFAULT_FREQ = 0.07

def build_dict():
	'''Create a dictionary of all the words with jyutping data.
	If there are multiple possibilities, the one with higher frequency is used.
	'''
	d = {}
	with open(path.join(here, 'zyenpheng.dict.yaml')) as f:
		for line in f:
			if line == '...\n':
				break
		next(f)
		for line in f:
			if line and line[0] != '#':
				parts = line.rstrip().split('\t')
				if len(parts) == 2:
					字, 粵拼 = parts
					詞頻 = DEFAULT_FREQ
				elif len(parts) == 3:
					字, 粵拼, 詞頻 = parts
					try:
						詞頻 = freq_str_to_float(詞頻)
					except ValueError:
						continue

				is_valid_length = len(字) == 粵拼.count(' ') + 1

				if is_valid_length or len(字) == 1:  # 瓩
					元字 = d.get(字)
					if not 元字:
						d[字] = (粵拼, 詞頻)
					else:
						元粵拼, 元詞頻 = 元字

						should_change = (詞頻 > 元詞頻)
						if should_change:
							d[字] = (粵拼, 詞頻)
	return {k: v[0] for k, v in d.items()}

def write_dict(d):
	with open(path.join(here, 'zyenpheng.dict.simple.yaml'), 'w') as f:
		for k, v in d.items():
			print(k + '\t' + v, file=f)

write_dict(build_dict())
