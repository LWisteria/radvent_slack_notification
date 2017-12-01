#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from slacker import Slacker
import json

def main():
	token = sys.argv[1]
	channel = sys.argv[2]
	text = sys.argv[3]

	# deleate previous message
	slacker = Slacker(token)
	id = [c for c in json.loads(str(slacker.channels.list()))["channels"] if c["name"] == channel.replace('#', '')][0]["id"]
	for mes in json.loads(str(slacker.channels.history(id)))["messages"]:
		if text in mes["text"]:
			slacker.chat.delete(id, mes["ts"])
			print(mes["text"])

if __name__ == "__main__":
	main()
