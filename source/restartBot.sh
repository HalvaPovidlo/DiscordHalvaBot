#!/bin/bash

killall python

DIRNAME=$(dirname "$0")

. "$DIRNAME"/venv/bin/activate
pip install --upgrade -r requirements.txt
nohup python "$DIRNAME/main.py" 1> bot.out 2> bot.err &
