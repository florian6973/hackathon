
import numpy as np
import pygame as pg
from map import Map
import character
import os
from utils import get_path
import time
class Fireball:
    def __init__(self, x, y, direction):
        self.image = pg.image.load.(get_path("resx/imgs/igni.png"))
        self.rect = self.image.get_rect()
        self.rect.x = 16 * x
        self.rect.y = 16 * y
        self.coordonnees_x = x
        self.coordonnees_y = y
        if direction[0] == 'droite':
            self.direction[0] = 1
        else:
            self.direction[0] = -1
        if direction[1] == 'bas':
            self.direction[1] = 1
        else:
            self.direction[1] = -1
        self.afficher = True
    def move(self):
        self.x += direction[0]
        self.y += direction[1]
        self.rect.x += 16*direction[0]
        self.rect.y += 16*direction[1]
    def stop(self):
        self.afficher = False 