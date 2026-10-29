#!/bin/bash
# Builds the 45-second promo, the poster and the QR code on a GitHub runner -> out/
set -e
D=tools/promo; mkdir -p out
sudo apt-get -qq update >/dev/null && sudo apt-get -qq install -y ffmpeg >/dev/null
pip install -q qrcode pillow numpy
python3 -c "import qrcode;q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=24,border=2);q.add_data('https://manahakku-team.github.io/manahakku/');q.make(fit=True);q.make_image(fill_color=(23,32,90),back_color='white').save('$D/qr-web.png')"
cp $D/qr-web.png out/ManaHakku-QR.png
mkdir -p /tmp/pw && (cd /tmp/pw && npm init -y >/dev/null && npm i playwright@1.48.2 >/dev/null 2>&1 && npx playwright install --with-deps chromium >/dev/null 2>&1)
export NODE_PATH=/tmp/pw/node_modules
node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});await p.goto('file://'+require('path').resolve('$D/poster.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);await p.screenshot({path:'out/ManaHakku-poster.png'});await b.close()})()"
python3 $D/music.py out/music.wav 45
node $D/render45.js $D out/still 30 2.5,13,19,25,30.5,43
node $D/render45.js $D out/silent.mp4 30
ffmpeg -y -loglevel error -i out/silent.mp4 -i out/music.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out/ManaHakku-promo-45s.mp4
rm -f out/silent.mp4 out/music.wav; ls -la out
