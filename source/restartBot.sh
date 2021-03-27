#!/bin/bash

killall python

cd $(dirname "$0")

. venv/bin/activate
pip install --upgrade -r requirements.txt
nohup python main.py 1>bot.log 2>&1 &
