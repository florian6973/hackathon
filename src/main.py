import pygame as pg
import utils
from jeu import Jeu
from character import *

def main():    
    player = Player("Robin")
    jeu = Jeu()
    ennemi = Evil("JE", 7, 1, 3, 3)
    player.rect.x = jeu.taille_case
    player.rect.y = jeu.taille_case

        
    MUSIC = utils.get_path('resx/bgm/Lazare.mp3')
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
                player.indice_animation = 0
        jeu.afficher(player, ennemi)
        player.rentrer_mur(jeu.map.map[player.coordonnees_y + player.direction[1], player.coordonnees_x + player.direction[0]])
        player.move(jeu.taille_case)
        l = [jeu.map.map[ennemi.coordonnees_y, ennemi.coordonnees_x + 1], jeu.map.map[ennemi.coordonnees_y, ennemi.coordonnees_x - 1], jeu.map.map[ennemi.coordonnees_y - 1, ennemi.coordonnees_x], jeu.map.map[ennemi.coordonnees_y + 1, ennemi.coordonnees_x]]
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
                elif event.key == pg.K_SPACE and not player.attaque:
                    player.attaque = True
                    player.combat(ennemi)
            elif event.type == pg.KEYUP:
                player.direction = (0, 0)



if __name__ == "__main__":
    main()