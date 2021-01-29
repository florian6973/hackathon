import pygame as pg
import utils
from jeu import Jeu
from character import *
import sys
import numpy as np

def main():
    map_n = ""    
    if len(sys.argv) >= 2:
        map_n = sys.argv[1]

    jeu = Jeu(map_n)


if __name__ == "__main__":
    main()