import discord
import discord.ext.commands
import logging
import json
import asyncio
import os
import sys
import time
import random

import commands
import utils

async def update_status():
	while True:
		try:
			if config["status"] == "":
				continue
			await bot.wait_until_ready()
			await bot.change_presence(activity=discord.Game(name=config["status"]))
		except Exception as exc:
			print("update_status(): " + repr(exc))
		await asyncio.sleep(15)

async def clear_command_log():
	while True:
		try:
			to_delete = list()
			cur_time = time.time()
			for x in range(len(command_log)):
				if command_log[x][0] + 300 < cur_time:
					to_delete.append(x)
					
			for x in to_delete:
				del command_log[x]
			
			await asyncio.sleep(15)
		except Exception as exc:
			print("clear_command_log(): " + repr(exc))

async def delete_last_loop():
	global bot
	while True:
		try:
			if bot.last_own_message == None:
				app.delete_last_message_button.config(state="disabled")
			else:
				app.delete_last_message_button.config(state="normal")

			if bot.delete_last:
				bot.delete_last = False
				await bot.last_own_message.delete()
				bot.last_own_message = None

			await asyncio.sleep(2)
		except Exception as exc:
			print("delete_last_loop(): " + repr(exc))

logging.basicConfig(level=logging.INFO)

config = json.load(open("config.json"))
try:
	features_toggle = json.load(open("features_toggle.json"))
except:
	features_toggle = {"screenshot": True, "webcam": True, "tts": True, "play": True, "proc": True, "flashbang": True, "webcamgif": True}
	json.dump(features_toggle, open("features_toggle.json", "w"))

try:
	user_blacklist = json.load(open("blacklist.json"))
except:
	user_blacklist =  []
	json.dump(user_blacklist, open("blacklist.json", "w"))

if not os.path.isdir("cache"):
	os.mkdir("cache")

bot = discord.ext.commands.Bot(command_prefix=config["prefix"], description="Stalkbot")

bot.emoji = utils.emojis.Emojis()
timeouts = utils.timeouts.Timeouts()
command_log = list() # Each element is 1 command, consisting of (timestamp, ctx, command)

if "win" in sys.platform.lower():
	bot.windows = True
else:
	bot.windows = False

if bot.windows:
	utils.functions.init("ffmpeg.exe", "windows")
else:
	utils.functions.init("ffmpeg", "other")

if os.path.isfile("ffmpeg_override.txt"):
	functions.init(open("ffmpeg_override.txt", "r").read().replace("\n", ""))
		
@bot.event
async def on_message(message):
	global bot
	if message.author.id == bot.user.id:
		bot.last_own_message = message
	elif not message.author.bot and not message.author.name + "#" + message.author.discriminator in user_blacklist:
		await bot.process_commands(message)

bot.last_own_message = None
bot.delete_last = False
bot.add_cog(commands.webcam.Webcam(bot, config, features_toggle, utils.functions, timeouts, command_log))
bot.add_cog(commands.screenshot.Screenshot(bot, config, features_toggle, utils.functions, timeouts, command_log))
bot.add_cog(commands.tts.TTS(bot, config, features_toggle, utils.functions, timeouts, command_log))
bot.add_cog(commands.play.Play(bot, config, features_toggle, utils.functions, timeouts, command_log))
bot.add_cog(commands.folder.Folder(bot, config, features_toggle, utils.functions, timeouts, command_log))
bot.add_cog(commands.proc.Proc(bot, config, features_toggle, utils.functions, timeouts, command_log))
bot.add_cog(commands.flashbang.Flashbang(bot, config, features_toggle, utils.functions, timeouts, command_log))

bot.loop.create_task(update_status())
bot.loop.create_task(clear_command_log())

app = utils.gui.App(bot, config, features_toggle, command_log, user_blacklist)
app.start()

bot.loop.create_task(delete_last_loop())

bot.run(config["token"])
