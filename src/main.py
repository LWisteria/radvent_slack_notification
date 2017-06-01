#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import urllib2
import datetime
from HTMLParser import HTMLParser
from slacker import Slacker

class RadventParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)

		self.tag_td = False
		self.tag_date = False
		self.date = 0
		self.today = datetime.date.today().day
		self.tag_author = False
		self.author = ""
		self.tag_entry = False
		self.link = ""
		self.tag_title = False
		self.title = ""
		self.complete = False

	def handle_starttag(self, tag, attrs):
		if not self.complete:
			if tag == "td":
				self.tag_td = True

			if self.tag_td and tag == "p":
				for a in attrs:
					if a[0] == "class":
						for c in a[1].split(" "):
							if c == "advent-calendar-date":
								self.tag_date = True
							elif c == "advent-calendar-author" and self.date == self.today:
								self.tag_author = True
							elif c == "advent-calendar-entry" and self.date == self.today:
								self.tag_entry = True

			if self.tag_entry and tag == "a":
				for a in attrs:
					if a[0] == "href":
						self.link = a[1]
				self.tag_title = True

	def handle_data(self, data):
		if not self.complete:
			data = data.decode("utf-8")
			if self.tag_date:
				self.date = int(data)
			elif self.tag_author:
				self.author = data.strip()[:-2]
			elif self.tag_title:
				self.title = data.strip()

	def handle_endtag(self, tag):
		if not self.complete:
			if self.date != 0 and self.author != "" and self.link != "" and self.title != "":
				self.complete = True

			if tag == "td":
				self.tag_td = False
				self.date = 0
				self.author = ""
				self.link = ""
				self.title = ""

			if tag == "p":
				self.tag_date = False
				self.tag_author = False
				self.tag_entry = False

			if tag == "a":
				self.tag_title = False

class Slack(object):
	def __init__(self, token):
		self.__slacker = Slacker(token)

	def post_message(self, date, author, link, title, site_title=u"アドベントカレンダー", icon=None, channel="#general"):
		username = "AdventCalender Notification"
		message = u"{4}、{0}日目の記事\n『{1}』({2})\n{3}\nが公開されました！\n\nお時間ある時にぜひご覧ください！".format(date, title, author, link, site_title)

		self.__slacker.chat.post_message(channel, message, username, None, None, None, None, None, None, icon)

def main():
	url = sys.argv[1]
	token = sys.argv[2]
	site_title = sys.argv[3].decode("utf-8")
	icon = sys.argv[4]
	channel = sys.argv[5]

	# download
	response = urllib2.urlopen(url)
	html = response.read()
	response.close()

	# parse
	parser = RadventParser()
	parser.feed(html)
	parser.close()
	if parser.complete:
		# post
		slack = Slack(token)
		slack.post_message(parser.date, parser.author, url[:-1] + parser.link, parser.title, site_title, icon, channel)

if __name__ == "__main__":
	main()
