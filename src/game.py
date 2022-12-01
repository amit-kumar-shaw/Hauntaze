from enum import Enum

import pygame
from settings import *
from menu import Menu

class Status(Enum):
    MENU = 1
    STORY = 2
    RUNNING = 3
    OVER = 4

class Game:
    def __init__(self):
        self.status = Status.MENU
        self.menu = Menu()

    def run(self):
        if self.status == Status.MENU:
            self.menu.update()