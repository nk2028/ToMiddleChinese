const fs = require('fs')
const Qieyun = require('qieyun');
const kyonh = require('./kyonh.js');
const unt = require('./unt.js');

__d = {};

for (let 小韻號 = 1; 小韻號 <= 3874; 小韻號++) {
	const 音韻地位 = Qieyun.get音韻地位(小韻號);
	__d[kyonh(音韻地位)] = 音韻地位;
}

function rev_inner(s) {
	let res = __d[s];
	if (res)
		return res.音韻描述;
}

function 音韻描述2音韻地位(音韻描述) {
	var pattern = /(.)(.)(.)([AB]?)(.)(.)/gu;  // 解析音韻地位
	var arr = pattern.exec(音韻描述);
	return new Qieyun.音韻地位(arr[1], arr[2], arr[3], arr[4] || null, arr[5], arr[6]);
}

function kyonh2音韻描述(s) {
	let res = rev_inner(s);
	if (res) {
		return res;
	}

	if (s.endsWith('x')) {
		res = rev_inner(s.slice(0, -1));
		if (res)
			return res.replace('平', '上');
	}

	if (s.endsWith('h')) {
		res = rev_inner(s.slice(0, -1));
		if (res)
			return res.replace('平', '去');
	}

	res = rev_inner(s + 'x');
	if (res)
		return res.replace('上', '平');

	res = rev_inner(s + 'h');
	if (res)
		return res.replace('去', '平');
}

var logger_qimyonhmieuzsjyt = fs.createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.qimyonhmieuzsjyt.yaml');
var logger_kyonh = fs.createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.kyonh.yaml');
var logger_unt = fs.createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.unt.yaml');

var lineReader = require('readline').createInterface({
	input: require('fs').createReadStream('zyenpheng.dict.simple.yaml')
});

lineReader.on('line', function (line) {
	let [字, 羅馬字們] = line.split('\t');
	羅馬字們 = 羅馬字們.split(' ').map(kyonh2音韻描述);
	if (!羅馬字們.some(x => !x)) /* Sucessfully converted */ {
		logger_qimyonhmieuzsjyt.write(字 + '\t' + 羅馬字們.join(' ') + '\n');

		let x = 羅馬字們.map(音韻描述2音韻地位).map(kyonh);
		logger_kyonh.write(字 + '\t' + x.join(' ') + '\n');

		x = 羅馬字們.map(音韻描述2音韻地位).map(unt);
		logger_unt.write(字 + '\t' + x.join(' ') + '\n');
	} else /* Error */ {
		console.log('Unhandled: ' + line);
	}
});
