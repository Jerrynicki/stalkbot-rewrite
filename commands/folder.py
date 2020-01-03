import discord
import discord.ext.commands as commands
import asyncio
import os
import random

class Folder(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts

	@commands.command()
	async def folder(self, ctx):
		if "folder" not in self.config or self.config["folder"] == "":
			await ctx.send("The bot owner has not set a folder for this command")
			return
		
		files = os.listdir(self.config["folder"])
		found_file = False
		while not found_file:
			file = random.choice(files)
			if self.config["folder"].endswith("/"):
				full_path = self.config["folder"] + file
			else:
				full_path = self.config["folder"] + "/" + file

			if os.stat(full_path).st_size < 8*1024*1024:
				found_file = True
				await ctx.message.add_reaction(self.bot.emoji.outbox_tray)

				self.functions.notification(self.config["notifications_format"], "Folder: " + file, ctx)
				await self.functions.warning_sound()
				
				
				await ctx.send(content=file, file=discord.File(fp=full_path))
				await ctx.message.remove_reaction(self.bot.emoji.outbox_tray, ctx.message.guild.me)
