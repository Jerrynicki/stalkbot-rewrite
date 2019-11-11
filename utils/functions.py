import pygame
import time
import asyncio


async def warning_sound():
	pygame.mixer.pre_init(frequency=44100, channels=1)
	pygame.mixer.init()

	snd = pygame.mixer.Sound("warning_sound.wav")
	snd.play()
	while pygame.mixer.get_busy():
		await asyncio.sleep(0.1)
	await asyncio.sleep(0.3)
	
	pygame.mixer.quit()
