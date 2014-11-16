import pygame, webbrowser

BIGFONT         = pygame.font.Font('fonts/roboto thin.ttf', 32)

def genText(text, topLeftPos, colour, font):
	surf = font.render(text, 1, colour)
	surf.set_colorkey((0,0,0))
	rect = surf.get_rect()
	rect.topleft = topLeftPos
	return (surf, rect)

class ThanksForPlaying:
	"""Popup that thanks the player and shows a couple of links to other stuff"""
	top = 220  # distance from top of window
	def __init__(self, winSize, screen):
		self.buttons = []
		texts = ['Resume', 'Play my other games', 'Read my devblog', 
					 'Hear about my next game', 'Exit']
		for i in range(len(texts)):
			self.buttons.append({'text': texts[i]})
			self.buttons[i]['surf'], self.buttons[i]['rect'] = genText(texts[i], (0, 0), (255, 255, 255), BIGFONT)
			self.buttons[i]['rect'].midbottom = (winSize[0] / 2, ThanksForPlaying.top + i*100)

		self.greySurf = pygame.Surface(winSize)
		self.greySurf.fill((0, 0, 0))
		self.greySurf.set_alpha(100)

		self.prevScreen = screen.copy()
		self.prevScreen.blit(self.greySurf, (0, 0))


	def update(self, winSize, screen, userInput, FPSClock):
		userInput.get(winSize, screen, FPSClock, True)

		screen.blit(self.prevScreen, (0, 0))

		for button in self.buttons:
			screen.blit(button['surf'], button['rect'])

			if button['rect'].collidepoint(userInput.mousePos) and userInput.mouseUnpressed == 1:
				if button['text'] == 'Resume':
					return 'DONE'
				if 'games' in button['text']:
					webbrowser.open('http://jellyberg.itch.io/')
				if 'devblog' in button['text']:
					webbrowser.open('http://jellybergfish.tumblr.com')
				if 'next  game' in button['text']:
					webbrowser.open('http://jellybergfish.tumblr.com/mailing-list')
				if button['text'] == 'Exit':
					userInput.terminate()
		pygame.display.update()


def showOutro(winSize, screen, FPSClock, userInput):
	outro = ThanksForPlaying(winSize, screen)
	done = False

	while not done:
		done = outro.update(winSize, screen, userInput, FPSClock)
	FPSClock.tick(60)