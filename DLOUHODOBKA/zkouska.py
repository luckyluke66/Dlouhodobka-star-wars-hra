import pygame, sys
from pygame.locals import *

BLACK  = (0, 0,0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE   = (0,0,255)

GREEN = (0,255,0)


# Data Definition
class helloWorld:
    '''Create a resizable hello world window'''
    def __init__(self):
        pygame.init()
        self.width = 300
        self.height = 300
        DISPLAYSURF = pygame.display.set_mode((self.width,self.height), RESIZABLE)
        DISPLAYSURF.fill(WHITE)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.CreateWindow(event.w,event.h)
            pygame.display.update()

    def CreateWindow(self,width,height):
        '''Updates the window width and height '''
        pygame.display.set_caption("Press ESC to quit")
        DISPLAYSURF = pygame.display.set_mode((width,height),RESIZABLE)
        DISPLAYSURF.fill(WHITE)


if __name__ == '__main__':
    helloWorld().run()
