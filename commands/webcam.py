import discord
import discord.ext.commands as commands
import pygame.camera
import pygame.image
import asyncio
import os

class Webcam(commands.Cog):
	def __init__(self, bot, functions, timeouts):
		self.bot = bot
		self.functions = functions
		self.timeouts = timeouts

	@commands.command(aliases=["wc"])
	async def webcam(self, ctx):
		if self.timeouts.is_timeout("webcam"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("webcam", self.bot.config["timeout"])
		
		try:
			self.functions.notification(self.bot.config["notifications_format"], "Webcam", ctx)
			await self.functions.warning_sound()
			
			pygame.camera.init()
			cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (self.bot.config["cam_width"], self.bot.config["cam_height"]))
			cam.start()

			await ctx.message.add_reaction(self.bot.emoji.timer)
			await asyncio.sleep(self.bot.config["webcam_delay"])
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
