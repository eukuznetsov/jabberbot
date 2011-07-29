	#!/usr/bin/python
# -*- coding: utf-8 -*-
import sleekxmpp, sys,os
import logging
  
LOG_LEVEL = logging.DEBUG
PRESENCE = 1
PLUGIN_PATH = 'plugins'

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
		self.loadPlugins()
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
		if len(self.plugins):
			self.log.debug('Register handlers:')
			#get dictionary with events and functions name 
			for name in self.plugins:
				handlers = self.plugins[name].listHandlers()
				for event in handlers:
					for func in handlers[event]:
						self.log.debug(name+':'+event+':'+func.__name__)
						#funct = getattr(self.plugins[name], func)
						self.add_event_handler(event, func)

	def loadPlugins(self):
		dirs = PLUGIN_PATH.split(',')
		#files in plugins directory
		files = []
		#modules
		self.plugins = {}
		#find files in dirs and add dirs in PATH
		for directory in dirs:
			if os.path.isdir(directory):
				sys.path.insert(0, directory)
				dir_obj = os.listdir(directory)
				for i in range(len(dir_obj)):
					if os.path.isfile(os.path.join(directory, dir_obj[i])):
						files.append(dir_obj[i])
				self.log.debug('Directory "'+directory+'" add to path')
			else:
				self.log.warn('Path '+directory+'not found')
		#import plugins
		if len(files):
			self.log.debug('Plugins found: '+','.join(files))
			for i in range(len(files)):
				name = os.path.splitext(files[i])[0]
				self.plugins[name] = __import__(name) 
				sel.log.debug(name)
		else:
			self.log.debug('Plugins not found')
