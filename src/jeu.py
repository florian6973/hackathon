import numpy as np
import pygame as pg
from map import Map
import character
class Jeu:
    def __init__(self):
        self.taille_x = 50
        self.taille_y = 25
        self.map = Map(self.taille_x, self.taille_y)
        self.map.load("map0.rg")
        
        pg.init()
        pg.display.set_caption("minimal program")
        self.font = pg.font.SysFont("Comic Sans MS", 16)
        self.screen = pg.display.set_mode((16 * self.taille_x, 16*self.taille_y))
        self.taille_case = 16
    def afficher(self, player):
        pg.draw.rect(self.screen, (0,0,0), (0, 0, self.taille_x * self.taille_case, self.taille_y * self.taille_case))
        for i in range(self.taille_y):
            for j in range(self.taille_x):
                img = self.font.render(self.map.map[i, j], True, (255, 255, 255))
                self.screen.blit(img,  (self.taille_case * j , self.taille_case *i ))
        self.screen.blit(player.image, player.rect)
        pg.display.flip()

                


            

        