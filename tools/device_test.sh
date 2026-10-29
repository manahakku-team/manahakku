#!/bin/bash
# Installs the APK on the emulator and checks: start-up time, a tab, Back to Home, Back to close.
mkdir -p out; set -x
adb install -r app.apk > out/install.txt 2>&1
adb shell dumpsys package org.manahakku.app | grep -E 'targetSdk|versionName|versionCode' > out/package.txt
# warm up the WebView once (first start on a fresh emulator installs WebView parts), then measure a normal start
adb shell am start -W -n org.manahakku.app/.MainActivity > out/start_cold.txt; sleep 15
adb shell am force-stop org.manahakku.app; sleep 2
adb shell am start -W -n org.manahakku.app/.MainActivity > out/start.txt
for s in 2 4 6; do sleep 2; adb exec-out screencap -p > out/1_start_${s}s.png; done
adb shell wm size > out/size.txt
read W H < <(sed -E 's/.*: ([0-9]+)x([0-9]+).*/\1 \2/' out/size.txt | tail -1)
adb shell input tap $((W/2)) $((H*92/100)); sleep 4
adb exec-out screencap -p > out/2_tab.png
adb shell input keyevent KEYCODE_BACK; sleep 3
adb exec-out screencap -p > out/3_back1.png
adb shell dumpsys activity activities | grep -E 'topResumedActivity' > out/after_back1.txt
adb shell input keyevent KEYCODE_BACK; sleep 3
adb shell dumpsys activity activities | grep -E 'topResumedActivity' > out/after_back2.txt
adb logcat -d | grep -iE 'manahakku|AndroidRuntime|FATAL|CONSOLE' | tail -120 > out/logcat.txt
true
