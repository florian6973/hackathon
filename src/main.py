import pygame as pg

def main():    
    # initialize the pygame module
    pg.init()
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pg.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode((240,180))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    print("left")



if __name__ == "__main__":
    main()