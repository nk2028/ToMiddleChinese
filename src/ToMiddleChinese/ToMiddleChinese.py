# -*- coding: utf-8 -*-

from opencc import OpenCC
from os import path
import pygtrie

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
	with open(path.join(here, 'dict', name + '.dict.yaml'), encoding='utf-8') as f:
		for line in f:
			k, v = line.rstrip().split('\t')
			t[k] = v
	return t

def get_middle_chinese_list_inner(s, t):
	s_t = cc_hk.convert(cc_s.convert(s))
	# s_t = cc_s.convert(s)
	l = []  # list of converted words
	while s:
		p = t.longest_prefix(s_t)  # match the longest prefix
		if not p:  # if the prefix does not exist
			l += [(s[0], None)]  # append (the first character, no result)
			s = s[1:]  # remove the first character from the string
			s_t = s_t[1:]
		else:  # if exists
			n = len(p.key)
			l += zip(s[:n], p.value.split(' '))
			s = s[n:]  # remove the word from the string
			s_t = s_t[n:]
	return l  # A list of chars and middle_chinese

def get_middle_chinese_list(s, t):
	res = []
	for k in jieba.cut(s):
		res.extend(get_middle_chinese_list_inner(k, t))
	return res

def get_middle_chinese(s, t, f = '(%s)'):
	l = ''
	for k, v in get_middle_chinese_list(s, t):
		l += k + (f % v if v else '')
	return l

def get_middle_chinese_text(s, t, sp = ' '):
	l = []
	for k, v in get_middle_chinese_list(s, t):
		if v:
			l += [v]
	return sp.join(l)

dict_pos = load_dict('pos')
dict_kyonh = load_dict('kyonh')
dict_unt = load_dict('unt')
dict_tupa = load_dict('tupa')

get_pos_list = lambda s: get_middle_chinese_list(s, dict_pos)
get_kyonh_list = lambda s: get_middle_chinese_list(s, dict_kyonh)
get_unt_list = lambda s: get_middle_chinese_list(s, dict_unt)
get_tupa_list = lambda s: get_middle_chinese_list(s, dict_tupa)

get_pos = lambda s: get_middle_chinese(s, dict_pos)
get_kyonh = lambda s: get_middle_chinese(s, dict_kyonh)
get_unt = lambda s: get_middle_chinese(s, dict_unt, '[%s]')
get_tupa = lambda s: get_middle_chinese(s, dict_tupa)

get_pos_text = lambda s: get_middle_chinese_text(s, dict_pos)
get_kyonh_text = lambda s: get_middle_chinese_text(s, dict_kyonh)
get_unt_text = lambda s: get_middle_chinese_text(s, dict_unt, '.')
get_tupa_text = lambda s: get_middle_chinese_text(s, dict_tupa)
