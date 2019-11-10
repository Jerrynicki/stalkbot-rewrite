import time

class Timeouts():
    def __init__(self):
        self.timeouts = dict()

    def add(self, command, length):
        if command not in self.timeouts:
            self.timeouts[command] = time.time() + length

    def is_timeout(self, command):
        if command in self.timeouts:
            if time.time() > self.timeouts[command]:
                return False
            else:
                return True

        return False
