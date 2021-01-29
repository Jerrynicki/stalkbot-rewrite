import discord
import discord.ext.commands as commands
import pygame.camera
import pygame.image
import asyncio
import os
import time

class Webcam(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts, command_log):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts
		self.command_log = command_log

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
			self.command_log.append((time.time(), ctx, "Webcam"))
			
			pygame.camera.init()

			await ctx.message.add_reaction(self.bot.emoji.timer)
			await asyncio.sleep(self.config["webcam_delay"])
			
			await ctx.message.remove_reaction(self.bot.emoji.timer, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.repeat_button)

			cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (self.config["cam_width"], self.config["cam_height"]))
			cam.start()
			img = cam.get_image()
			img = cam.get_image()
			pygame.image.save(img, "cache/webcam.png")
			cam.stop()
			
			await ctx.message.remove_reaction(self.bot.emoji.repeat_button, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.outbox_tray)
			
			await ctx.send(content="", file=discord.File("cache/webcam.png"))
			os.unlink("cache/webcam.png")
			
			await ctx.message.remove_reaction(self.bot.emoji.outbox_tray, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
		except Exception as exc:
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))

	@commands.command(aliases=["wcgif","gif"])
	async def webcamgif(self, ctx, speed=1.0):
		if self.timeouts.is_timeout("webcamgif"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("webcamgif", self.config["timeout"])
		
		if not self.features_toggle["webcamgif"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return
		
		try:
			if speed < 0.25 or speed > 10:
				await ctx.message.add_reaction("🇳")
				await ctx.message.add_reaction("🇴")
				return
			
			self.functions.notification(self.config["notifications_format"], "Webcam GIF", ctx)
			await self.functions.warning_sound()
			self.command_log.append((time.time(), ctx, "Webcam GIF"))
			
			pygame.camera.init()

			await ctx.message.add_reaction(self.bot.emoji.timer)
			await asyncio.sleep(self.config["webcam_delay"])
			
			await ctx.message.remove_reaction(self.bot.emoji.timer, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.repeat_button)

			cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (self.config["small_cam_width"], self.config["small_cam_height"]))
			cam.start()
			
			counter = 0
			start_time = time.time()
			images = list()
			
			while (time.time() - start_time) < self.config["gif_length"]:
				images.append(cam.get_image())
				
			cam.stop()
				
			for i in range(len(images)):
				pygame.image.save(images[i], "cache/webcamgif" + str(i) + ".png")

			# 8 mb / (byte per pixel width per frames * frames)
			# 200 bytes per pixel width is a very rough estimate but it works well enough and
			# i dont really care as long as it works
			width = int(8*1024*1024 / (300 * len(images)))
			print(width)
				
			ffmpeg_args = "-y -framerate " + str(int(len(images) / self.config["gif_length"])) + " -i cache/webcamgif%d.png -vf scale=" + str(width) + ":-1,setpts=PTS*" + str(1/float(speed)) + " cache/funny.gif"
			
			if self.functions.ffmpeg2(ffmpeg_args):
				await ctx.message.remove_reaction(self.bot.emoji.repeat_button, ctx.message.guild.me)
				await ctx.message.add_reaction(self.bot.emoji.outbox_tray)
			
				await ctx.send(content="", file=discord.File("cache/funny.gif"))
				os.unlink("cache/funny.gif")
				for i in range(len(images)):
					os.unlink("cache/webcamgif" + str(i) + ".png")
			
			await ctx.message.remove_reaction(self.bot.emoji.outbox_tray, ctx.message.guild.me)
			await ctx.message.add_reaction(self.bot.emoji.check_mark)
			
		except Exception as exc:
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
