import pygame as pg
from jeu import Jeu
from character import *

def main():    
    player = Player("Robin")
    jeu = Jeu()
    ennemi = Evil("JE", 100, 1, 5, 5)
    player.rect.x = jeu.taille_case
    player.rect.y = jeu.taille_case
    
    running = True
     
    # main loop
    while running:
        pg.time.wait(50)
        jeu.afficher(player, ennemi)
        player.rentrer_mur(jeu.map.map[player.coordonnees_y + player.direction[1], player.coordonnees_x + player.direction[0]])
        player.move(jeu.taille_case)
        l = [jeu.map.map(ennemi.coordonnees_x + 1, ennemi_coordonnees_y), jeu.map.map(ennemi.coordonnees_x - 1, ennemi_coordonnees_y), jeu.map.map(ennemi.coordonnees_x, ennemi_coordonnees_y - 1), jeu.map.map(ennemi.coordonnees_x, ennemi_coordonnees_y + 1)]
        ennemi.move(player, jeu.taille_case, l)

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