import pygame, pygame.font, pygame.event, pygame.draw, string,time
from pygame.locals import*
WHITE=(255,255,255)
blue=(0,0,255)
lblue=(0,255,255)
BRICK=(255, 51, 0)
BLACK=(0,0,0)
green=(0,255,0)
YELLOW = (255,255,0)
GREY = (128,128,128)
button = False
KEYDOWN = False
rectx = 0
recty = 0
#charge constants
chargemod = 1.2
#unit = (Mcavalry,Bcavalry,swordsman,archers,pikemen,catapult)
positive = +1
negative = -1
flat = 1
#vARIABLES FOR HIGHLIGHTING AN AREA 
startpost = []
endpost = []
mpost = []
rectx = 0
recty = 0
#-NEED TO ADD A METHOD TO WORK OUT WHICH UNITS ARE WITHIN THE GIVEN AREA
#unit properties
health = {
"Mcavalry":80,
"Bcavalry":75,
"swordsman":90,
"archers":70,
"pikemen":90,
"catapult":50,
}
defence = {
"Mcavalry":50,
"Bcavalry":50,
"swordsman":65,
"archers":45,
"pikemen":70,
"catapult":30
}
attack = {
"Mcavalry":5,
"Bcavalry":8,
"swordsman":6,
"archers":10,
"pikemen":15,z
}
speed = {
"Mcavalry":50,
"Bcavalry":50,
"swordsman":65,
"archers":45,
"pikemen":70,
"catapult":30,
}
tilesize = 64
#choose your units


#to find the tile the unit is on
pygame.init()
DISPLAY = pygame.display.set_mode((641,641))
pygame.display.set_caption("Battle simulator")
DISPLAY.fill(blue)
pygame.display.flip()
#map constructor
x = 0
y = 0
for i in range(11):
    grid = pygame.draw.line(DISPLAY,BRICK,[x,y],[x,641],1)
    x = x + tilesize
    step = 1
x = 0
y = 0
for i in range(11):
    grid1 = pygame.draw.line(DISPLAY,BRICK,[x,y],[641,y],1)
    y = y + tilesize
pygame.display.flip()    
#draw background###########################
def background():
    DISPLAY.fill(blue)
    pygame.display.flip()
    x = 0
    y = 0
    for i in range(11):
        grid = pygame.draw.line(DISPLAY,BRICK,[x,y],[x,641],1)
        x = x + tilesize
        step = 1
    x = 0
    y = 0
    for i in range(11):
        grid1 = pygame.draw.line(DISPLAY,BRICK,[x,y],[641,y],1)
        y = y + tilesize
    pygame.display.flip()    
    
#-----------------------------------------------
##class unit:
##    def health(self,unit):
##        self.health = health[unit]
##    def defence(self,unit):
##        self.defence = defence[unit] 
##    def attack(self,unit):
##        self.attack = (attack[unit])
##    def damage(self,damage):
##        self.health = (self.health - damage)
##    def attackterrain(self,terrainmodatt):
##        self.attack = (self.attack * terrainmodatt)
##    def defenceterrain(self,terrainmoddef):
##        self.defence = (self.defense * terrainmoddef)


class unit:
    health = 0
    defence = 0
    attack = 0
    xpost = 0
    ypost = 0
    def gethealth(self):
        return self.health
    def getdefence(self):
        return self.defence
    def getxpost(self):
        return (self.x)
    def getypost(self):
        return(self.y)
    #removed as useless
###put these into the initialisation statements for each object 
##    def health(self,unit):#check if these 3 will work as will save a lot of time programming 
##        self.health = health[unit]
##    def defence(self,unit):
##        self.defence = defence[unit] 
##    def attack(self,unit):
##        self.attack = (attack[unit])


#melee cavalry class
class Mcavalry(unit):
    health = health[Mcavalry]
    defence = defence[Mcavalry]
    attack = attack[Mcavalry]
    speed = 70
    ranged = False
    charge = chargemod
    img = pygame.image.load('Mcavalry scaled.PNG')
def __init__(self,unitname,x,y):
    self.health = health
    self.defence = defence
    self.attack = attack
    self.xpost = x
    self.ypost = y
    self.speed = speed
    self.icon = img
    self.range = ranged
    self.charge = charge


#bow cavalry class
class Bcavalry(unit):
    health = 60
    defence = 40
    attack = 8
    speed = 70
    ranged = True
    img = pygame.image.load('Bcavalry scaled.PNG')
def __init__(self,unitname,x,y):
    self.health = health
    self.defence = defence
    self.attack = attack
    self.xpost = x
    self.ypost = y
    self.speed = speed
    self.icon = img
    self.range = ranged      


#class swordsman
class swordsman(unit):
    health = 80
    defence = 60
    attack = 6
    speed = 30
    ranged = False
    img = pygame.image.load('Bcavalry scaled.PNG')
def __init__(self,unitname,x,y):
    self.health = health
    self.defence = defence
    self.attack = attack
    self.xpost = x
    self.ypost = y
    self.speed = speed
    self.icon = img
    self.range = ranged      

   
#----------------------------------------------
    #function to make a numebr positive
def positive(number):
    if number < 0:
        number = (number * -1)
        return number
    else:
        return number
                               
#----game loop#----------
while True:
#highlighting#################################################
    
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    event1 = pygame.event.wait()
    
    if KEYDOWN == False:
        startpost.clear()
        startpost.append(mousex)
        startpost.append(mousey)
        print("run")
    
    if (event1.type == pygame.MOUSEBUTTONDOWN) or ((pygame.mouse.get_pressed()[0])==True):
        endpost.clear()
        endpost.append(mousex)
        endpost.append(mousey)
        #if endpost[1] > startpost[1]:
         #   startpost[1] = endpost[1]
        if (endpost != startpost) and (KEYDOWN == True):
            #pygame.draw.polygon(DISPLAY, BRICK,((startpost[0],startpost[1]),(endpost[0],endpost[1])),5 )
            background()
            pygame.draw.line(DISPLAY,BRICK,[startpost[0],startpost[1]],[endpost[0],startpost[1]],3)
            #line from start to end on the x
            pygame.draw.line(DISPLAY,BRICK,[startpost[0],startpost[1]],[startpost[0],endpost[1]],3)
            #line vertical
            pygame.draw.line(DISPLAY,BRICK,[endpost[0],endpost[1]],[startpost[0],endpost[1]],3)
            #line horizontal from end
            pygame.draw.line(DISPLAY,BRICK,[endpost[0],endpost[1]],[endpost[0],startpost[1]],3)
            pygame.display.flip()
        elif startpost == endpost:
            #time.sleep(0.1)
            KEYDOWN = True
        
    elif event1.type == pygame.MOUSEBUTTONUP:
        KEYDOWN = False
        background()
        pygame.display.flip()
        
    else:
        pass


###########################################################################################################
        
            #check if units are present    
#check is there is a unit on the tile
#def checkunitsposts():
 #   for i in range(len.unitpost):
  #      if mouse_post == unitpost[i]:
   #         unit_ispresent = True
#movement pathfinding algorithm#

#    pygame.init()
 #   screen = pygame.display.set_mode((480, 360))
  #  name = ""
   # font = pygame.font.Font(None, 50)
    #while True:
     #   for evt in pygame.event.get():
      #      if evt.type == KEYDOWN:
       #         if evt.unicode.isalpha():
        #            name += evt.unicode
         #       elif evt.key == K_BACKSPACE:
          #          name = name[:-1]
           #     elif evt.key == K_RETURN:
           #         name = ""
            #elif evt.type == QUIT:
             #   return
#        screen.fill((0, 0, 0))
 #       block = font.render(name, True, (255, 255, 255))
  #      rect = block.get_rect()
   #     rect.center = screen.get_rect().center
    #    screen.blit(block, rect)
     #   pygame.display.flip()  
        
   # while not done:
    #    pygame.time.clock():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
