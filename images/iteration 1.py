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
positive = +1
negative = -1
flat = 1

#list to store units for player, for now the enemy will have the same units, may let them pick in the future
player_army = []
enemy_army = []
#lists to hold the postitions of units in the player arm and in the enemy army
player_armypost = []
player_armyOB = []
enemyy_armypost = []
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
"archer":70,
"pikemen":90,
"catapult":50
}
defence = {
"Mcavalry":50,
"Bcavalry":50,
"swordsman":65,
"archer":45,
"pikemen":70,
"catapult":30
}
attack = {
"Mcavalry":5,
"Bcavalry":8,
"swordsman":6,
"archer":10,
"pikemen":15,
"catapult":20
}
speed = {
"Mcavalry":50,
"Bcavalry":50,
"swordsman":65,
"archer":45,
"pikemen":70,
"catapult":30
}
min_range = {
"Mcavalry":1,
"Bcavalry":2,
"swordsman":1,
"archer":2,
"pikemen":1,
"catapult":3
}
tilesize = 64

################################map classes

#####################maps-add the tilemap strings here###############################
map1 = [["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ]

#to find the tile the unit is on
pygame.init()
DISPLAY = pygame.display.set_mode((641,641))
##pygame.display.set_caption("Battle simulator")
##DISPLAY.fill(blue)
##pygame.display.flip()
###map constructor
##x = 0
##y = 0
##for i in range(11):
##    grid = pygame.draw.line(DISPLAY,BRICK,[x,y],[x,641],1)
##    x = x + tilesize
##    step = 1
##x = 0
##y = 0
##for i in range(11):
##    grid1 = pygame.draw.line(DISPLAY,BRICK,[x,y],[641,y],1)
##    y = y + tilesize
##pygame.display.flip()    
###draw background###########################
##def background():
##    DISPLAY.fill(blue)
##    pygame.display.flip()
##    x = 0
##    y = 0
##    for i in range(11):
##        grid = pygame.draw.line(DISPLAY,BRICK,[x,y],[x,641],1)
##        x = x + tilesize
##        step = 1
##    x = 0
##    y = 0
##    for i in range(11):
##        grid1 = pygame.draw.line(DISPLAY,BRICK,[x,y],[641,y],1)
##        y = y + tilesize
##    pygame.display.flip()    
##    
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
################################map classes
class map:
    Hill = False
    Flat = True
    terraintype = ""
    passable = False
    speedmod = 1
    attmod = 1
    defmod = 1
    xpos = 1
    ypos = 1
    #for simplicity the attack and defence modifiers will be the same for now but may change later
    
##############################################add modifier atibute values here######################################################
                                                                                    #to do~
                                                                                        #-add images to every tile of tilesize
   # def gradientmod(self,terraintype):
        #RETURN gradient MODIFIER FOR THAT SPECIFIC TYPE OF UNIT
    def chargebonus(self,terraintype):
        return self.chargebonus
    def canmove(self,terraintype):
        if self.passable == True:
            return True
        else:
            return False
    def getspeed(self):
        return self.speedmod
    def getdefence(self):
        return self.defmod
    def getx (self):
        return xpos
    def gety (self):
        return self.ypos
    def getterrain(self):
        return self.terraintype


class water(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos

class mountain(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos

class lake(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos


class fjord(map):
    passable = True
    speedmod = 0.6
    attmod = 0.8
    defmod = 1.1
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos


class plains(map):
    passable = True
    speedmod = 1
    attmod = 1
    defmod = 1
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos


class gentleslope(map):
    passable = True
    speedmod = 0.8
    attmod = 0.9
    defmod = 1.2
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos


class steepslope(map):
    passable = True
    speedmod = 0.7
    attmod = 0.7
    defmod = 1.4
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos


class hill(map):
    passable = True
    speedmod = 0.6
    attmod = 0.7
    defmod = 1.6
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
    
#########################################################unit classes
class unit:
    health = 0
    defence = 0
    attack = 0
    xpost = 0
    ypost = 0
    min_range = 0
    def gethealth(self):
        return self.health
    def getdefence(self):
        return self.defence
    def getxpost(self):
        return (self.x)
    def getypost(self):
        return(self.y)
    def updatepost(self,newpostx,newposty):
        xpost = newpostx
        ypost = newposty
    #def movement(self,newpostx,newposty)
        
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
    health = health['Mcavalry']
    defence = defence['Mcavalry']
    attack = attack['Mcavalry']
    speed = speed['Mcavalry']
    min_range = min_range['Mcavalry']
    ranged = False
    charge = chargemod
    img = pygame.image.load('Mcavalry scaled.PNG')
    def __init__(self,unitname,x,y):
        self.icon = pygame.image.load('Mcavalry scaled.PNG')



#bow cavalry class
class Bcavalry(unit):
    health = health['Bcavalry']
    defence = defence['Bcavalry']
    attack = attack['Bcavalry']
    speed = speed['Bcavalry']
    min_range = min_range['Bcavalry']
    ranged = True
    img = pygame.image.load('Bcavalry scaled.PNG')
    def __init__(self,x,y):
        self.icon = pygame.image.load('Bcavalry scaled.PNG')


#class swordsman
class swordsman(unit):
    health = health['swordsman']
    defence = defence['swordsman']
    attack = attack['swordsman']
    speed = speed['swordsman']
    min_range = min_range['swordsman']
    ranged = False
    img = pygame.image.load('Bcavalry scaled.PNG')
    def __init__(self,x,y):
        self.icon = pygame.image.load('Bcavalry scaled.PNG')

#class archer
class archer(unit):
    health = health['archer']
    defence = defence['archer']
    attack = attack['archer']
    speed = speed['archer']
    min_range = min_range['archer']
    ranged = True
    #img = ADD IMAGE HERE
    def __init__(self,unitname,x,y):
        self.icon = img


#class pikemen
class pikemen(unit):
    health = health['pikemen']
    defence = defence['pikemen']
    attack = attack['pikemen']
    speed = speed['pikemen']
    min_range = min_range['pikemen']
    ranged = False
    #img = ADD IMAGE HERE
    def __init__(self,unitname,x,y):
        self.health = health
        self.defence = defence
        self.attack = attack
        self.xpost = x
        self.ypost = y
        self.speed = speed
        self.icon = img
        self.range = ranged
        slef.min_range = min_range

#class catapult
class catapult(unit):
    health = health['catapult']
    defence = defence['catapult']
    attack = attack['catapult']
    speed = speed['catapult']
    min_range = min_range['catapult']
    ranged = True
    #img = ADD IMAGE HERE
    def __init__(self,unitname,x,y):
        self.health = health
        self.defence = defence
        self.attack = attack
        self.xpost = x
        self.ypost = y
        self.speed = speed
        self.icon = img
        self.range = ranged
        self.min_range = min_range

#dictionary for menue, had to be moved outside funtion so it could be accessed for validation

menuemap = {
    1:"Mcavalry",
    2:"Bcavalry",
    3:"swordsman",
    4:"archer",
    5:"pikemen",
    6:"catapult"
}
#units mapped to numbers for the ingame menue
def unitinput(unitchoice):
    print(menuemap.get(int(unitchoice)))
    player_army.append((menuemap.get(int(unitchoice))))
    for i in range (len(player_army)):
        if unitchoice == 1:
            player_armyOB.append(Mcavalry(800,1000))
        elif unitchoice == 2:
            player_armyOB.append(Bcavalry(800,1000))                       
        elif unitchoice ==3:
            player_armyOB.append(swordsman(800,1000))
        elif unitchoice ==4:
            player_armyOB.append(archer(800,1000))
        elif unitchoice ==5:
            player_armyOB.apend(pikemen(800,1000))
        elif unitchoice ==6:
            player_armyOB.append(catapult(800,1000))
# for now the enemy army will mimic the players army but will get 2 more units for the sake of balance                                     
#----------------------------------------------
#function to make a numebr positive
def positive(number):
    if number < 0:
        number = (number * -1)
        return number
    else:
        return number
#before the game loop the player needs to choose their army, done on a cost basis#however for now they will just pick until they have 6 units 
#picking units###########################################################################################
print("Welcome to the battle simulator army picking menue")

done_input = False
counter = 0
while done_input == False:
    unitchoice = input("please enter your unit,1-melee cav,2-bow cav,3-swordsmen,4-archer,5-pikemen,6-catapult")
    if int(unitchoice) in menuemap:
        unitinput(unitchoice)
        counter+=1
    else:
        done_input = False
    if counter == 6:
        done_input = True    
#SCREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEN
pygame.display.set_caption("Battle simulator")
DISPLAY.fill(blue)
pygame.display.flip()
#map constructor, used to draw the grid
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
  


#----game loop#----------
while True:
#highlighting#################################################
    
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    event1 = pygame.event.wait()
    testman = swordsman(2,2)
##    print(testman.attack)
##    DISPLAY.blit(testman.icon,(2,2))
##    testman2 = Bcavalry(66,2)
##    DISPLAY.blit(testman.icon,(66,2))
##    print(testman2.defence)
##    testman2.health = 30
##    print(testman2.health)
##    pygame.display.flip()
    if KEYDOWN == False:
        startpost.clear()
        startpost.append(mousex)
        startpost.append(mousey)
    
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
