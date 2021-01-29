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
            elif event.type == pg.KEYUP:
                player.direction = (0, 0)



if __name__ == "__main__":
    main()