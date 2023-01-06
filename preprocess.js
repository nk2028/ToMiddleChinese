// @ts-check

import { access, constants, createReadStream, createWriteStream, unlink } from "fs";
import { createInterface } from "readline";
import { get } from "https";
import { pipeline } from "stream/promises";

import { 音韻地位 } from "qieyun";
import { kyonh, unt, tupa } from "qieyun-examples";

// File Downloading

/**
 * @param {string} url
 * @param {string} path
 * @returns {Promise<void>}
 */
function download(url, path) {
  return new Promise((resolve, reject) => {
    access(path, constants.F_OK, error => {
      if (error) {
        console.log(`downloading ${path}`);
        get(url, response => {
          if (response.statusCode === 200) {
            response.pipe(
              createWriteStream(path)
                .on("finish", resolve)
                .on("error", error => unlink(path, () => reject(error)))
            );
          } else {
            reject(new Error(`Server responded with ${response.statusCode}: ${response.statusMessage}`));
          }
        }).on("error", reject);
      } else {
        console.log(`${path} already exists, skip downloading`);
        resolve();
      }
    });
  });
};

// Sorting

/**
 * Compare two strings by (full) Unicode code point order.
 * @param {string} x
 * @param {string} y
 * @returns {number}
 */
function compareFullUnicode(x, y) {
  const ix = x[Symbol.iterator]();
  const iy = y[Symbol.iterator]();
  for (;;) {
    const nx = ix.next();
    const ny = iy.next();
    if (nx.done && ny.done) {
      return 0;
    }
    const cx = nx.done ? -1 : nx.value.codePointAt(0);
    const cy = ny.done ? -1 : ny.value.codePointAt(0);
    const diff = cx - cy;
    if (diff) {
      return diff;
    }
  }
}

/**
 * @param {string[]} x
 * @param {string[]} y
 * @returns {number}
 */
function compareRow(x, y) {
  const diffWordLen = [...x[0]].length - [...y[0]].length;
  if (diffWordLen) {
    return diffWordLen;
  }
  const l = Math.min(x.length, y.length);
  for (let i = 0; i < l; i++) {
    const diff = compareFullUnicode(x[i], y[i]);
    if (diff) {
      return diff;
    }
  }
  return x.length - y.length;
}

/**
 * @param {string[][]} rows
 * @returns {IterableIterator<string>}
 */
function* uniqSortedLines(rows) {
  let lastLine;
  for (let row of rows.slice().sort(compareRow)) {
    const line = row.join("\t") + "\n";
    if (line !== lastLine) {
      yield line;
    }
    lastLine = line;
  }
}

// Converter utils

/**
 * @param {(地位: 音韻地位) => string} derive
 * @param {{ [x: string]: string }} special地位
 * @returns {(描述: string) => string}
 */
function makeConverter(derive, special地位) {
  const cache = new Map();
  return x => {
    if (x.startsWith("!")) {
      const sub = special地位[x.slice(1)];
      if (!sub) {
        throw new Error(`unhandled special 地位: ${x}`);
      } else if (sub.startsWith(">")) {
        return sub.slice(1);
      } else if (sub.startsWith("=")) {
        x = sub.slice(1);
      } else {
        throw new Error(`invalid instruction for special 地位 ${x}: ${sub}`);
      }
    }
    if (cache.has(x)) {
      return cache.get(x);
    }
    const res = derive(音韻地位.from描述(x));
    cache.set(x, res);
    return res;
  };
}

// File reading

/**
 * @param {string} path
 * @param {(描述: string) => string} conv
 * @returns {AsyncIterableIterator<string[]>}
 */
async function* loadTsv(path, conv) {
  for await (const line of createInterface({
    input: createReadStream(path),
    crlfDelay: Infinity,
  })) {
    const [word, input] = line.split("\t");
    const codes = input.split(" ").map(conv).join(" ");
    yield [word, codes];
  }
}

/**
 * @param {string[][]} dict
 * @param {string} path
 * @param {(描述: string) => string} conv
 */
async function extendFromTsv(dict, path, conv) {
  for await (const row of loadTsv(path, conv)) {
    dict.push(row);
  }
}

// Main

const sourceFiles = ["chars.tsv", "words.tsv", "extra_words.tsv"];

/**
 * @param {string} name
 * @param {(描述: string) => string} conv
 */
async function generate(name, conv) {
  const dict = [];
  for (const path of sourceFiles) {
    console.log(`${name}:\treading ${path}`);
    await extendFromTsv(dict, path, conv);
  }
  console.log(`${name}:\twriting dict`);
  await pipeline(
    uniqSortedLines(dict),
    createWriteStream(`src/ToMiddleChinese/dict/${name}.dict.yaml`)
  );
}

const deriveTupa = tupa.schema({ 模式: "寬鬆" });

/** @type {[string, (描述: string) => string][]} */
const schemas = [
  ["tupa", makeConverter(deriveTupa, { 精一侵上: ">tsoimq" })],
  ["kyonh", makeConverter(kyonh, { 精一侵上: "=莊侵上" })],
  ["unt", makeConverter(unt, { 精一侵上: "=精三侵上" })],
];

download("https://raw.githubusercontent.com/fxsjy/jieba/237dc66/extra_dict/dict.txt.big", "src/ToMiddleChinese/dict/dict.big.txt")
download("https://cdn.jsdelivr.net/npm/opencc-data@1.0.8/data/HKVariantsRev.txt", "src/ToMiddleChinese/dict/HKVariantsRev.txt")
download("https://cdn.jsdelivr.net/npm/opencc-data@1.0.8/data/HKVariantsRevPhrases.txt", "src/ToMiddleChinese/dict/HKVariantsRevPhrases.txt")

Promise
  .all(sourceFiles.map(path => download(`https://raw.githubusercontent.com/nk2028/rime-dict-source/df307c8/${path}`, path)))
  .then(() => schemas.map(args => generate(...args)));
