# Juggleball
# a game by Adam Binks

import pygame, input, random, time, ui

from pygame.locals import *

pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.init()

WINDOWWIDTH, WINDOWHEIGHT = (1200, 800)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSClock = pygame.time.Clock()


def genText(text, topLeftPos, colour, font):
	surf = font.render(text, 1, colour).convert_alpha()
	surf.set_colorkey((0,0,0))
	rect = surf.get_rect()
	rect.topleft = topLeftPos
	return (surf, rect)



class StateHandler:
	def __init__(self):
		"""Start the program"""
		screen.fill((135, 206, 250))
		pygame.display.update()
		pygame.time.wait(400)
		self.input = input.Input()
		self.mode = 'menu'
		self.menu = MenuScreen('Press SPACE to play Juggleball')
		FPSClock.tick(60)


	def update(self):
		self.input.get()
		screen.fill((135, 206, 250))

		if self.mode == 'menu':
			isDone = self.menu.update(self.input)
			if isDone:
				self.mode = 'game'
				self.gameHandler = GameHandler(self.input)

		if self.mode == 'game':
			result = self.gameHandler.update()
			if result == 'game over':
				self.mode = 'menu'
				self.menu = MenuScreen('Press SPACE to play again')
		
		pygame.display.update()
		pygame.display.set_caption('Juggleball')



class MenuScreen:
	font   = pygame.font.Font('fonts/roboto thin.ttf', 30)
	def __init__(self, text):
		self.playAgainText, self.playAgainRect = genText(text, (0, 0), ( 60,  60,  60), MenuScreen.font) # light grey
		self.playAgainAlpha = 0
		self.playAgainRect.midbottom = (WINDOWWIDTH / 2, WINDOWHEIGHT)
		self.playAgainTargetY = WINDOWHEIGHT / 2


	def update(self, userInput):
		dt = FPSClock.tick(60) / 100.0

		if self.playAgainRect.centery > self.playAgainTargetY:
			self.playAgainRect.centery -= (self.playAgainRect.centery - self.playAgainTargetY) * 0.35 * dt

		self.playAgainText.set_alpha(self.playAgainAlpha)
		self.playAgainAlpha += 0.0005 * dt
		if self.playAgainAlpha > 255: self.playAgainAlpha = 255

		screen.blit(self.playAgainText, self.playAgainRect)

		if K_SPACE in userInput.unpressedKeys:
			return 'done'





class GameHandler:
	def __init__(self, userInput):
		"""Start the program"""
		self.game = GameData()
		self.game.input = userInput

		self.addNewBird(self.game)
		for bird in self.game.birdGroup:
			bird.add(self.game.activeBirds)


	def update(self):
		self.game.birdGroup.update(self.game)

		if len(self.game.activeBirds) > 0:
			if time.time() - self.game.lastNewBirdTime > self.game.BIRDSPAWNINTERVAL:
				self.addNewBird(self.game)
			# 
			pygame.draw.rect(screen, self.game.LIGHTGREY, ((0, WINDOWHEIGHT - 30), 
							 (((float(time.time()) - self.game.lastNewBirdTime + 0.01) / self.game.BIRDSPAWNINTERVAL) * WINDOWWIDTH, 30)))

		self.game.dt =  FPSClock.tick(self.game.FPS) / 1000.0
		
		if len(self.game.birdGroup) == 0: # all balls are dead and have disappeared
			pygame.time.wait(200)
			return 'game over'


	def addNewBird(self, game):
		if len(game.inactiveKeys) == 0:
			return  # all keys have active balls
		Bird(random.choice(self.game.inactiveKeys), random.choice(self.game.pastelColours.values()), random.randint(50, 150),
							 game, (random.randint(300, WINDOWWIDTH - 300), random.randint(400, 500)))
		game.lastNewBirdTime = time.time()



class GameData:
	"""Stores globally important game data. To be passed between methods"""
	def __init__(self):
		self.dt = 0.1

		self.birdGroup = pygame.sprite.Group()
		self.activeBirds = pygame.sprite.Group()

		# CONSTANTS
		self.FPS = 60
		self.BASICFONT = pygame.font.Font('fonts/roboto medium.ttf', 14)
		self.MEDIUMFONT =pygame.font.Font('fonts/roboto regular.ttf', 16)
		self.BIGFONT   = pygame.font.Font('fonts/roboto regular.ttf', 20)
		self.BIRDFONT = pygame.font.Font('fonts/roboto medium.ttf', 25)
		self.WINDOWRECT = pygame.Rect((0, 0), (WINDOWWIDTH, WINDOWHEIGHT))
		
		self.POSSIBLEKEYCODES = [K_h, K_j, K_k] #[K_a, K_s, K_d, K_f, K_h, K_j, K_k, K_l] # home keys
		self.inactiveKeys = self.POSSIBLEKEYCODES
		self.BIRDSPAWNINTERVAL = 5

	# COLOURS        ( R ,  G ,  B )
		self.WHITE     = (255, 255, 255)
		self.BLACK     = (  0,   0,   0)
		self.SKYBLUE   = (135, 206, 250)
		self.DARKBLUE  = (  0,  35, 102)
		self.YELLOW    = (255, 255, 102)
		self.DARKYELLOW= (204, 204,   0)
		self.GREEN     = (110, 255, 100)
		self.ORANGE    = (255, 165,   0)
		self.DARKGREY  = ( 60,  60,  60)
		self.LIGHTGREY = (180, 180, 180)
		self.CREAM     = (255, 255, 204)

		self.pastelColours = {'yellow': (253,253, 150),
							  'orange': (255, 179, 71),
							  'red'   : (250, 105, 97),
							  'pink':   (255, 209, 220),
							  'brown':  (130, 105,  83),
							  'grey':   (207, 207, 196),
							  'green':  (119, 221, 119)}


class Bird(pygame.sprite.Sprite):
	"""Player controlled bird, dies on collision with pipes"""
	jumpVelocity = 8
	timeTillCompulsaryJump = 5  # gravity does not act upon the bird until it jumps or this amount of time is elapsed

	def __init__(self, key, colour, size, game, centerPos):
		pygame.sprite.Sprite.__init__(self)
		self.add(game.birdGroup)
		self.key, self.colour, self.size = key, colour, size
		game.inactiveKeys.remove(self.key) # only one ball with each key
		self.genSurf(game, centerPos)

		self.velocity = 0 # y velocity
		self.gravity = 20 * size / 150.0
		self.maxAlpha = 80
		self.isDead = False
		self.hasJumped = False
		self.alpha = 1.0
		self.birthTime = time.time()


	def update(self, game):
		if self.key in game.input.justPressedKeys and not self.isDead:
			self.jump()
			if not self.hasJumped:
				self.hasJumped = True
				self.add(game.activeBirds)
				self.surf = self.circleSurf.copy()
				self.maxAlpha = 255

		if not self.hasJumped and time.time() - self.birthTime > Bird.timeTillCompulsaryJump:
			self.hasJumped = True  # start falling
			self.surf = self.circleSurf.copy()

		if self.hasJumped:
			self.updateYPosition(game)
			self.surf.set_alpha(255)
		else:
			self.maxAlpha = 50
			if time.time() - self.birthTime > Bird.timeTillCompulsaryJump - 1:
				self.surf.blit(self.redCircle, (0, 0))

		if not self.isDead:
			if not game.WINDOWRECT.collidepoint(self.rect.midtop) or not game.WINDOWRECT.collidepoint(self.rect.midbottom):
				if not game.WINDOWRECT.collidepoint(self.rect.midtop):
					self.velocity = 0
				elif not game.WINDOWRECT.collidepoint(self.rect.midbottom):
					self.velocity = 5

				self.xVelocity = random.randint(-700, 700)
				self.isDead = True
				self.surf.blit(self.fadedCircle, (0,0))

		if self.isDead:
			if self.key not in game.inactiveKeys:
				game.inactiveKeys.append(self.key)
			self.remove(game.activeBirds)
			if self.rect.top > game.WINDOWRECT.bottom:
				self.kill()
			else:
				self.rect.x += self.xVelocity * game.dt
				
				modifier = -1
				if self.xVelocity < 0:
					modifier = 1
				self.xVelocity += modifier

		if not self.hasJumped and self.alpha < self.maxAlpha:
			self.alpha += 1
			self.surf.set_alpha(self.alpha)
		screen.blit(self.surf, self.rect)


	def jump(self):
		self.velocity = Bird.jumpVelocity


	def updateYPosition(self, game):
		self.velocity -= self.gravity * game.dt
		self.rect.y -= self.velocity


	def genSurf(self, game, centerPos):
		"""Generates a surface and rect object for the bird"""
		self.circleSurf = pygame.Surface((self.size, self.size))
		self.circleSurf.set_colorkey(game.BLACK)

		self.rect = self.circleSurf.get_rect()
		self.rect.center = centerPos

		halfRectWidth = int(self.rect.width / 2.0)
		pygame.draw.circle(self.circleSurf, self.colour, (halfRectWidth, halfRectWidth), halfRectWidth) # coloured circle
		pygame.draw.circle(self.circleSurf, game.LIGHTGREY, (halfRectWidth, halfRectWidth), halfRectWidth, 5) # outline

		keyTextSurf, keyTextRect = genText(pygame.key.name(self.key).upper(), (0,0), game.DARKGREY, game.BIRDFONT)
		keyTextRect.center = (halfRectWidth, halfRectWidth)
		self.circleSurf.blit(keyTextSurf, keyTextRect)

		self.fadedCircle = pygame.Surface((self.size, self.size))
		self.fadedCircle.set_colorkey(game.BLACK)
		pygame.draw.circle(self.fadedCircle, game.WHITE, (self.size / 2, self.size / 2), self.size / 2)
		self.fadedCircle.set_alpha(100)
	
		self.redCircle = pygame.Surface((self.size, self.size))
		self.redCircle.set_colorkey(game.BLACK)
		pygame.draw.circle(self.redCircle, game.pastelColours['red'], (self.size / 2, self.size / 2), self.size / 2)
		self.redCircle.set_alpha(20)
		
		self.surf = self.circleSurf.copy()



if __name__ == '__main__':
	stateHandler = StateHandler()
	while True:
		stateHandler.update()