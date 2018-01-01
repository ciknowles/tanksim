import pygame,sys
import math
from pygame.math import Vector2

from pygame.locals import *

pygame.init()
WIDTH = 350
HEIGHT = 350

DISPLAYSURF=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
pygame.display.set_caption('')

class Tank(pygame.Surface):  

        def __init__(self,
                     parent,
                     xpos,
                     ypos,
                     width,
                     height,
                     direction=0,
                     updaterate = 100,
                     upms = 1/200,
                     turret_deg_delta=5,
                     turret_deg_swing=60,
                     turret_upms = 1/10
                     ):
                super(Tank, self).__init__((width, height), pygame.SRCALPHA)
                self.xpos = xpos
                self.ypos = ypos
                self.xtarget = xpos
                self.ytarget = ypos
                self.parent = parent
                self.direction = direction
                self.updaterate = updaterate
                self.upms=upms
                self.turret_deg_delta=turret_deg_delta
                self.turret_deg_swing=turret_deg_swing
                self.turret_direction = 0
                self.turret_tdirection =self.turret_deg_swing
                self.turret_upms = turret_upms
                self.ticks = pygame.time.get_ticks()
                self.turret_ticks = pygame.time.get_ticks()
                self.turret_isincreasing = True
                
                self.fill
                self.fill((0,255,0))
                
        def update(self, parent):
                self.fill
                rsurface = self.rotate()
                dirty = False        
                deltaticks = pygame.time.get_ticks() - self.ticks
                if (deltaticks>=self.updaterate):
                        self.ticks = self.ticks + deltaticks
                        #check if we need to move
                        if ((self.xpos!=self.xtarget) or (self.ypos!=self.ytarget)):
                                 dirty=True
                                 xdis = self.xtarget - self.xpos
                                 ydis = self.ytarget - self.ypos
                                 dis = math.sqrt(xdis*xdis + ydis*ydis)
                                 if (dis>0):
                                         if (xdis>0):
                                                 self.xpos = self.xpos + xdis * self.upms*deltaticks/dis
                                                 if (self.xpos>self.xtarget):
                                                         self.xpos = self.xtarget
                                         else:
                                                 self.xpos = self.xpos + xdis * self.upms*deltaticks/dis
                                                 if (self.xpos<self.xtarget):
                                                         self.xpos = self.xtarget

                                         if (ydis>0):
                                                 self.ypos = self.ypos + ydis * self.upms*deltaticks/dis
                                                 if (self.ypos>self.ytarget):
                                                         self.ypos = self.ytarget
                                         else:
                                                 self.ypos = self.ypos + ydis * self.upms*deltaticks/dis
                                                 if (self.ypos<self.ytarget):
                                                         self.ypos = self.ytarget

                        #check if turret direction needs to change
                        #turret_deg_delta = 5
                        #turret_deg_swing = 50
                        #turrent_tdirection = 0
                        #turrent_upms = 1/100
                        #have we moved more than delta degs
                deltaticks = pygame.time.get_ticks() - self.turret_ticks        
                if (deltaticks*self.turret_upms>self.turret_deg_delta):
                        dirty=True
                        self.turret_ticks = pygame.time.get_ticks()
                        #increasing
                        if(self.turret_tdirection-self.turret_direction>0):
                                self.turret_isincreasing = True
                                self.turret_direction = self.turret_direction + self.turret_deg_delta
                                if (self.turret_direction>=self.turret_tdirection):
                                        self.turret_direction = self.turret_tdirection
                                        self.turret_tdirection = -self.turret_deg_swing
                        else:
                                self.turret_isincreasing = False
                                self.turret_direction = self.turret_direction - self.turret_deg_delta
                               # print(self.turret_tdirection )
                                if (self.turret_direction<=self.turret_tdirection):
                                        self.turret_direction = self.turret_tdirection
                                        self.turret_tdirection = self.turret_deg_swing
                                        

                                                
                parent.blit(rsurface, (self.xpos - rsurface.get_width()/2, self.ypos - rsurface.get_height()/2))
                pygame.draw.circle(parent,(0,0,255), (int(self.xpos), int(self.ypos)), 1, 0)
                return dirty
        #def update_snd(self,parent):

        def set_pos(self,x,y):
                self.xpos  = x
                self.ypos = y
        def get_x(self):
                return self.xpos
        def get_y(self):
                return self.ypos
        def set_x(self,x):
                self.xpos = x
        def set_y(self,y):
                self.ypos = y

        def get_turret_isincreasing(self):
                return self.turret_isincreasing
        
        def set_direction(self, angle):
                pygame.transform.rotate(self,self.direction)
                self.direction = angle
                
        def get_direction(self):
                return self.direction
                  
        def rotate(self):
                self.fill
                self.fill((0,255,0))
                return pygame.transform.rotate(self, -self.direction)

        def set_turret_direction(self,angle):
                self.turret_direction = angle

        def get_turret_direction(self):
                return self.turret_direction

        def get_actualturretdir(self):
                return (self.turret_direction + self.direction)%360

        def set_speed(self, unitspermillisecond):
                self.upms = unitspermillisecond

        def move_to(self, x, y):
                 self.ticks = pygame.time.get_ticks()
                 self.xtarget = x
                 self.ytarget = y
                 #set the direction
                 d = math.degrees(math.atan2(self.xtarget-self.xpos, self.ypos-self.ytarget))
                 if (d<0):
                         d = d+360
                 self.set_direction(d)
                 print(self.get_direction()) 
                 

        def set_updaterate(self, updaterate):
                self.updaterate = updaterate
                
                
class VRoom(object):
        mult = 1
        ptLast = [None, None]
 
        
        def __init__(self, parent,  width, height):
                self.swalls = pygame.Surface((WIDTH/self.mult, HEIGHT/self.mult), 0,8)
                self.flow = pygame.Surface((WIDTH/self.mult, HEIGHT/self.mult), 0,8)
                
                #super(VRoom, self).__init__((WIDTH/self.mult, HEIGHT/self.mult), 0)
                self.parent = parent
                palette = tuple([i,i,i] for i in range(256))
                self.swalls.set_palette(palette)
                self.swalls.fill((0))
                self.scopy = self.swalls.copy()
                self.dcopy = self.swalls.copy()
                self.dmask = self.swalls.copy()
                #self.dmask.fill((256,0,256))
                
        def update(self,parent):
                sur = pygame.transform.scale(self.swalls, (WIDTH, HEIGHT))
                self.parent.blit(sur, (0,0))

        def add(self, x, y, angle, sweepangle, distance, isbounded, isincreasing):
                self.scopy.fill((0))
                self.dcopy.fill((0))
                
                mult = self.mult

                #tank point
                p0 =Vector2(x/mult, y/mult)

                #blank 'nothing' triangle
                sdistance = distance-4
                p1 = Vector2()
                p1.from_polar((sdistance/mult,90-angle+sweepangle/2))
                p1[1] = -p1[1]        
                p1 = p1 + p0
                p2 = Vector2()
                p2.from_polar((sdistance/mult,90-angle-sweepangle/2))
                p2[1] = -p2[1]
                p2=p2+p0

                #points bounding either side of triangle
                ptNext = [Vector2(),Vector2()]
                ptNext[0].from_polar((distance/mult,90-angle-sweepangle/2))        
                ptNext[0][1] = -ptNext[0][1]
                ptNext[0] = ptNext[0] + p0

                ptNext[1].from_polar((distance/mult,90-angle+sweepangle/2))        
                ptNext[1][1] = -ptNext[1][1]
                ptNext[1] = ptNext[1] + p0


                pygame.draw.polygon(self.swalls, (0), [p0,p1,p2], 0)
                if isbounded:
                        if (self.ptLast[0]!=None):
                                idx = 0
                                if ((ptNext[0] - self.ptLast[0]).length_squared()>= (ptNext[1] - self.ptLast[1]).length_squared()):
                                        idx = 1
      
                                if ((ptNext[idx] - self.ptLast[idx]).length_squared()<(p2-p1).length_squared()):
                                        if (isincreasing):
                                                angle = (180+ (ptNext[idx]-self.ptLast[idx]).as_polar()[idx])%360
                                        else:
                                                angle = ((ptNext[idx]-self.ptLast[idx]).as_polar()[idx])%360
                                        
                                        pygame.draw.line(self.scopy, (40), self.ptLast[idx], ptNext[idx],4)
                                        #pygame.draw.line(self.scopy, (40,int(angle*256/360),0), self.ptLast[idx], ptNext[idx],4)
                                        self.swalls.blit(self.scopy, (0,0),None, pygame.BLEND_ADD)                                           
                        self.ptLast= ptNext
                                                 
                
                #self.blit(self.dmask, (0,0),None, pygame.BLEND_MIN)
                

        
class Room(pygame.Surface):
        wthickness = 10
        
        def __init__(self, parent,  width, height, wallthickness):
                super(Room, self).__init__((width, height), pygame.SRCALPHA)
                self.parent = parent
                self.wthickness = wallthickness
                self.fill
                pygame.draw.rect(self, (255,255,255), (self.wthickness/2,self.wthickness/2,self.get_width()-self.wthickness,
                                                       self.get_height()-self.wthickness),self.wthickness)
                pygame.draw.rect(self, (255,255,255), (200,200,20,30), 0)

                pygame.draw.circle(self, (255,255,255), (200,100),20, 0)

                self.mask = pygame.mask.from_surface(self)      
                
        def update(self, parent):
                self.parent.blit(self, (0,0))

        def get_distance(self, rc, x, y, angle):
                tpoints = rc.getpts(x,y,angle)
                row = 2
                tocount =row
                dis = -1
                #array arranged in 2,3,4,5,6, 7 dots
                for pt in tpoints:
                        tocount = tocount-1
                        #endof row and we have a distance
                        if ((tocount==0) and (dis>-1)):
                                return dis

                        #end of band so start the next one        
                        if (tocount==0):
                                row=row+1
                                tocount = row
                        
                        #hit something
                        if ((pt.x>0) and (pt.x<self.mask.get_size()[0]) and
                                    (pt.y>0) and (pt.y<self.mask.get_size()[1])):
                                if (self.mask.get_at((int(pt.x), int(pt.y)))):
                                       # print('hit',dis,pt.length())
                                        if ((dis==-1) or (pt.length()<dis)):
                                             dis = (pt-Vector2(x,y)).length()
                    
                return dis
        
class Raycast(object):
        dmax=0
        angle=30
        step =10
        seedpoints =[]
        rpoints=[]
        
        def __init__(self,dmax, angle, step):
                self.dmax = dmax
                self.angle = angle*1000
                self.step = step
                pts=0
                for d in range(step, dmax+1, step):
                        pts=pts+1                                
                        for a in range(int(-self.angle/2), int(self.angle/2)+1, int(self.angle/pts)):
                                #print(a)
                                v = Vector2(d*math.sin(math.radians(a/1000)), -d*math.cos(math.radians(a/1000)))
                                self.seedpoints.append(v)

                self.rpoints.append(self.seedpoints)
                for a in range(1, 360):
                        self.rpoints.append([])       
                        for pt in self.seedpoints:
                                self.rpoints[a].append(pt.rotate(a))

        def update(self, parent, x, y, angle):
                pts = self.getpts(x,y,angle)
                for pt in pts:
                       pygame.draw.circle(parent,(255,0,0), (int(pt.x), int(pt.y)), 1, 0)

        def getpts(self, x, y, angle):
                pts = self.rpoints[angle]
                t= Vector2(x,y)
                tpts = []
                for pt in pts:
                        tpts.append(pt+t)
                return tpts



#tank - xpos, ypos, width, height                                
tank=Tank(DISPLAYSURF, 100, 100, int(40), int(30))

#room - width, height, wall thickness
room=Room(DISPLAYSURF, WIDTH,HEIGHT,10)

cone = 30
maxdis = 400
#maxrange, cone spread, step
raycast = Raycast(maxdis, cone, 5)
vroom = VRoom(DISPLAYSURF, WIDTH, HEIGHT)


while 1:
        DISPLAYSURF.fill((0,0,0))
    
        
        for event in pygame.event.get():
                if event.type==QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        tank.move_to(pos[0],pos[1])
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                 tank.set_direction(tank.get_direction()+5)
                        if event.key == pygame.K_RIGHT:
                                 tank.set_direction(tank.get_direction()-5)
                        if event.key == pygame.K_UP:
                            tank.set_y(tank.get_y()-1)
                        if event.key == pygame.K_DOWN:
                            tank.set_y(tank.get_y()+1)

       
        
        vroom.update(DISPLAYSURF)
        raycast.update(DISPLAYSURF, tank.get_x(),tank.get_y(), int(tank.get_actualturretdir()))     
        if (tank.update(DISPLAYSURF)):
                dis = room.get_distance(raycast, tank.get_x(), tank.get_y(), int(tank.get_actualturretdir() ))
                if (dis>0):
                        vroom.add(tank.get_x(), tank.get_y(), tank.get_actualturretdir(), cone, dis, True, tank.get_turret_isincreasing())
                else:
                        vroom.add(tank.get_x(), tank.get_y(), tank.get_actualturretdir(), cone, maxdis, False, tank.get_turret_isincreasing())
       # room.update(DISPLAYSURF)
        pygame.display.update()

        pygame.display.flip()
