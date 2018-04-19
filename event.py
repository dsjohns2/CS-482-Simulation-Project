class event:
	def __init__(self, name, time, func):
		self.name = name
		self.time = time
		self.func = func

	def execute(self, sys):
		self.func(sys)
