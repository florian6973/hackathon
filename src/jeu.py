import numpy as np
import pygame as pg
from map import Map
import character
import os
from utils import get_path
import time


class Jeu:
    def __init__(self, map_name):
        self.taille_x = 50
        self.taille_y = 25
        self.map = Map(self.taille_x, self.taille_y)
        if (map_name == ""):
            self.map.generate()
            self.map.save("map_" + str(int(time.time())) + ".rg")
        else:
            self.map.load(map_name)
        icone = pg.image.load(get_path("resx/imgs/icon.png"))

        pg.display.set_icon(icone)

        pg.init()
        pg.display.set_caption("Le Wisher : Gérard Dérive")
        self.font = pg.font.SysFont("Comic Sans MS", 16)
        self.screen = pg.display.set_mode(
            (16 * self.taille_x, 16*self.taille_y + 100))
        self.taille_case = 16
        

        self.son_attaque_gerard = pg.mixer.Sound(
            get_path('resx/bgm/swordhit.mp3'))
        #self.potion = self.map.textures['!']

    def afficher(self, player, ennemis):
        pg.draw.rect(self.screen, (255, 255, 255), (0, 0, self.taille_x *
                                                    self.taille_case, self.taille_y * self.taille_case + 100))
        text_vie = self.font.render(
            "Vie = " + str(player.life), True, (0, 0, 0))
        text_money = self.font.render(
            "Argent = " + str(player.money), True, (0, 0, 0))
        text_damage = self.font.render(
            "Attaque = " + str(player.damage), True, (0, 0, 0))
        text_defense = self.font.render(
            "Defense = " + str(player.defense), True, (0, 0, 0))
        text_mana = self.font.render(
            "Mana = " + str(player.mana), True, (0, 0, 0))
        text_potion0 = self.font.render(
            "Potion vie = " + str(player.inventory[0]), True, (0, 0, 0))
        text_potion1 = self.font.render(
            "Potion defense = " + str(player.inventory[1]), True, (0, 0, 0))
        text_potion2 = self.font.render(
            "Potion mana = " + str(player.inventory[2]), True, (0, 0, 0))
        text_potion3 = self.font.render(
            "Potion attaque = " + str(player.inventory[3]), True, (0, 0, 0))
        self.screen.blit(
            text_vie, [10, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(
            text_money, [150, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(
            text_damage, [300, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(
            text_defense, [450, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(
            text_mana, [600, self.taille_y * self.taille_case + 20, 16, 16])
        self.screen.blit(
            text_potion0, [10, self.taille_y * self.taille_case + 50, 16, 16])
        self.screen.blit(
            text_potion1, [150, self.taille_y * self.taille_case + 50, 16, 16])
        self.screen.blit(
            text_potion2, [300, self.taille_y * self.taille_case + 50, 16, 16])
        self.screen.blit(
            text_potion3, [450, self.taille_y * self.taille_case + 50, 16, 16])
        for i in range(self.taille_y):
            for j in range(self.taille_x):
                for img in self.map.get_tile(i, j):
                    self.screen.blit(
                        img, (self.taille_case * j, self.taille_case * i))
        if player.alive:
            self.screen.blit(
                player.images[player.indice_animation], player.rect)
        for ennemi in ennemis:
            if ennemi.alive:
                self.screen.blit(
                    ennemi.images[ennemi.indice_animation], ennemi.rect)

        pg.display.flip()
