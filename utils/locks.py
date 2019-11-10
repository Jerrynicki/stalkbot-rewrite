import time

class Locks():
	def __init__(self, max_duration):
		self.locks = list()
		self.max_duration = max_duration
		
	def add(self, name):
		for lock in self.locks:
			if lock[0] == name:
				if time.time() - lock[1] > self.max_duration:
					return False
		
		self.locks.append([name, int(time.time())])
		return True
		
	def release(self, name):
		for lock in range(len(self.locks)):
			if self.locks[lock][0] == name:
				del self.locks[lock]
				return True
				
		return False
		
	
		
