import numpy as np
import os
import utils
import random as rd

#matrice avec string

class Map:

    def __init__(self, tx, ty):
        self.map = np.full((ty, tx), " ", dtype='U1') #ne pas inverser
        self.__folder__ = 'resx/maps/'
        self.__encoding__ = 'UTF-8'
        self.__delimiter__ = ' '
        self.__comment__ = '§'

    @staticmethod
    def get_img(char):
        folder = 'resx/imgs/'
        def c(n):
            return utils.get_path(folder + n)
        if char=='¤':
            return ""
        elif char in ['-', '|']:
            return c('mur.png')
        elif char in ['#']:
            return c('couloir.png')
        elif char in ['.']:
            return c('sol.png')
        elif char in ['o']:
            return c('door.png') # faire doorenter ensuite
        else:
            raise Exception("Unknown char")

    def get_tile(self, i, j):
        return Map.get_img(self.map[i,j])


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
            dep_x = rd.randrange(1, tx-1) # pas sur le bord
            dep_y = rd.randrange(1, ty-1)
            if (self.map[dep_y, dep_x] == '¤'):
                return (dep_y, dep_x)
            else:
                return valid_pos()
        self.map = np.full((ty, tx), "¤", dtype='U1')
        nb_rooms = rd.randint(1,6)
        for _ in range(nb_rooms):
            i,j = valid_pos()
            self.map[i,j] = '.'
            #pièce carrée
            taille = rd.randint(3,9)
            for ib in range(i, i+taille):
                for jb in range(j ,j+taille):
                    if (0 < ib < (ty-1)) and 0 < (jb) < (tx-1):
                        self.map[ib,jb] = '.'


        print(self.map)
        



def test_map():
    print("Running test_map")
    m = Map(50, 25) # incohérent
    m.load("map0.rg")
    print(Map.get_img(m.map[2,3]))
    print(m.map)
    m.generate()

    m.save("map1.rg")

test_map()