#!/usr/bin/python
import xmpp, sys,os

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	params = {}
	if os.path.isfile('config.ini'):
		config.read('config.ini')
	else:
		sys.exit('Error: Config file not found')
	try:
		params['login'] = config.get('connect', 'login')
	except ConfigParser.NoOptionError:
		sys.exit("Eror: not defined login")
	try:
		params['password'] = config.get('connect', 'password')
	except ConfigParser.NoOptionError:
		sys.exit("Eror: not defined password")
	try:
		admins = config.get('connect', 'admins').split(',')
	except ConfigParser.NoOptionError:
		print "Warning: not defined admin account"
	else:
		params['admins']=admins
	try:
		readOnlyUsers = config.get('connect','readonly').split(',')
	except ConfigParser.NoOptionError:
		print "Debug: not defined ReadOnly-users"
	else:
		params['readOnlyUsers']=readOnlyUsers
	return  params

def message():
	pass 

config = loadConfig()
print config['login']
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
