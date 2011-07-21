#!/usr/bin/python
import xmpp

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	login = config.get('connect', 'login')
	password = config.get('connect', 'password')
	admins = config.get('connect', 'admins').split(',')
	readOnlyUsers = config.get('connect','readonly').split(',')
	return {'login':login, 'password': password, 'admins' : admins, 'readOnlyUsers' : readOnlyUsers}

def message():
	global bot
	print 'Incoming message!'
	bot.send(xmpp.protocol.Message('irockez@jabber.ru', 'Ubuntu for dummies!'))

config = loadConfig()
#create bot
jid = xmpp.JID(config['login'])
bot = xmpp.Client(jid.getDomain(), debug = [])
bot.config = config
#connect to server
bot.connect()
a = bot.auth(jid.getNode(), bot.config['password'])
#view user info about connecting to server
if (a==None) :
	print "Error: can't connect to server"
if (a=='sasl') :
	print "Connected!"
#event for inbox messages
bot.RegisterHandler('message', message())
bot.online = 1
while bot.online:
	bot.Process(1)
bot.disconnect()
