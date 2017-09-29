#!/bin/bash

echo "Checking if bot is online...";

count=`ps -aux | grep bot.py | grep -v grep | wc -l`;

if [[ $count == 0 ]] ; then
	echo "Bot is not running, starting it...";
	export bot_token=(?) && /usr/bin/python /home/freddy/bot/InfoUniBot/bot.py &
else
	echo "Allright, bot is running!";
fi
