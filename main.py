# Flappy Flock
# a game by Adam Binks

import pygame, input, random

from pygame.locals import *

pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.init()

WINDOWWIDTH, WINDOWHEIGHT = (1200, 600)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


def genText(text, topLeftPos, colour, font):
	surf = font.render(text, 1, colour)
	rect = surf.get_rect()
	rect.topleft = topLeftPos
	return (surf, rect)



class StateHandler:
	def __init__(self):
		"""Start the program"""
		self.gameHandler = GameHandler()


	def update(self):
		self.gameHandler.update()


class GameHandler:
	def __init__(self):
		"""Start the program"""
		self.game = GameData()

		self.addNewBird()


	def update(self):
		self.game.input.get()

		# game
		screen.fill(self.game.SKYBLUE)
		self.game.birdGroup.update(self.game)

		pygame.display.update()
		pygame.display.set_caption('Flappy Flock   FPS: ' + str(int(self.game.FPSClock.get_fps())))
		self.game.dt =  self.game.FPSClock.tick(self.game.FPS) / 1000.0


	def addNewBird(self):
		Bird(random.choice(self.game.POSSIBLEKEYCODES), random.choice(self.game.pastelColours.values()), self.game,
							(random.randint(300, 600), random.randint(400, 500)))



class GameData:
	"""Stores globally important game data. To be passed between methods"""
	def __init__(self):
		self.input = input.Input()
		self.FPSClock = pygame.time.Clock()
		self.dt = 0.1

		self.birdGroup = pygame.sprite.Group()


		# CONSTANTS
		self.FPS = 60
		self.BASICFONT = pygame.font.Font('fonts/roboto medium.ttf', 14)
		self.MEDIUMFONT =pygame.font.Font('fonts/roboto regular.ttf', 16)
		self.BIGFONT   = pygame.font.Font('fonts/roboto regular.ttf', 20)
		self.WINDOWRECT = pygame.Rect((0, 0), (WINDOWWIDTH, WINDOWHEIGHT))
		
		self.gravity = 20
		self.POSSIBLEKEYCODES = [K_a, K_s, K_d, K_f, K_h, K_j, K_k, K_l] # home keys!

		# COLOURS        ( R ,  G ,  B )
		self.WHITE     = (255, 255, 255)
		self.BLACK     = (  0,   0,   0)
		self.SKYBLUE   = (135, 206, 250)
		self.DARKBLUE  = (  0,  35, 102)
		self.YELLOW    = (255, 250,  17)
		self.GREEN     = (110, 255, 100)
		self.ORANGE    = (255, 165,   0)
		self.DARKGREY  = ( 60,  60,  60)
		self.LIGHTGREY = (180, 180, 180)
		self.CREAM     = (255, 255, 204)

		self.pastelColours = {'yellow': (253,253, 150),
							  'orange': (255, 179, 71),
							  'pink':   (255, 209, 220),
							  'purple': ( 50,  20,  50),
							  'brown':  (130, 105,  83),
							  'grey':   (207, 207, 196),
							  'green':  (119, 221, 119)}


class Bird(pygame.sprite.Sprite):
	"""Player controlled bird, dies on collision with pipes"""
	jumpVelocity = 20

	fadedCircle = pygame.Surface((120, 120))
	fadedCircle.set_colorkey((  0,   0,   0))
	pygame.draw.circle(fadedCircle, (255, 255, 255), (60, 60), 60)
	fadedCircle.set_alpha(100)

	def __init__(self, key, colour, game, centerPos):
		pygame.sprite.Sprite.__init__(self)
		self.add(game.birdGroup)
		self.key, self.colour = key, colour
		self.genSurf(game, centerPos)

		self.velocity = 0 # y velocity
		self.isDead = False
		self.hasJumped = False


	def update(self, game):
		if self.key in game.input.unpressedKeys and not self.isDead:
			self.jump()
			self.hasJumped = True

		if self.hasJumped:
			self.updateYPosition(game)

		if not self.isDead:
			self.collisionRect.center = self.rect.center
			if not game.WINDOWRECT.collidepoint(self.rect.midtop) or not game.WINDOWRECT.collidepoint(self.rect.midbottom):
				if not game.WINDOWRECT.collidepoint(self.rect.midtop):
					self.velocity = 0
				elif not game.WINDOWRECT.collidepoint(self.rect.midbottom):
					self.velocity = 5

				self.xVelocity = random.randint(-700, -200)
				self.isDead = True
				self.surf.blit(Bird.fadedCircle, (0,0))

		if self.isDead:
			if self.rect.top > game.WINDOWRECT.bottom:
				self.kill()
			else:
				self.rect.x += self.xVelocity * game.dt
				
				modifier = -1
				if self.xVelocity < 0:
					modifier = 1
				self.xVelocity += modifier

		screen.blit(self.surf, self.rect)


	def jump(self):
		self.velocity += Bird.jumpVelocity


	def updateYPosition(self, game):
		self.velocity -= game.gravity * game.dt
		self.rect.y -= self.velocity
		if self.velocity < 0: # travelling upwards
			self.rect.y -= self.velocity


	def genSurf(self, game, centerPos):
		"""Generates a surface and rect object for the bird"""
		self.circleSurf = pygame.Surface((120, 120))
		self.circleSurf.set_colorkey(game.BLACK)

		self.rect = self.circleSurf.get_rect()
		self.rect.center = centerPos
		self.collisionRect = self.rect.copy()
		self.collisionRect.width -= 25
		self.collisionRect.height -= 25

		halfRectWidth = int(self.rect.width / 2.0)
		pygame.draw.circle(self.circleSurf, self.colour, (halfRectWidth, halfRectWidth), halfRectWidth) # coloured circle
		pygame.draw.circle(self.circleSurf, game.LIGHTGREY, (halfRectWidth, halfRectWidth), halfRectWidth, 5) # outline

		self.surf = self.circleSurf.copy()

		keyTextSurf, keyTextRect = genText(pygame.key.name(self.key).upper(), (0,0), game.DARKGREY, game.BIGFONT)
		keyTextRect.center = (halfRectWidth, halfRectWidth)
		self.surf.blit(keyTextSurf, keyTextRect)




if __name__ == '__main__':
	stateHandler = StateHandler()
	while True:
		stateHandler.update()