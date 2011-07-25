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
		self.addHandlers()
		self.client.online = 0
	
	def online(self): 
		if self.client.connect():
			self.log.info("Connect to server")
		else:
			self.log.critical("Unable to connect to server %s", self.client.getjidresourse())
		self.client.sendPresence()
		self.client.process(threaded="false")
		self.client.online = 1
	
	def offline(self): 
		self.client.disconnect()
		self.log.info("Disconnect from server")
		self.client.online = 0
		
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
		self.log.debug("Login: ",self.config['jid'])
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
		self.client.add_event_handler('message', self.processMessage)
		
	def processMessage(self, msg):
		print(msg['from'])
