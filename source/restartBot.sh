#!/bin/sh

killall -u u0905056 python
. ~/tmp/discordEnv/bin/activate
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib discord nltk numpy berserk
nohup python "$(dirname "$0")/main.py" > bot.out 2> bot.err &
