#!/bin/sh

wget -nc https://cdn.jsdelivr.net/gh/nk2028/qieyun-examples@20200809/kyonh.js
sed -i '1s/^/function kyonh(音韻地位) { /' kyonh.js
echo '} module.exports = kyonh;' >> kyonh.js

wget -nc https://cdn.jsdelivr.net/gh/nk2028/qieyun-examples@20200809/unt.js
sed -i '1s/^/function unt(音韻地位) { /' unt.js
echo '} module.exports = unt;' >> unt.js
