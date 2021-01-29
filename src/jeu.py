import numpy as np
import pygame as pg
from map import Map
import character

class Jeu:
    def __init__(self, map_name):
        self.taille_x = 50
        self.taille_y = 25
        self.map = Map(self.taille_x, self.taille_y)
        self.map.load(map_name)
        
        pg.init()
        pg.display.set_caption("minimal program")
        self.font = pg.font.SysFont("Comic Sans MS", 16)
        self.screen = pg.display.set_mode((16 * self.taille_x, 16*self.taille_y))
        self.taille_case = 16
    def afficher(self, player):
        pg.draw.rect(self.screen, (0,0,0), (0, 0, self.taille_x * self.taille_case, self.taille_y * self.taille_case))
        for i in range(self.taille_y):
            for j in range(self.taille_x):
                for img in self.map.get_tile(i, j):
                    self.screen.blit(img, (self.taille_case * j , self.taille_case *i ))
        self.screen.blit(player.image, player.rect)
        pg.display.flip()

                


            

        