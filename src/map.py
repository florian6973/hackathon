import numpy as np
import os
import utils

#matrice avec string

class Map:
    def __init__(self, tx, ty):
        self.map = np.full((ty, tx), " ", dtype='U1') #ne pas inverser

    def load(self, name):
        self.map = np.genfromtxt(utils.get_path('resx/maps/' + name), delimiter=' ', dtype='U1', comments='§', encoding='UTF-8')
        print(f"Map {name} loaded (shape {self.map.shape})")        

    def save(self):
        pass

    def generate(self):
        pass



def test_map():
    print("Running test_map")
    m = Map(3, 2)
    m.load("map0.rg")
    print(m.map)

test_map()