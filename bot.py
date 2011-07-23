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

class JabberBot(xmpp.Client):
	def __init__(self):
		self.log = MyLogger('main logger')
		self.readConfig()
		#hack for inherit base class Client
		self.Namespace,self.DBG='jabber:client', 'client'
		xmpp.client.CommonClient.__init__(self, self.config['login'].getDomain(), debug=[])
		self.online = 0
	
	def setOnline(self): 
		self.online = 1
		self.log.info("Set status ONLINE")
	
	def setOffline(self): 
		self.online = 0
		self.log.info("Set status OFLINE")
		
	def readConfig(self):
		import ConfigParser
		config = ConfigParser.ConfigParser()
		self.config = {}
		if os.path.isfile('config.ini'):
			config.read('config.ini')
		else:
			self.log.critical('Config file not found')
		try:
			self.config['login'] = xmpp.JID(config.get('connect', 'login'))
		except ConfigParser.NoOptionError:
			self.log.critical("Not defined login")
		try:
			self.config['password'] = config.get('connect', 'password')
		except ConfigParser.NoOptionError:
			self.log.critical("Not defined password")
		try:
			admins = config.get('connect', 'admins').split(',')
		except ConfigParser.NoOptionError:
			self.log.warn()
		else:
			self.config['admins']=admins
		try:
			readOnlyUsers = config.get('connect','readonly').split(',')
		except ConfigParser.NoOptionError:
			print "Debug: not defined ReadOnly-users"
		else:			
			self.config['readOnlyUsers']=readOnlyUsers
