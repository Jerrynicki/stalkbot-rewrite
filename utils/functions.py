import pygame

pygame.mixer.pre_init(frequency=44100, channels=1)
pygame.mixer.init()

def warning_sound():
	snd = pygame.mixer.Sound("warning_sound.wav")
	snd.play()
