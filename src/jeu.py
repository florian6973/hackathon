# -*- coding: utf-8 -*-

import numpy as np
import pygame as pg
from map import Map
import character
import os
from utils import get_path
import time
import pygame_menu as pgm
from character import *
import utils


def run_game(jeu):
    x,y=list(zip(*np.where(jeu.map.map == '@')))[0][::-1]
    player = Player("Robin", pos=(x,y))
    
    gobs =list(zip(*np.where(jeu.map.map == '&')))#[0][::-1]
    ennemis = []
    for i, g in enumerate(gobs):
        x, y = g[::-1]
        ennemis.append(Evil("Gobelin " + str(i), 7, 2, x, y))
        
    MUSIC = utils.get_path('resx/bgm/wishertheme.mp3')
    pg.mixer.init()
    pg.mixer.music.load(MUSIC)
    pg.mixer.music.set_volume(3/10.)
    pg.mixer.music.play(-1)
        
    running = True
     
    # main loop
    while running:
        pg.time.wait(50)
        if player.attaque:
            player.indice_animation += 1
            if player.indice_animation == len(player.images) - 1:
                player.attaque = False
                jeu.son_attaque_gerard.stop()
                player.indice_animation = 0
        for ennemi in ennemis:
            if ennemi.attaque:
                ennemi.indice_animation += 1
                if ennemi.indice_animation == len(ennemi.images) - 1:
                    ennemi.attaque = False
                    jeu.son_attaque_gerard.stop()
                    ennemi.indice_animation = 0
            if ennemi.alive:
                l = [jeu.map.map[ennemi.coordonnees_y, ennemi.coordonnees_x + 1], jeu.map.map[ennemi.coordonnees_y, ennemi.coordonnees_x - 1], jeu.map.map[ennemi.coordonnees_y - 1, ennemi.coordonnees_x], jeu.map.map[ennemi.coordonnees_y + 1, ennemi.coordonnees_x]]
                ennemi.move(player, jeu.taille_case, l)
        
        jeu.afficher(player, ennemis)
        if player.alive:
            player.rentrer_mur(jeu.map.map[player.coordonnees_y + player.direction[1], player.coordonnees_x + player.direction[0]])
            player.move(jeu.taille_case)
            potion_recupere = player.get_potion(jeu.map.map[player.coordonnees_y, player.coordonnees_x])
            if potion_recupere:
                jeu.map.map[player.coordonnees_y, player.coordonnees_x] = "."
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.direction = (-1, 0)
                    if player.orientation != "gauche":
                        for i in range(len(player.images)):
                            player.images[i] = pg.transform.flip(player.images[i], True, False)
                        player.orientation = 'gauche'
                elif event.key == pg.K_RIGHT:
                    player.direction = (1, 0)
                    if player.orientation != 'droite':
                        for i in range(len(player.images)):
                            player.images[i] = pg.transform.flip(player.images[i], True, False)
                        player.orientation = 'droite'
                elif event.key == pg.K_UP:
                    player.direction = (0, -1)
                elif event.key == pg.K_DOWN:
                    player.direction = (0, 1)
                elif event.key == pg.K_SPACE and not player.attaque:
                    player.attaque = True
                    jeu.son_attaque_gerard.play()
                    for ennemi in ennemis:
                        if ennemi.fight:
                            player.combat(ennemi)
                elif event.key == pg.K_f:
                    jeu.son_potion.play()
                    player.use_object("force")
                elif event.key == pg.K_m:
                    jeu.son_potion.play()
                    player.use_object("mana")
                elif event.key == pg.K_d:
                    jeu.son_potion.play()
                    player.use_object("defense")
                elif event.key == pg.K_v:
                    jeu.son_potion.play()
                    player.use_object("vie")
            elif event.type == pg.KEYUP:
                player.direction = (0, 0)

class Jeu:
    def __init__(self, map_name):
        def run():
            run_game(self)
        def set_nom(val):
            #print(val)
            self.comment = self.font.render(val + ", trouvez l'objet caché !", True, (0, 0, 0))
        
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

        self.taille_case = 16        
        self.comment = "Trouvez l'objet caché !"
        self.son_attaque_gerard = pg.mixer.Sound(
            get_path('resx/bgm/swordhit.mp3'))
        self.font = pg.font.SysFont("Comic Sans MS", 16)
        sx, sy = 16 * self.taille_x, 16*self.taille_y + 100
        self.screen = pg.display.set_mode(
            (sx, sy))

        menu = pgm.Menu(300, 400, 'LE WISHER',
                       theme=pgm.themes.THEME_DARK)
        menu.add_text_input('Nom :', default='Gérard', onchange=set_nom)
        #menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)        
        menu.add_button('Jouer', run)
        menu.add_button('Quitter', pgm.events.EXIT)
        menu.mainloop(self.screen)

        self.son_potion = pg.mixer.Sound(
            get_path('resx/bgm/potion.mp3'))
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
            "Potion vie = " + str(player.inventory['vie']), True, (0, 0, 0))
        text_potion1 = self.font.render(
            "Potion defense = " + str(player.inventory['defense']), True, (0, 0, 0))
        text_potion2 = self.font.render(
            "Potion mana = " + str(player.inventory['mana']), True, (0, 0, 0))
        text_potion3 = self.font.render(
            "Potion force = " + str(player.inventory['force']), True, (0, 0, 0))
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
        self.screen.blit(
            self.comment, [10, self.taille_y * self.taille_case + 80, 16, 16])
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
        if fireball.afficher:
            self.screen.blit(fireball.image, fireball.rect)

        pg.display.flip()
