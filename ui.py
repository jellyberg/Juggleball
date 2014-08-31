import pygame

pygame.init()

BASICFONT = pygame.font.Font('fonts/roboto medium.ttf', 14)
MEDIUMFONT =pygame.font.Font('fonts/roboto regular.ttf', 16)
BIGFONT   = pygame.font.Font('fonts/roboto regular.ttf', 20)

def genText(text, topLeftPos, colour, font):
	surf = font.render(text, 1, colour)
	rect = surf.get_rect()
	rect.topleft = topLeftPos
	return (surf, rect)


class Button:
	"""A simple button, can be clickable. When clicked, self.isClicked=True"""
	def __init__(self, text, screenPos, font, game, screenPosIsTopRight=0):
		self.text, self.screenPos, self.posIsTopRight = text, screenPos, screenPosIsTopRight
		
		self.textSurf = font.render(self.text, 1, game.DARKGREY)

		# CREATE BASIC SURF
		self.padding = 10
		self.buttonSurf = pygame.Surface((self.textSurf.get_width() + self.padding,
										  self.textSurf.get_height() + self.padding)).convert()
		self.buttonSurf.fill(game.pastelColours['yellow'])
		self.buttonSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
		self.currentSurf = self.buttonSurf
		self.rect = pygame.Rect(self.screenPos, self.buttonSurf.get_size())
		if self.posIsTopRight:
			self.rect.topright = self.screenPos
		else:
			self.rect.topleft = self.screenPos

		# CREATE ADDITIONAL SURFS

		# MOUSE HOVER
		self.hoverSurf = pygame.Surface(self.buttonSurf.get_size()).convert()
		self.hoverSurf.fill(game.YELLOW)
		self.hoverSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))

		# MOUSE CLICK
		self.clickSurf = pygame.Surface(self.buttonSurf.get_size()).convert()
		self.clickSurf.fill(game.DARKYELLOW)
		self.clickSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
		self.isClicked = False
		self.isHovered = False

	def simulate(self, userInput, screen):
		if self.isClickable:
			self.handleClicks(userInput)
		screen.blit(self.currentSurf, self.rect)

	def handleClicks(self, userInput):
		self.isClicked = False
		wasHovered = self.isHovered
		self.isHovered = False
		if self.rect.collidepoint(userInput.mousePos):
			if userInput.mousePressed == 1:
				self.currentSurf = self.clickSurf
			else:
				if not wasHovered:
					pass #sound.play('tick', 0.8, False)
				self.currentSurf = self.hoverSurf
				self.isHovered = True
		else:
			self.currentSurf = self.buttonSurf
		if userInput.mouseUnpressed == True and self.rect.collidepoint(userInput.mousePos):
			self.isClicked = True
			#sound.play('click', 0.8, False)