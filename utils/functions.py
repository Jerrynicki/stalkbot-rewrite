import pygame
import time
import asyncio
import subprocess


async def warning_sound():
	pygame.mixer.pre_init(frequency=44100, channels=1)
	pygame.mixer.init()

	snd = pygame.mixer.Sound("warning_sound.wav")
	snd.play()
	while pygame.mixer.get_busy():
		await asyncio.sleep(0.1)
	await asyncio.sleep(0.3)
	
	pygame.mixer.quit()

async def play_sound(filepath):
	pygame.mixer.pre_init(frequency=44100, channels=2)
	pygame.mixer.init()

	snd = pygame.mixer.Sound(filepath)
	snd.play()
	while pygame.mixer.get_busy():
		await asyncio.sleep(0.1)
	
	pygame.mixer.quit()

def ffmpeg(inputf, args, outputf):
	try:
		subprocess.run(["ffmpeg", "-y", "-i", inputf, *args, outputf], check=True, timeout=20)
		return True
	except Exception as exc:
		print(exc)
		return False

def notification(fmt, command, ctx):
	text = fmt
	text = text.replace("AUTHOR", ctx.message.author.name + "#" + ctx.message.author.discriminator)
	text = text.replace("COMMAND", command)
	text = text.replace("SERVER", ctx.message.guild.name)
	text = text.replace("CHANNEL", "#" + ctx.message.channel.name)
	
	subprocess.run(["notify-send", "-t", "5000", "Stalkbot", text], timeout=3)
	
