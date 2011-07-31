#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect

def  listHandlers():
	return {'message': [parseCommand]}
	
def parseCommand(self, msg):
	self.log.debug('Parsing command.')
	result = ""
	if msg['from'] in self.config['admins']:
		result += sendCommand(self, msg['body'])
	else:
		result += "Access denied\n"
	self.sendMessage(msg['from'], result)
	
def sendCommand(self, command):
	result = ""
	if "__" not in command:
		for name in self.plugins:
			if command in dir(self.plugins[name]):
				to_exec = getattr(self.plugins[name], command)
				if inspect.isfunction(to_exec):
					 result += to_exec()				 
	else:
		result += "Dont use command with '__'"
		self.log.warning("Dont use command with '__'")
	try: 
		to_exec
	except NameError:
		result += "Unknown command \n"
	return result
