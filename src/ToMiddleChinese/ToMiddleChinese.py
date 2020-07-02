# -*- coding: utf-8 -*-

from opencc import OpenCC
from os import path
import pygtrie
import re
import urllib.request

here = path.abspath(path.dirname(__file__))

import jieba
import logging
jieba.setLogLevel(logging.INFO)

user_dict = 'dict.big.txt'

jieba.set_dictionary(path.join(here, 'dict', user_dict))
jieba.initialize()

# Initialize

cc_s = OpenCC('s2t.json')  # TODO: Cannot handle 沈
cc_hk = OpenCC(path.join(here, 'dict', 'hk2t.json'))  # Wait for https://github.com/BYVoid/OpenCC/issues/406

def load_dict(name):
	t = pygtrie.CharTrie()
	with open(path.join(here, 'dict', 'zyenpheng.dict.' + name + '.yaml')) as f:
		for line in f:
			k, v = line.rstrip().split('\t')
			t[k] = v
	return t

def get_middle_chinese_list_inner(s, t):
	def replace_words_plain(s, t):
		s_t = cc_hk.convert(cc_s.convert(s))
		#s_t = cc_s.convert(s)
		l = []  # list of converted words
		while s:
			longest_prefix = t.longest_prefix(s_t)  # match the longest prefix
			if not longest_prefix:  # if the prefix does not exist
				l.append((s[0], None))  # append (the first character, no result)
				s = s[1:]  # remove the first character from the string
				s_t = s_t[1:]
			else:  # if exists
				word, jyut = longest_prefix.key, longest_prefix.value
				if len(word) == 1:
					l.append((s[0], jyut))
					s = s[1:]  # remove the word from the string
					s_t = s_t[1:]
				else:
					for k, v in zip(s[:len(word)], jyut.split(' ')):
						l.append((k, v))
					s = s[len(word):]  # remove the word from the string
					s_t = s_t[len(word):]  # remove the word from the string
		return l  # A list of chars and middle_chinese

	return replace_words_plain(s, t)

def get_middle_chinese_list(s, t):
	res = []
	for k in jieba.cut(s):
		res.extend(get_middle_chinese_list_inner(k, t))
	return res

def get_middle_chinese(s, t):
	l = []
	for k, v in get_middle_chinese_list(s, t):
		if v is None:
			l.append(k)
		else:
			l.append(k + '(' + v + ')')
	return ''.join(l)

dict_qimyonhmieuzsjyt = load_dict('qimyonhmieuzsjyt')
dict_kuxyonh = load_dict('kuxyonh')
dict_unt = load_dict('unt')

get_qimyonhmieuzsjyt_list = lambda s: get_middle_chinese_list(s, dict_qimyonhmieuzsjyt)
get_kuxyonh_list = lambda s: get_middle_chinese_list(s, dict_kuxyonh)
get_unt_list = lambda s: get_middle_chinese_list(s, dict_unt)

get_qimyonhmieuzsjyt = lambda s: get_middle_chinese(s, dict_qimyonhmieuzsjyt)
get_kuxyonh = lambda s: get_middle_chinese(s, dict_kuxyonh)
get_unt = lambda s: get_middle_chinese(s, dict_unt)
