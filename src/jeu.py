import numpy as np
import pygame as pg
from map import Map
import character
import os
from utils import get_path
class Jeu:
    def __init__(self):
        self.taille_x = 50
        self.taille_y = 25
        self.map = Map(self.taille_x, self.taille_y)
        self.map.load("map0.rg")
        icone = pg.image.load("resx/imgs/icon.png")

        pg.display.set_icon(icone)
        
        pg.init()
        pg.display.set_caption("minimal program")
        self.font = pg.font.SysFont("Comic Sans MS", 16)
        self.screen = pg.display.set_mode((16 * self.taille_x, 16*self.taille_y + 100))
        self.taille_case = 16
    def afficher(self, player, ennemi):
        pg.draw.rect(self.screen, (255,255,255), (0, 0, self.taille_x * self.taille_case, self.taille_y * self.taille_case + 100))
        text_vie = self.font.render("Vie = " + str(player.life), True, (0,0,0))
        text_money = self.font.render("Argent = " + str(player.money), True, (0,0,0))
        text_damage = self.font.render("Attaque = " + str(player.damage), True, (0,0,0))
        text_defense = self.font.render("Defense = " + str(player.defense), True, (0,0,0))
        self.screen.blit(text_vie, [10, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(text_money, [200, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(text_damage, [400, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(text_defense, [600, self.taille_y * self.taille_case + 20, 16, 16])

        for i in range(self.taille_y):
            for j in range(self.taille_x):
                for img in self.map.get_tile(i, j):
                    self.screen.blit(img, (self.taille_case * j , self.taille_case *i ))
        if player.alive:
            self.screen.blit(player.images[player.indice_animation], player.rect)
        if ennemi.alive:
            self.screen.blit(ennemi.image, ennemi.rect)
        
        pg.display.flip()

                


            

        