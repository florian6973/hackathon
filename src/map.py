import numpy as np
import os
import random as rd
import pygame as pg
import sys

import utils
from utils import *
import time

class Map:
    def __init__(self, tx, ty):
        self.map = np.full((ty, tx), " ", dtype='U1') #ne pas inverser
        self.__folder__ = 'resx/maps/'
        self.__encoding__ = 'UTF-8'
        self.__delimiter__ = ' '
        self.__comment__ = '§'
        self.superposes = ['v', 'a', 'd', 'm', '+']

        folder_img = 'resx/imgs/'
        self.textures = {'-': pg.image.load(get_path(folder_img + 'wall.png')),
                         '|': pg.image.load(get_path(folder_img + 'wall.png')),
                         'v': pg.image.load(get_path(folder_img + 'lifepotion.png')),
                         'a': pg.image.load(get_path(folder_img + 'strengthpotion.png')),
                         'd': pg.image.load(get_path(folder_img + 'defpotion.png')),
                         'm': pg.image.load(get_path(folder_img + 'manapotion.png')),
                         '+' : pg.image.load(get_path(folder_img + 'door.png')),
                         '#' : pg.image.load(get_path(folder_img + 'corridor.png')),
                         '.' : pg.image.load(get_path(folder_img + 'sol.png')),
                         '¤' : pg.image.load(utils.get_path(folder_img + 'void.png'))}

    def get_tile(self, i, j):
        if self.map[i,j] in self.textures:
            t = self.textures[self.map[i,j]]
            if self.map[i,j] in self.superposes:
                return [self.textures['.'], t]
            else:
                return [t]
        elif self.map[i,j] == '@':
            return [self.textures['.']]
        else:
            return [self.textures['¤']]

    def load(self, name):
        self.map = np.genfromtxt(utils.get_path(self.__folder__ + name), delimiter=self.__delimiter__, dtype='U1', comments=self.__comment__, encoding=self.__encoding__)
        print(f"Map {name} loaded (shape {self.map.shape})")        

    def save(self, name):
        np.savetxt(utils.get_path(self.__folder__ + name), self.map, fmt='%s', delimiter=self.__delimiter__, encoding=self.__encoding__)
        print(f"Map {name} saved")

    def generate(self, seed=None):
        if seed != None:
            rd.seed(seed)

        ty, tx = self.map.shape
        self.map = np.full((ty, tx), "¤", dtype='U1')
        cases = []

        def valid_pos():            
            j = rd.randrange(1, tx-2) # pas sur le bord
            i = rd.randrange(1, ty-2) # en bas case pas vide
            taille = min(rd.randint(3,7),ty-i, tx-j)

            recouvrement = False
            for ib in range(i, i+taille):
                for jb in range(j ,j+taille):
                    if (self.map[ib, jb] != '¤'):
                        recouvrement = True
            
            if (self.map[i, j] == '¤') and not recouvrement:
                return (i, j, taille)
            else:
                return valid_pos()


        nb_rooms = rd.randint(7,14)
        col = []
        for _ in range(nb_rooms):
            i,j, taille = valid_pos()
            borders = []
            for ib in range(i, i+taille):
                for jb in range(j ,j+taille):
                    if ((ib!=i) and (jb!=j) and (ib!=(i+taille-1)) and (jb!=(j+taille-1))):
                        if (self.map[ib,jb] == '¤'):
                            self.map[ib,jb] = '.'
                        cases.append((ib,jb))
                    else:
                        if (self.map[ib,jb] == '¤'):
                            self.map[ib,jb] = '-'
                        if (not ((ib == i) and (jb == j)) # pour la porte, quelles frontières bien
                        and not ((ib==i) and (jb==(j+taille-1)))
                        and not ((ib==(i+taille-1)) and (jb==j)) 
                        and not ((ib==(i+taille-1)) and (jb==(j+taille-1)))):
                            if ((0 < ib < (ty-1)) and (0 < (jb) < (tx-1))):
                                borders.append((ib,jb))
            col.append(borders)

        # portes
        locs = []
        for e in col:
            tmp = rd.randrange(0, len(e))
            vu = set()
            while len(list(get_neighbors(self.map, e[tmp]))) == 0 and len(vu) < len(e):
                tmp = rd.randrange(0, len(e))
                vu.add(e[tmp])           
            locs.append(e[tmp])            
            self.map[locs[-1]] = '+'

        # couloirs
        k = len(locs)
        for i in range(k):
            for j in range(i, k):
                if i != j:
                    try:
                        p = find_path(self.map, locs[i], locs[j])
                        for e in p[1:-1]:
                            self.map[e] = '#'
                    except:
                        print('err')
        
        # personnages, potions, gobelins

        def ajouter_elem(elem, min_i=1, max_i=6):
            nb_potions = rd.randint(min_i, max_i)
            for _ in range(nb_potions):
                ind = rd.randrange(0, len(cases))
                self.map[cases[ind]] = elem
                del cases[ind]
                if (len(cases) == 0):
                    break

        ajouter_elem('@', 1, 1)
        ajouter_elem('!')
        ajouter_elem('&', 2, 10)    

        print("Map generated")   
