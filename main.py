#!/usr/bin/python
# -*- coding: utf-8 -*-
import bot, time

def main():
	jbot = bot.JabberBot()
	jbot.online()
	while jbot.client.online:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			jbot.offline()
	#jbot.offline()
	
if __name__ == "__main__":
	main()
