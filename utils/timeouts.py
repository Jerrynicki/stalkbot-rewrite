import time

class Timeouts():
	def __init__(self):
		self.timeouts = dict()

	def add(self, command, length):
		ctime = time.time()
		if command not in self.timeouts or ctime > self.timeouts[command]:
			self.timeouts[command] = ctime + length

	def is_timeout(self, command):
		if command in self.timeouts:
			if time.time() > self.timeouts[command]:
				return False
			else:
				return True

		return False
