import discord
import discord.ext.commands
import logging
import json
import asyncio
import os
import sys

import commands
import utils

async def update_status():
	while True:
		try:
			if config["status"] == "":
				continue
			await bot.wait_until_ready()
			await bot.change_presence(status=discord.Game(name=config["status"]))
			await asyncio.sleep(15)
		except Exception as exc:
			print(exc)

logging.basicConfig(level=logging.INFO)

config = json.load(open("config.json"))
try:
	features_toggle = json.load(open("features_toggle.json"))
except:
	features_toggle = {"screenshot": True, "webcam": True, "tts": True, "play": True}
	json.dump(features_toggle, open("features_toggle.json", "w"))

if not os.path.isdir("cache"):
	os.mkdir("cache")

bot = discord.ext.commands.Bot(command_prefix=config["prefix"], description="Stalkbot")

bot.emoji = utils.emojis.Emojis()
timeouts = utils.timeouts.Timeouts()

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


bot.add_cog(commands.webcam.Webcam(bot, config, features_toggle, utils.functions, timeouts))
bot.add_cog(commands.screenshot.Screenshot(bot, config, features_toggle, utils.functions, timeouts))
bot.add_cog(commands.tts.TTS(bot, config, features_toggle, utils.functions, timeouts))
bot.add_cog(commands.play.Play(bot, config, features_toggle, utils.functions, timeouts))

bot.loop.create_task(update_status())

app = utils.gui.App(bot, config, features_toggle)
app.start()

while True:
	print("Starting event loop...")
	asyncio.get_event_loop().run_until_complete(bot.start(config["token"]))
