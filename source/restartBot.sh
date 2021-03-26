#!/bin/sh

killall python
. /root/venv/bin/activate
pip install --upgrade -r requirements.txt
nohup python "$(dirname "$0")/main.py" 1> bot.out 2> bot.err &
