#!/usr/bin/python
# -*- coding: utf-8 -*-

def  listHandlers():
	return {'message': [parseCommand]}
	
def parseCommand(msg):
	self.log.debug('Parsing command.')
	if msg['from'] in self.config['admins']:

def sendCommand(self, command):
	for name in self.plugins:
		if command in dir( )
