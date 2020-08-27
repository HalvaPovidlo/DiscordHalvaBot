#!/bin/sh

killall -u u0905056 python
. ~/tmp/discordEnv/bin/activate
nohup python "$(dirname "$0")/bot_main.py" > bot_main.out 2> bot_main.err &
nohup python "$(dirname "$0")/client_main.py" > client_main.out 2> client_main.err &
