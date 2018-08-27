#!/bin/bash
set -euf -o pipefail

cd /home/pi/asmr

mpg123 --random -a hw:1,0 gal-gadot.opus.mp3 grilling.m4a.mp3 noodles.ogg.mp3 &
mpg123 --loop -1 -a hw:2,0 compilation.opus.mp3 &
mpg123 --loop -1 -a hw:3,0 sleep.opus.mp3 &
