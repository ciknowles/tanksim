import pygame,sys
import math
from pygame.math import Vector2

from pygame.locals import *

pygame.init()
WIDTH = 300
HEIGHT = 300

DISPLAYSURF=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My first game')


    
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

        #def update_snd(self,parent):
                
        def rotate(self):
                self.fill
                self.fill((0,255,0))
                return pygame.transform.rotate(self, self.d)
                

class Room(pygame.Surface):
        wthickness = 5

        def __init__(self, parent,  width, height, wallthickness):
                super(Room, self).__init__((width, height), pygame.SRCALPHA)
                self.parent = parent
                self.wthickness = wallthickness
                self.fill
                pygame.draw.rect(self, (255,255,255), (self.wthickness/2,self.wthickness/2,self.get_width()-self.wthickness, self.get_height()-self.wthickness),self.wthickness)
                
                
        def update(self, parent):
                self.parent.blit(self, (0,0))
               
class Raycast(object):
        dmax=0
        angle=30
        step =10
        seedpoints =[]
        rpoints=[]
        
        def __init__(self,dmax, angle, step):
                self.dmax = dmax
                self.angle = angle
                self.step = step
                pts=0
                for d in range(0, dmax, step):
                        pts=pts+1                                
                        for a in range(int(-angle/2), int(angle/2)+1, int(angle/pts)):
                                v = Vector2(d*math.cos(math.radians(a+90)), -d*math.sin(math.radians(a+90)))
                                self.seedpoints.append(v)
                for a in range(0, 360):
                        self.rpoints.append([])       
                        for pt in self.seedpoints:
                                self.rpoints[a].append(pt.rotate(a))

        def update(self, parent, x, y, angle):
                pts = self.rpoints[-angle]
                t= Vector2(x,y)
                for pt in pts:
                        tpt = pt+t
                        pygame.draw.circle(parent,(255,0,0), (int(tpt.x), int(tpt.y)), 2, 0)
                
                                
tank=Tank(DISPLAYSURF, 100, 100, 60, int(50), int(60))
room=Room(DISPLAYSURF, WIDTH,HEIGHT,10)
raycast = Raycast(100, 30, 25)

while 1:
        for event in pygame.event.get():
                if event.type==QUIT:
                        pygame.quit()
                        sys.exit()

        tank.update(DISPLAYSURF)
        room.update(DISPLAYSURF)
        raycast.update(DISPLAYSURF, 100,100, 10)
        pygame.display.update()
     
