import discord
import discord.ext.commands as commands
import asyncio
import os
import time
import requests

class Play(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts, command_log):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts
		self.command_log = command_log

	@commands.command()
	async def play(self, ctx, *args):
		if self.timeouts.is_timeout("play"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("play", self.config["timeout"])
		
		if not self.features_toggle["play"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return
		
		try:
			url = None
			args = " ".join(args)

			if args.startswith("http"):
				url = args
			if len(ctx.message.attachments) == 0 and url == None:
				await ctx.send("Did you forget to attach a file, " + ctx.message.author.mention + "?")
				return
			
			self.functions.notification(self.config["notifications_format"], "Play file", ctx)
			await self.functions.warning_sound()
			
			if url == None:
				self.command_log.append((time.time(), ctx, "Play: " + ctx.message.attachments[0].filename))
			else:
				self.command_log.append((time.time(), ctx, "Play: " + args.split("/")[-1]))
			await ctx.message.add_reaction(self.bot.emoji.inbox_tray)

			if url == None:
				filename = "cache/play." + ctx.message.attachments[0].filename.split(".")[-1]
				await ctx.message.attachments[0].save(filename)
			else:
				filename = "cache/play." + url.split("/")[-1].split(".")[-1]

				r = requests.get(url, stream=True)
				if int(r.headers["Content-Length"]) > 50*1024*1024:
					await ctx.send("Files larger than 50 MiB are not allowed.")
					return
				
				filesize = 0 # Count filesize manually in case the server is returning a wrong value for content-length
				file = open(filename, "wb")
				for chunk in r.iter_content(chunk_size=2048):
					file.write(chunk)
					filesize += len(chunk)
					if filesize > 50*1024*1024:
						file.close()
						os.unlink(filename)
						await ctx.send("Files larger than 50 MiB are not allowed.")
						return
				file.close()
			
			if filename.split(".")[-1] != "wav":
				result = self.functions.ffmpeg(filename, ["-af", "volume=-25dB,loudnorm=tp=0", "-t", \
											   str(self.config["max_message_length"]), "-ar", "44100", "-ac", "2"], filename + "_converted.wav")
			else:
				filename = ".".join(filename.split(".")[:-1])
				result = True

			if result is False:
				raise Exception("FFmpeg command timed out or returned an error")
			
			await ctx.message.remove_reaction(self.bot.emoji.inbox_tray, ctx.message.guild.me)
			
			await ctx.message.add_reaction(self.bot.emoji.play)
			
			await self.functions.play_sound(filename + "_converted.wav")
			await ctx.message.remove_reaction(self.bot.emoji.play, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
			
			os.unlink(filename)
			os.unlink(filename + "_converted.wav")
			
		except Exception as exc:
			raise exc
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
