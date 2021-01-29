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
        pg.time.wait(100)
        jeu.afficher(player)
        player.move(jeu.taille_case)
        player.rentrer_mur(jeu.map.map[player.rect.x//jeu.taille_case + player.direction[0]], jeu.map.map[player.rect.y//jeu.taille_case + player.direction[1]])
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.direction = (-1, 0)
                elif event.key == pg.K_RIGHT:
                    player.direction = (1, 0)
                elif event.key == pg.K_UP:
                    player.direction = (0, -1)
                elif event.key == pg.K_DOWN:
                    player.direction = (0, 1)
            elif event.type == pg.KEYUP:
                player.direction = (0, 0)



if __name__ == "__main__":
    main()