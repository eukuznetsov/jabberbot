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

class JabberBot(sleekxmpp.ClientXMPP):
	def __init__(self):
		self.log = MyLogger('main logger')
		self.readConfig()
		sleekxmpp.ClientXMPP.__init__(self, self.config['jid'], self.config['password'])
		self.addHandlers()
		self.status = 0
	
	def online(self): 
		if self.connect():
			self.log.info("Connect to server")
		else:
			self.log.critical("Unable to connect to server %s", self.client.getjidresourse())
		self.sendPresence()
		self.process(threaded="false")
		self.status = 1
	
	def offline(self): 
		self.disconnect()
		self.log.info("Disconnect from server")
		self.status = 0
		
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
		else:
			self.log.debug("Login: " + self.config['jid'])
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
		self.add_event_handler('message', self.processMessage)
		
	def processMessage(self, msg):
		self.log.info('Incomming message from %s', msg['from'])
		if msg['from'] in self.config['admins']:
			self.sendMessage(msg['from'], 'Hello, admin!')
		else:
			self.sendMessage(msg['from'], 'Access forbidden!')
		
