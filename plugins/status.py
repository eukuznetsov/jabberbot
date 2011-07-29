NAME = "StatusBot"

def name():
	return NAME

def listHandlers():
	return {'message': ['uptime', 'hello']}
	
def uptime(msg):
	print('Fuck you!')

def hello(msg):
	print('Bot say Hello!')
