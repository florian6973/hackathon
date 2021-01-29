import numpy as np
import os
import utils
import random as rd
import pygame as pg
import sys

class Map:
    def __init__(self, tx, ty):
        self.map = np.full((ty, tx), " ", dtype='U1') #ne pas inverser
        self.__folder__ = 'resx/maps/'
        self.__encoding__ = 'UTF-8'
        self.__delimiter__ = ' '
        self.__comment__ = '§'
        self.superposes = ['!']

        folder_img = 'resx/imgs/'
        self.textures = {'-': pg.image.load(utils.get_path(folder_img + 'wall.png')),
                         '|': pg.image.load(utils.get_path(folder_img + 'wall.png')),
                         '!': pg.image.load(utils.get_path(folder_img + 'defpotion.png')),
                         '+' : pg.image.load(utils.get_path(folder_img + 'door.png')),
                         '#' : pg.image.load(utils.get_path(folder_img + 'corridor.png')),
                         '.' : pg.image.load(utils.get_path(folder_img + 'sol.png')),
                         '¤' : pg.image.load(utils.get_path(folder_img + 'void.png'))}

    def get_tile(self, i, j):
        if self.map[i,j] in self.textures:
            t = self.textures[self.map[i,j]]
            if self.map[i,j] in self.superposes:
                return [self.textures['.'],t]
            else:
                return [t]
        else:
            return [self.textures['¤']]

    def load(self, name):
        self.map = np.genfromtxt(utils.get_path(self.__folder__ + name), delimiter=self.__delimiter__, dtype='U1', comments=self.__comment__, encoding=self.__encoding__)
        print(f"Map {name} loaded (shape {self.map.shape})")        

    def save(self, name):
        np.savetxt(utils.get_path(self.__folder__ + name), self.map, fmt='%s', delimiter=self.__delimiter__, encoding=self.__encoding__)

    def generate(self, seed=None):
        if seed != None:
            rd.seed(seed)
        ty, tx= self.map.shape
        def valid_pos():            
            dep_x = rd.randrange(1, tx-2) # pas sur le bord
            dep_y = rd.randrange(1, ty-2) # en bas case pas vide
            if (self.map[dep_y, dep_x] == '¤'):
                return (dep_y, dep_x)
            else:
                return valid_pos()
        self.map = np.full((ty, tx), "¤", dtype='U1')
        nb_rooms = rd.randint(1,8)
        col = []
        for _ in range(nb_rooms):
            i,j = valid_pos()
            self.map[i,j] = '.'
            #pièce carrée
            taille = min(rd.randint(3,8),ty-i, tx-j)
            borders = []
            for ib in range(i, i+taille):
                for jb in range(j ,j+taille):
                    if ((ib!=i) and (jb!=j) and (ib!=(i+taille-1)) and (jb!=(j+taille-1))): # ((0 < ib < (ty-1)) and (0 < (jb) < (tx-1))) and 
                        self.map[ib,jb] = '.'
                    else:
                    #elif ((0 <= ib <= (ty-1)) and (0 <= (jb) <= (tx-1))):
                        self.map[ib,jb] = '-'
                        #if ((ib!=i) and (jb!=j) and (ib!=(i+taille-1)) and (jb!=(j+taille-1)))
                        
                        borders.append((ib,jb))
                        #faire la bonne taille pour simplifier...
                    #elif ((0 <= ib <= (ty-1)) and (0 <= (jb) <= (tx-1))): 
                    #    self.map[ib,jb] = '-'
                    #elif (((0 <= ib <= (ty-1)) and (0 <= (jb) <= (tx-1))) and ((ib==i) or (jb==j) or (ib==(i+taille-1)) or (jb==(j+taille-1)))):
                    #    self.map[ib,jb] = '-'
            col.append(borders)

        for e in col:
            self.map[e[rd.randrange(0, len(e))]] = '+'
        



        print(self.map)
        

## arobase 

def test_map():
    print("Running test_map")
    m = Map(50, 25) # incohérent
    m.load("map0.rg")
    #print(Map.get_img(m.map[2,3]))
    print(m.map)
    print(m.get_tile(2,3))
    m.generate()

    m.save("map1.rg")

if (len(sys.argv) == 2):
    test_map()