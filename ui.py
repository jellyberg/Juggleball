import pygame, time

pygame.init()

BASICFONT       = pygame.font.Font('fonts/roboto medium.ttf', 14)
MEDIUMFONT      = pygame.font.Font('fonts/roboto regular.ttf', 16)
BIGFONT         = pygame.font.Font('fonts/roboto regular.ttf', 25)
INSTRUCTIONFONT = pygame.font.Font('fonts/roboto thin.ttf', 30)

def genText(text, topLeftPos, colour, font):
	surf = font.render(text, 1, colour)
	surf.set_colorkey((0,0,0))
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



class ScoreDisplay:
	def __init__(self, game):
		self.labelSurf, self.labelRect = genText('SCORE: ', (0, 0), game.YELLOW, BIGFONT)
		self.labelRect.topright = (game.WINDOWRECT.width - 100, 10)
		self.labelSurf.convert_alpha()
		self.lastScore = -1 # always generate score surf on first update


	def update(self, game, screen):
		if game.score != self.lastScore:
			self.scoreSurf, self.scoreRect = genText(str(game.score), (0, 0), game.YELLOW, BIGFONT)
			self.scoreRect.topleft = self.labelRect.topright
		screen.blit(self.labelSurf, self.labelRect)
		screen.blit(self.scoreSurf, self.scoreRect)
		self.lastScore = game.score



class TutorialText(pygame.sprite.Sprite):
	lifetime = 5
	def __init__(self, text, game):
		pygame.sprite.Sprite.__init__(self)
		self.add(game.tutorialText)
		self.surf, self.rect = genText(text, (0, 0), game.BLACK, INSTRUCTIONFONT)
		self.rect.midtop = (game.WINDOWRECT.width / 2, game.WINDOWRECT.height - 150)
		self.text = text
		self.birthTime = time.time()


	def update(self, game, screen):
		if time.time() - self.birthTime > TutorialText.lifetime:
			self.kill()
			return True
		screen.blit(self.surf, self.rect)
