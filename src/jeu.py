import numpy as np
import pygame as pg
from map import Map
class Jeu:
    def __init__(self):
        self.map = Map(100, 50)
        self.taille_x = 100
        self.taille_y = 50
        pg.init()
        pg.display.set_caption("minimal program")
        self.font = pg.font.SysFont(None, 16)
        self.screen = pg.display.set_mode((1600, 800))
        self.taille_case = 16
    def afficher(self):
        for i in range(50):
            for j in range(100):
                img = self.font.render(self.map.map[i, j], True, (255, 255, 255))
                self.screen.blit(img,  (self.taille_case * j , self.taille_case *i ))


                


            

        