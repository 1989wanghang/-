#!/bin/bash

adb pull /data/local/temp/
mv temp/* .

#adb pull /sys/kernel/debug/tracing/trace

