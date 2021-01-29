import pygame
from jeu import Jeu
def main():    
    jeu = Jeu()
    running = True
     
    # main loop
    while running:
        jeu.afficher()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False



if __name__ == "__main__":
    main()