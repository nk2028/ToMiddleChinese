# ToMiddleChinese [![Release Python Package](https://github.com/nk2028/ToMiddleChinese/actions/workflows/python-publish.yml/badge.svg)](https://github.com/nk2028/ToMiddleChinese/actions/workflows/python-publish.yml)

### Install

```sh
$ pip install ToMiddleChinese
```

### Usage

```python
>>> import ToMiddleChinese

>>> # 音韻地位 (Description of Phonological Position)
>>> ToMiddleChinese.get_pos_list('遙襟甫暢，逸興遄飛')
[('遙', '以開三宵平'), ('襟', '見開三B侵平'), ('甫', '幫三虞上'), ('暢', '徹開三陽去'), ('，', None), ('逸', '以開三眞入'), ('興', '曉開三蒸平'), ('遄', '常合三仙平'), ('飛', '幫三微平')]
>>> ToMiddleChinese.get_pos('遙襟甫暢，逸興遄飛')
'遙(以開三宵平)襟(見開三B侵平)甫(幫三虞上)暢(徹開三陽去)，逸(以開三眞入)興(曉開三蒸平)遄(常合三仙平)飛(幫三微平)'
>>> ToMiddleChinese.get_pos_text('遙襟甫暢，逸興遄飛')
'以開三宵平 見開三B侵平 幫三虞上 徹開三陽去 以開三眞入 曉開三蒸平 常合三仙平 幫三微平'

>>> # 切韻拼音 (Tshet-uinh Phonetic Alphabet)
>>> ToMiddleChinese.get_tupa_list('遙襟甫暢，逸興遄飛')
[('遙', 'jiew'), ('襟', 'kyim'), ('甫', 'puoq'), ('暢', 'trhyangh'), ('，', None), ('逸', 'jit'), ('興', 'hyngh'), ('遄', 'djwien'), ('飛', 'puj')]
>>> ToMiddleChinese.get_tupa('遙襟甫暢，逸興遄飛')
'遙(jiew)襟(kyim)甫(puoq)暢(trhyangh)，逸(jit)興(hyngh)遄(djwien)飛(puj)'
>>> ToMiddleChinese.get_tupa_text('遙襟甫暢，逸興遄飛')
'jiew kyim puoq trhyangh jit hyngh djwien puj'

>>> # 古韻羅馬字 (Koxyonh’s Romanization)
>>> ToMiddleChinese.get_kyonh_list('遙襟甫暢，逸興遄飛')
[('遙', 'jeu'), ('襟', 'kim'), ('甫', 'pyox'), ('暢', 'thriangh'), ('，', None), ('逸', 'jit'), ('興', 'hingh'), ('遄', 'zjyen'), ('飛', 'pyoi')]
>>> ToMiddleChinese.get_kyonh('遙襟甫暢，逸興遄飛')
'遙(jeu)襟(kim)甫(pyox)暢(thriangh)，逸(jit)興(hingh)遄(zjyen)飛(pyoi)'
>>> ToMiddleChinese.get_kyonh_text('遙襟甫暢，逸興遄飛')
'jeu kim pyox thriangh jit hingh zjyen pyoi'

>>> # unt 切韻擬音 (unt’s Qieyun Reconstruction)
>>> ToMiddleChinese.get_unt_list('遙襟甫暢，逸興遄飛')
[('遙', 'jew'), ('襟', 'kɹim'), ('甫', 'púo'), ('暢', 'ʈʰàɴ'), ('，', None), ('逸', 'jit'), ('興', 'xɨ̀ŋ'), ('遄', 'dʑwen'), ('飛', 'puj')]
>>> ToMiddleChinese.get_unt('遙襟甫暢，逸興遄飛')
'遙[jew]襟[kɹim]甫[púo]暢[ʈʰàɴ]，逸[jit]興[xɨ̀ŋ]遄[dʑwen]飛[puj]'
>>> ToMiddleChinese.get_unt_text('遙襟甫暢，逸興遄飛')
'jew.kɹim.púo.ʈʰàɴ.jit.xɨ̀ŋ.dʑwen.puj'
```
