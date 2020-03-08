import discord
import discord.ext.commands as commands
import asyncio
import os
import subprocess
import time

from PIL import Image, ImageFilter

class Screenshot(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts, command_log):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts
		self.command_log = command_log
		if self.bot.windows:
			import tkinter as tk
			window = tk.Tk()
			self.screensize = (window.winfo_screenwidth(), window.winfo_screenheight())
			window.destroy()
		
	@commands.command(aliases=["ss"])
	async def screenshot(self, ctx):
		if self.timeouts.is_timeout("screenshot"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("screenshot", self.config["timeout"])
			
		if not self.features_toggle["screenshot"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return
		
		try:
			self.functions.notification(self.config["notifications_format"], "Screenshot", ctx)
			await self.functions.warning_sound()
			self.command_log.append((time.time(), ctx, "Screenshot"))
			await ctx.message.add_reaction(self.bot.emoji.outbox_tray)

			if not self.bot.windows:
				scrot = subprocess.run(["scrot", "cache/screenshot.png", "--overwrite"], check=True, timeout=5)
				img = Image.open("cache/screenshot.png")
			else:
				from PIL import ImageGrab
				img = ImageGrab.grab(bbox=[0, 0, self.screensize[0], self.screensize[1]])
	
			img = img.filter(ImageFilter.GaussianBlur(self.config["screenshot_blur"]))
			img.save("cache/screenshot_blurred.png")
			
			await ctx.send(content="", file=discord.File("cache/screenshot_blurred.png"))
			if os.path.isfile("cache/screenshot.png"):
				os.unlink("cache/screenshot.png")
			os.unlink("cache/screenshot_blurred.png")
			
			await ctx.message.remove_reaction(self.bot.emoji.outbox_tray, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
		except Exception as exc:
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
