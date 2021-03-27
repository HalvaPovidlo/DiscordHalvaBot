#!/bin/bash

killall python

DIRNAME=$(dirname "$0")

. "$DIRNAME"/venv/bin/activate
pip install --upgrade -r "$DIRNAME"/requirements.txt
nohup python "$DIRNAME/main.py" 1> "$DIRNAME"/bot.log 2>$1 &
