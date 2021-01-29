import pygame as pg
from jeu import Jeu
from character import *

def main():    
    player = Player("Robin")
    player.rect.x = 0
    player.rect.y = 0
    jeu = Jeu()
    running = True
     
    # main loop
    while running:
        jeu.afficher(player)
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.rect.x -= jeu.taille_case
                if event.key == pg.K_RIGHT:
                    player.rect.x += jeu.taille_case
                if event.key == pg.K_UP:
                    player.rect.y -= jeu.taille_case
                if event.key == pg.K_DOWN:
                    player.rect.y += jeu.taille_case



if __name__ == "__main__":
    main()