class event:
	def __init__(self, time, func):
		self.time = time
		self.func = func

	def execute(self, ev_list):
		self.func(ev_list)
