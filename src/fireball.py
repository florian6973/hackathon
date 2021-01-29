
import numpy as np
import pygame as pg
from map import Map
import character
import os
from utils import get_path
import time
class Fireball:
    def __init__(self, x, y, direction):
        self.image = pg.image.load(get_path("resx/imgs/igni.png"))
        self.rect = self.image.get_rect()
        self.rect.x = 16 * x
        self.rect.y = 16 * y
        self.coordonnees_x = x
        self.coordonnees_y = y
        self.direction = [0, 0]
        if direction == 'droite':
            self.direction = (1, 0)
        elif direction == 'gauche':
            self.direction = (-1, 0)
            self.image = pg.transform.scale(self.image, True, False)
        elif direction == 'bas':
            self.direction = (0, 1)
        else:
            self.direction = (0, -1)
        self.afficher = True
    def move(self):
        self.coordonnees_x += self.direction[0]
        self.coordonnees_y += self.direction[1]
        self.rect.x += 16*self.direction[0]
        self.rect.y += 16*self.direction[1]
    def stop(self):
        self.afficher = False 