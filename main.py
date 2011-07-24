#!/usr/bin/python
# -*- coding: utf-8 -*-
import bot, time

def main():
	jbot = bot.JabberBot()
	jbot.online()
	while 1:
		time.sleep(1)
	#jbot.offline()
	
if __name__ == "__main__":
	main()
	
#bot.RegisterHandler('message', message())
#bot.online = 1
#while bot.online:
	#bot.Process(1)
#bot.disconnect()
