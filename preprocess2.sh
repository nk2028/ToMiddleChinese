#!/bin/sh

wget -nc https://cdn.jsdelivr.net/gh/nk2028/qieyun-examples@20200705/kuxyonh.js
sed -i '1s/^/function kuxyonh(音韻地位) { /' kuxyonh.js
echo '} module.exports = kuxyonh;' >> kuxyonh.js

wget -nc https://cdn.jsdelivr.net/gh/nk2028/qieyun-examples@20200705/unt.js
sed -i '1s/^/function unt(音韻地位) { /' unt.js
echo '} module.exports = unt;' >> unt.js
