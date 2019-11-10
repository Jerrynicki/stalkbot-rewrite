import discord
import discord.ext.commands
import logging
import json
import asyncio
import os

import commands
import utils

logging.basicConfig(level=logging.INFO)

config = json.load(open("config.json"))

if not os.path.isdir("cache"):
	os.mkdir("cache")

bot = discord.ext.commands.Bot(command_prefix=config["prefix"], description="Stalkbot")

bot.config = config
bot.emoji = utils.emojis.Emojis()

timeouts = utils.timeouts.Timeouts()

bot.add_cog(commands.webcam.Webcam(bot, utils.functions, timeouts))
bot.add_cog(commands.screenshot.Screenshot(bot, utils.functions, timeouts))

while True:
	print("Starting event loop...")
	asyncio.get_event_loop().run_until_complete(bot.start(config["token"]))
