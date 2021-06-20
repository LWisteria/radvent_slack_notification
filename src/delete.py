#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import slack_sdk
import json
import datetime

def main():
	token = sys.argv[1]
	channel = sys.argv[2]
	text = sys.argv[3]

	client = slack_sdk.WebClient(token=token);

	t = datetime.datetime.now() - datetime.timedelta(weeks=1)
	ret = client.conversations_history(channel=channel, oldest=t.timestamp())

	assert ret["ok"] is True

	# delete last message
	for mes in ret["messages"]:
		if text in mes["text"]:
			client.chat_delete(channel=channel, ts=mes["ts"])
			print(mes["text"])
			break

if __name__ == "__main__":
	main()

