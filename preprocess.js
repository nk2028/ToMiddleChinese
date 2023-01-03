// @ts-check

import { createReadStream, createWriteStream } from 'fs';
import { 資料, 音韻地位 } from 'qieyun';
import { kyonh, unt, tupa } from 'qieyun-examples';
import { createInterface } from 'readline';

/** @type {{ [s: string]: 音韻地位 }} */
const d = {};

for (const 地位 of 資料.iter音韻地位()) {
	d[kyonh(地位)] = 地位;
}

/** @type {(s: string) => 音韻地位 | undefined} */
function kyonh2音韻地位(s) {
	let res = d[s];
	if (res)
		return res;
	switch (s.slice(-1)) {
		case 'p':
		case 't':
		case 'k':
			break;
		case 'x':
			res = d[s = s.slice(0, -1)] || d[s + 'h'];
			if (res)
				return res.調整({ 聲: '上' });
			break;
		case 'h':
			res = d[s = s.slice(0, -1)] || d[s + 'x'];
			if (res)
				return res.調整({ 聲: '去' });
		default:
			res = d[s + 'x'] || d[s + 'h'];
			if (res)
				return res.調整({ 聲: '平' });
	}
}

const logger_qimyonhmieuzsjyt = createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.qimyonhmieuzsjyt.yaml');
const logger_kyonh = createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.kyonh.yaml');
const logger_unt = createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.unt.yaml');
const logger_tupa = createWriteStream('src/ToMiddleChinese/dict/zyenpheng.dict.tupa.yaml');

const lineReader = createInterface({
	input: createReadStream('zyenpheng.dict.simple.yaml')
});

let count = 0;
lineReader.on('line', line => {
	const [字, 羅馬字] = line.split('\t');
	const [...字們] = 字;
	const 地位們 = 羅馬字.split(' ').map(kyonh2音韻地位);
	if (地位們.every(x => x)) {
		logger_qimyonhmieuzsjyt.write(`${字}\t${羅馬字}\n`);
		logger_kyonh.write(轉換(kyonh));
		logger_unt.write(轉換(unt));
		logger_tupa.write(轉換(tupa));
	} else {
		console.error('Unhandled: ' + line);
		count++;
	}
	/** @type {(方案: typeof tupa) => string} */
	function 轉換(方案) {
		return `${字}\t${地位們.map((地位, i) => 地位 && 方案(地位, 字們[i])).join(' ')}\n`;
	}
});
lineReader.on('close', () => {
	if (count) {
		console.log('Unhandled count: ' + count);
		process.exit(1);
	}
});
