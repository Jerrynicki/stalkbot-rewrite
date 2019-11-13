import discord
import discord.ext.commands as commands

import subprocess

class TTS(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts

	@commands.command(aliases=["say"])
	async def tts(self, ctx, *text):
		if self.timeouts.is_timeout("screenshot"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("screenshot", self.config["timeout"])
		
		if not self.features_toggle["tts"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return
		
		try:
			self.functions.notification(self.config["notifications_format"], "TTS", ctx)
			await self.functions.warning_sound()
			await ctx.message.add_reaction(self.bot.emoji.play)

			text = " ".join(text)
			subprocess.run(["espeak", "-v", self.config["tts_voice"], ctx.message.author.name + " sagt " + text], \
			               check=True, timeout=self.config["max_message_length"])

			await ctx.message.remove_reaction(self.bot.emoji.play, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
		except Exception as exc:
			if type(exc) == subprocess.TimeoutExpired:
				await ctx.message.remove_reaction(self.bot.emoji.play, ctx.message.guild.me)
				await ctx.message.add_reaction(self.bot.emoji.stop_sign)
				return

			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
