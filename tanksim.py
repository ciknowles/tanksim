import pygame,sys
from pygame.locals import *

pygame.init()
WIDTH = 300
HEIGHT = 300

DISPLAYSURF=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My first game')


        
#tank object. Position, direction, ultrasound, drawer for ultrasound
class Tank(pygame.Surface):
        d = 0

        def __init__(self, parent, xpos, ypos, direction, width, height):
                super(Tank, self).__init__((width, height), pygame.SRCALPHA)
                self.xpos = xpos
                self.ypos = ypos
                self.parent = parent
                self.d = direction
                self.fill
                self.fill((0,255,0))
        
        def update(self, parent):
                rsurface = self.rotate()
                parent.blit(rsurface, (self.xpos - rsurface.get_width()/2, self.ypos - rsurface.get_height()/2))
                pygame.draw.circle(parent,(255,0,0), (self.xpos, self.ypos), 2, 0)

        def rotate(self):
                self.fill
                self.fill((0,255,0))
                return pygame.transform.rotate(self, self.d)
                

     
tank=Tank(DISPLAYSURF, 100, 100, 60, int(50), int(60))

while 1:
        for event in pygame.event.get():
                if event.type==QUIT:
                        pygame.quit()
                        sys.exit()

        tank.update(DISPLAYSURF)
        pygame.display.update()
     
