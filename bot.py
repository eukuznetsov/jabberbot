#!/usr/bin/python
# -*- coding: utf-8 -*-
import sleekxmpp, sys,os
import logging

LOG_LEVEL = logging.DEBUG
PRESENCE = 1

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

class JabberBot():
	def __init__(self):
		self.log = MyLogger('main logger')
		self.readConfig()
		self.client = sleekxmpp.ClientXMPP(self.config['jid'], self.config['password'])
	
	def online(self): 
		conn = self.client.connect()
		if conn:
			self.log.info("Connect to server")
		else:
			self.log.critical("Unable to connect to server %s", self.client.getjidresourse())
		print(conn)
		self.client.sendPresence()
		self.client.sendMessage("irockez@jabber.ru", "Hi!")
		self.client.process(threaded="false")
	
	def offline(self): 
		self.disconnected()
		self.log.info("Disconnect from server")
		sys.exit()
		
	def readConfig(self):
		import configparser
		config = configparser.ConfigParser()
		self.config = {}
		if os.path.isfile('config.ini'):
			config.read('config.ini')
		else:
			self.log.critical('Config file not found')
		try:
			self.config['jid'] = config.get('connect', 'jid')
		except configparser.NoOptionError:
			self.log.critical("Not defined login")
			self.log("Login: ",self.client.getjidresourse())
		try:
			self.config['password'] = config.get('connect', 'password')
		except configparser.NoOptionError:
			self.log.critical("Not defined password")
		try:
			admins = config.get('connect', 'admins').split(',')
		except configparser.NoOptionError:
			self.log.warn("Not defined admins")
		else:
			self.config['admins']=admins
		try:
			readOnlyUsers = config.get('connect','readonly').split(',')
		except configparser.NoOptionError:
			self.log.debug("Not defined ReadOnly-users")
		else:			
			self.config['readOnlyUsers']=readOnlyUsers

	def addHandlers(self):
		self._owner = self.client
		self.RegisterHandler('message', self.online)
		#self.RegisterDisconnetHandler(self, )
		pass
