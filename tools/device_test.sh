#!/bin/bash
# Installs the APK on the emulator, opens it and takes screenshots: first screen, a tab, after Back, and keyboard open.
mkdir -p out; set -x
adb install -r app.apk > out/install.txt 2>&1
adb shell dumpsys package org.manahakku.app | grep -E 'targetSdk|versionName|versionCode' > out/package.txt
adb shell am start -n org.manahakku.app/.MainActivity; sleep 12
adb exec-out screencap -p > out/1_home.png
adb shell wm size > out/size.txt
read W H < <(sed -E 's/.*: ([0-9]+)x([0-9]+).*/\1 \2/' out/size.txt | tail -1)
adb shell input tap $((W/2)) $((H*45/100)); sleep 6
adb exec-out screencap -p > out/2_after_tap.png
adb shell input swipe $((W/2)) $((H*80/100)) $((W/2)) $((H*30/100)) 300; sleep 2
adb exec-out screencap -p > out/3_scrolled.png
adb shell input keyevent KEYCODE_BACK; sleep 3
adb exec-out screencap -p > out/4_after_back.png
adb shell dumpsys activity activities | grep -E 'mResumedActivity|topResumedActivity' > out/after_back.txt
adb shell input keyevent KEYCODE_BACK; sleep 3
adb shell dumpsys activity activities | grep -E 'mResumedActivity|topResumedActivity' > out/after_back2.txt
adb exec-out screencap -p > out/5_after_back2.png
adb logcat -d | grep -iE 'manahakku|chromium|AndroidRuntime|FATAL' | tail -150 > out/logcat.txt
true
