import discord
import discord.ext.commands as commands
import pygame.camera
import pygame.image
import asyncio
import os

class Webcam(commands.Cog):
	def __init__(self, bot, functions):
		self.bot = bot
		self.functions = functions

	@commands.command(aliases=["wc"])
	async def webcam(self, ctx):
		lock = self.bot.locks.add("webcam")

		if lock is False:
			await ctx.send("The webcam command is already being used!")
			return

		if self.bot.timeouts.is_timeout("webcam"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.bot.timeouts.add("webcam", self.bot.config["timeout"])
		
		try:
			self.functions.warning_sound()
			
			pygame.camera.init()
			cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (self.bot.config["cam_width"], self.bot.config["cam_height"]))
			cam.start()

			await ctx.message.add_reaction(self.bot.emoji.timer)
			await asyncio.sleep(self.bot.config["webcam_delay"])
			await ctx.message.remove_reaction(self.bot.emoji.timer, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.repeat_button)

			img = cam.get_image()
			pygame.image.save(img, "cache/webcam.png")
			cam.stop()
			
			await ctx.send(content="", file=discord.File("cache/webcam.png"))
			os.unlink("cache/webcam.png")
			
			await ctx.message.remove_reaction(self.bot.emoji.repeat_button, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
			
		except Exception as exc:
			ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
		finally:
			self.bot.locks.release("webcam")
		
