#!/usr/bin/python
# -*- coding: utf-8 -*-
import xmpp, sys,os
import logging

LOG_LEVEL = logging.DEBUG

class MyLogger(logging.Logger):
	def __init__(self, name):
		#logging settings
		logging.Logger.__init__(self, name)
		self.setLevel(LOG_LEVEL)
		#create handler
		sh = logging.StreamHandler()
		sh.setLevel(logging.DEBUG)
		#set handler for logger
		self.addHandler(sh)
		

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.log = MyLogger("config log")
	params = {}
	if os.path.isfile('config.ini'):
		config.read('config.ini')
	else:
		config.log.critical('Config file not found')
	try:
		params['login'] = config.get('connect', 'login')
	except ConfigParser.NoOptionError:
		config.log.error("Not defined login")
		sys.exit()
	try:
		params['password'] = config.get('connect', 'password')
	except ConfigParser.NoOptionError:
		config.log.error("Not defined password")
		sys.exit()
	try:
		admins = config.get('connect', 'admins').split(',')
	except ConfigParser.NoOptionError:
		config.log.warn()
	else:
		params['admins']=admins
	try:
		readOnlyUsers = config.get('connect','readonly').split(',')
	except ConfigParser.NoOptionError:
		print "Debug: not defined ReadOnly-users"
	else:
		params['readOnlyUsers']=readOnlyUsers
	return  params

#class JabberBot(xmpp.Client):
	##init
	#def __init__(self, login, password):
		#self.login = login
		#self.password = password
		#self.online = 0
	

