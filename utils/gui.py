import threading
import json
import tkinter as tk

class App():
	def __init__(self, bot, config, features_toggle):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		
	def _start(self):
		self.root = tk.Tk()
		self.root.title("Stalkbot Control Panel")
				
		self.title = tk.Label(self.root, text="Stalkbot Control Panel", font=("Helvetica", 24))
		self.online_status = tk.Label(self.root, text="status", font=("Helvetica", 14))
		self.ping = tk.Label(self.root, text="ping", font=("Helvetica", 14))
		
		self.edit_config_button = tk.Button(self.root, text="Edit config", font=("Helvetica", 18), command=self.edit_config)
		
		self.feature_buttons = list()
		
		i = 0
		for button in self.features_toggle:
			self.feature_buttons.append(tk.Button(self.root, text="Toggle " + button + " (" + str(self.features_toggle[button]) + ")", command=lambda x=button, y=i: self.toggle(x, y)))
			i += 1
		
		self.title.pack()
		self.online_status.pack()
		self.ping.pack()
		self.edit_config_button.pack()
		for button in self.feature_buttons:
			button.pack()

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

	def toggle(self, feature, button_id):
		self.features_toggle[feature] = not self.features_toggle[feature]
		self.feature_buttons[button_id].config(text="Toggle " + feature + " (" + str(self.features_toggle[feature]) + ")")
		
		json.dump(self.features_toggle, open("features_toggle.json", "w"))

	def edit_config(self):
		root = tk.Tk()
		root.title("Stalkbot Config Editor")
		
		labels = list()
		values = list()

		i = 1
		for x in self.config:
			labels.append(tk.Label(root, text=x, font=("Helvetica", 14)))
			values.append(tk.Entry(root, font=("Helvetica", 14)))
			values[-1].insert(0, self.config[x])

			if x == "token":
				values[-1].config(show="*")
			
			labels[-1].grid(column=0, row=i)
			values[-1].grid(column=1, row=i)
			
			i += 1
		
		tk.Button(root, text="Save", font=("Helvetica", 18), command=root.quit).grid(column=0, row=i)

		root.mainloop()
		i = 0
		for x in self.config:
			convert = type(self.config[x])
			self.config[x] = convert(values[i].get())
			i += 1

		json.dump(self.config, open("config.json", "w"))

		root.destroy()
		