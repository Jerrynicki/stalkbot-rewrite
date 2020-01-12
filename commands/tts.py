import discord
import discord.ext.commands as commands
import os
import time

from gtts import gTTS

class TTS(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts, command_log):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts
		self.command_log = command_log

	@commands.command(aliases=["say"])
	async def tts(self, ctx, *text):
		if self.timeouts.is_timeout("tts"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("tts", self.config["timeout"])
		
		if not self.features_toggle["tts"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return
		
		try:
			text = " ".join(text)

			self.functions.notification(self.config["notifications_format"], "TTS", ctx)
			await self.functions.warning_sound()
			self.command_log.append((time.time(), ctx, "TTS: " + text))
			await ctx.message.add_reaction(self.bot.emoji.play)

			# subprocess.run(["espeak", "-v", self.config["tts_voice"], ctx.message.author.name + " sagt " + text], \
			#                check=True, timeout=self.config["max_message_length"])
			
			tts = gTTS(ctx.message.author.name + ": " + text, lang=self.config["tts_voice"])
			tts.save("cache/tts.mp3")
			self.functions.ffmpeg("cache/tts.mp3", ["-ar", "44100", "-ac", "2", "-t", str(self.config["max_message_length"])], "cache/tts.wav")
			await self.functions.play_sound("cache/tts.wav")

			os.unlink("cache/tts.mp3")
			os.unlink("cache/tts.wav")

			await ctx.message.remove_reaction(self.bot.emoji.play, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
		except Exception as exc:
			if type(exc) == subprocess.TimeoutExpired:
				await ctx.message.remove_reaction(self.bot.emoji.play, ctx.message.guild.me)
				await ctx.message.add_reaction(self.bot.emoji.stop_sign)
				return

			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
