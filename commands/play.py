import discord
import discord.ext.commands as commands
import asyncio
import os

class Play(commands.Cog):
	def __init__(self, bot, functions, timeouts):
		self.bot = bot
		self.functions = functions
		self.timeouts = timeouts

	@commands.command()
	async def play(self, ctx):
		if self.timeouts.is_timeout("play"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("play", self.bot.config["timeout"])
		
		try:
			await self.functions.warning_sound()
			await ctx.message.add_reaction(self.bot.emoji.inbox_tray)
			
			filename = "cache/play." + ctx.message.attachments[0].filename.split(".")[-1]
			await ctx.message.attachments[0].save(filename)
			
			if filename.split(".")[-1] != "wav":
				result = self.functions.ffmpeg(self.bot.config["ffmpeg_location"], filename, ["-af", "volume=-25dB", "-t", \
											   str(self.bot.config["max_message_length"]), "-ar", "44100", "-ac", "2"], filename + ".wav")
			else:
				filename = ".".join(filename.split(".")[:-1])
				result = True

			if result is False:
				raise Exception("FFmpeg command timed out or returned an error")
			
			await ctx.message.remove_reaction(self.bot.emoji.inbox_tray, ctx.message.guild.me)
			
			await ctx.message.add_reaction(self.bot.emoji.play)
			
			await self.functions.play_sound(filename + ".wav")
			await ctx.message.remove_reaction(self.bot.emoji.play, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
			
			os.unlink(filename)
			os.unlink(filename + ".wav")
			
		except Exception as exc:
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
