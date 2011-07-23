#!/usr/bin/python
# -*- coding: utf-8 -*-
import xmpp, sys,os
import logging

LOG_LEVEL = logging.DEBUG

def initLogger():
	#logging settings
	logger = logging.getLogger("main")
	logger.setLevel(LOG_LEVEL)
	#create handler
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG)
	#set handler for logger
	logger.addHandler(sh)
	return logger

def loadConfig():
	import ConfigParser
	global logger
	config = ConfigParser.ConfigParser()
	params = {}
	if os.path.isfile('config.ini'):
		config.read('config.ini')
	else:
		logger.critical('Config file not found')
	try:
		params['login'] = config.get('connect', 'login')
	except ConfigParser.NoOptionError:
		logger.error("Not defined login")
		sys.exit()
	try:
		params['password'] = config.get('connect', 'password')
	except ConfigParser.NoOptionError:
		logger.error("Not defined password")
		sys.exit()
	try:
		admins = config.get('connect', 'admins').split(',')
	except ConfigParser.NoOptionError:
		logger.warn()
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
	

