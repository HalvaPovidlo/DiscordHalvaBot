#!/bin/sh

killall -u u0905056 python
. ~/tmp/discordEnv/bin/activate
nohup python "$(dirname "$0")/main.py" > bot.out 2> bot.err &
