# Juggleball
# a game by Adam Binks

import pygame, sys
from pygame.locals import *

class Input:
    """A class to handle input accessible by all other classes"""
    def __init__(self):
        self.pressedKeys = []
        self.mousePressed = False
        self.mouseUnpressed = False
        self.mousePos = (0, 0)
        

    def get(self):
        """Update variables - mouse position and click state, and pressed keys"""
        self.mouseUnpressed = False
        self.unpressedKeys = []
        self.justPressedKeys = []

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key not in self.pressedKeys:
                    self.justPressedKeys.append(event.key)
                self.pressedKeys.append(event.key)
            elif event.type == KEYUP:
                for key in self.pressedKeys:
                    if event.key == key:
                        self.pressedKeys.remove(key)
                    self.unpressedKeys.append(key)
            elif event.type == MOUSEMOTION:
                self.mousePos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                self.mousePressed = event.button
                self.mouseUnpressed = False
            elif event.type == MOUSEBUTTONUP:
                self.mousePressed = False
                self.mouseUnpressed = event.button
            elif event.type == QUIT:
                pygame.event.post(event)
        
        self.checkForQuit()


    def checkForQuit(self):
        """Terminate if QUIT events"""
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        if K_ESCAPE in self.unpressedKeys:
            self.terminate()


    def terminate(self):
        """Safely end the program"""
        pygame.quit()
        sys.exit()