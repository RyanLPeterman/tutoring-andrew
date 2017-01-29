import pygame, sys
from pygame.locals import *

def main():
    # initialize pygame object
    pygame.init()

    screen_width = 500
    screen_height = 400

    # create display object with set dimensions
    display=pygame.display.set_mode((screen_width, screen_height))

    # RGB values for white and blue
    WHITE=(255,255,255)
    BLUE=(0,0,255)

    # fill the screen with white
    display.fill(WHITE)

    # draw the rectangle
    pygame.draw.rect(display , BLUE, (200,150,100,50))

    # do this forever
    while True:
        # check if someone tries to close the window
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        # refresh the window
        pygame.display.update()

if __name__ == "__main__":
    main()
