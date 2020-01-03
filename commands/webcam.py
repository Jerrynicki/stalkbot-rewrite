import discord
import discord.ext.commands as commands
import pygame.camera
import pygame.image
import asyncio
import os

class Webcam(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts

	@commands.command(aliases=["wc", ":toilet:"])
	async def webcam(self, ctx):
		if self.timeouts.is_timeout("webcam"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("webcam", self.config["timeout"])
		
		if not self.features_toggle["webcam"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return
		
		try:
			self.functions.notification(self.config["notifications_format"], "Webcam", ctx)
			await self.functions.warning_sound()
			
			pygame.camera.init()
			cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (self.config["cam_width"], self.config["cam_height"]))
			cam.start()
			img = cam.get_image()

			await ctx.message.add_reaction(self.bot.emoji.timer)
			await asyncio.sleep(self.config["webcam_delay"])
			await ctx.message.remove_reaction(self.bot.emoji.timer, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.outbox_tray)

			img = cam.get_image()
			pygame.image.save(img, "cache/webcam.png")
			cam.stop()
			
			await ctx.send(content="", file=discord.File("cache/webcam.png"))
			os.unlink("cache/webcam.png")
			
			await ctx.message.remove_reaction(self.bot.emoji.outbox_tray, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
			
		except Exception as exc:
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
