
import math
import os
import sys
import pickle
import random

import pygame
from pygame.locals import *

# makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

from gameinstances import *
from gamefunc import *
from events import *

class CPUController:
    '''
    The while-loop is here

    Implements fps-limit and takes care of gamepauses
    used with menus, inventories, dialogues etc.
    '''
    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.clock = pygame.time.Clock()
        self.ticking = 1
        self.state = "ingame"
        self.ticktime = 0
    def tickTock(self):
        while self.ticking:
            self.clock.tick(35)
            if self.state == "ingame":
                self.mediator.inform(InGameTick())
            elif self.state == "menu":
                self.mediator.inform(MenuTick())
            elif self.state == "pause":
                self.mediator.inform(PauseTick())
    def inform(self, event):
        if event.name == 'Quit':
            # stop the while-loop
            self.ticking = 0

