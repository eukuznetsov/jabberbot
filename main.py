#!/usr/bin/python
# -*- coding: utf-8 -*-
import bot

def main():
	jbot = bot.JabberBot()
	
if __name__ == "__main__":
	main()
	


##create bot
#jid = xmpp.JID(config['login'])
#bot = xmpp.Client(jid.getDomain(), debug = [])
#bot.config = config
##connect to server
#bot.connect()
#a = bot.auth(jid.getNode(), bot.config['password'])
##view user info about connecting to server
#if (a==None) :
	#print "Error: can't connect to server"
#if (a=='sasl') :
	#print "Connected!"
##event for inbox messages
#bot.RegisterHandler('message', message())
#bot.online = 1
#while bot.online:
	#bot.Process(1)
#bot.disconnect()
