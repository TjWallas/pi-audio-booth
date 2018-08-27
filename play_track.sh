#!/bin/bash
set -euf -o pipefail

cd /home/pi/asmr

mpg123 --loop -1 -a hw:"$2",0 "$1"
