import threading
import tkinter as tk

class App():
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		
	def _start(self):
		self.root = tk.Tk()
		self.root.title("Stalkbot Control Panel")
				
		self.title = tk.Label(self.root, text="Stalkbot Control Panel", font=("Helvetica", 24))
		self.online_status = tk.Label(self.root, text="status", font=("Helvetica", 14))
		self.ping = tk.Label(self.root, text="ping", font=("Helvetica", 14))
		
		self.edit_config_button = tk.Button(self.root, text="Edit config", font=("Helvetica", 18), command=self.edit_config)
		
		self.title.pack()
		self.online_status.pack()
		self.ping.pack()
		self.edit_config_button.pack()

		self.root.after(1, self.update_stats)

		self.root.mainloop()

	def start(self):
		self.thread = threading.Thread(target=self._start)
		self.thread.start()

	def update_stats(self):
		if not self.bot.is_closed() and self.bot.is_ready():
			self.online_status.config(fg="#00FF00", text="Online")
		else:
			self.online_status.config(fg="#FF0000", text="Offline")
		self.ping.config(text="Ping: " + str(round(self.bot.latency*1000, 1)) + " ms")
		self.root.after(2000, self.update_stats)

	def edit_config(self):
		pass
