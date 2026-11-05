#!/bin/bash
# per scene: background with the caption fading in and out; then join and add the voice
set -e
D=$(dirname "$0"); cd "$D"
for L in ${LANGS:-en te}; do
  rm -f $L/*.mp4 $L/list.txt
  python3 - "$L" <<'P' > $L/jobs.txt
import json,sys;L=sys.argv[1]
for i,x in enumerate(json.load(open(f"{L}/shots.json"))):print(x['f'],x['d'],i)
P
  while read f d i; do
    out=$L/c$(printf %02d $i).mp4; fo=$(python3 -c "print(max(0.2,$d-0.3))")
    ffmpeg -nostdin -v error -y -framerate 30 -i $L/bg.png -framerate 30 -i "$f" -filter_complex "[0]format=yuv420p,loop=-1:1,trim=duration=$d,setpts=N/30/TB[b];[1]format=rgba,loop=-1:1,trim=duration=$d,setpts=N/30/TB,fade=in:st=0:d=0.3:alpha=1,fade=out:st=$fo:d=0.28:alpha=1[t];[b][t]overlay=format=auto,format=yuv420p[v]" -map "[v]" -r 30 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p $out.tmp.mp4 && mv $out.tmp.mp4 $out
    echo "file '$(basename $out)'" >> $L/list.txt
  done < $L/jobs.txt
  (cd $L && ffmpeg -nostdin -v error -y -f concat -safe 0 -i list.txt -c copy video.tmp.mp4 && mv video.tmp.mp4 video.mp4)
  ffmpeg -nostdin -v error -y -i $L/video.mp4 -i $L.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -af "adelay=$(python3 -c "print(int(1000*${LEAD:-0.3}))"):all=1,apad" -t $(python3 -c "import json;print(round(sum(x['d'] for x in json.load(open('$L/shots.json'))),3))") out-$L.tmp.mp4 && mv out-$L.tmp.mp4 "Mana-Hakku-cyclone-appeal-$L.mp4"
done
for L in ${LANGS:-en te}; do ffprobe -v error -show_entries format=duration -of csv=p=0 "Mana-Hakku-cyclone-appeal-$L.mp4"; done
