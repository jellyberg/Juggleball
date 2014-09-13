import pygame, random

SOUND = {}
for filename in ['pop', 'shatter', 'whoosh', 'booshWhaWhaWhaWha', 'jingle']: # .wav files only
	SOUND[filename] = pygame.mixer.Sound('assets/sounds/%s.wav' %(filename))

def play(sound, volume=0.8, varyVolume=True ,loops=0):
	"""Plays the given sound"""
	if varyVolume:
		volume -= random.uniform(0.0, 0.2)
		if volume < 0.1: volume == 0.1
		SOUND[sound].set_volume(volume)
	SOUND[sound].play(loops)


def startMusic():
	# OBSOLETE ATM
	pygame.mixer.music.load('sounds/INSERT MUSIC FILE NAME HERE.mp3')
	pygame.mixer.music.play(-1)