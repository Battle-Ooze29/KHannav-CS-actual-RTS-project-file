import pygame, pygame.font, pygame.event, pygame.draw, string,time,random
from math import *
from pygame.locals import*
import time
import math
import threading
import pygame
WHITE=(255,255,255)
blue=(0,0,255)
lblue=(0,255,255)
BRICK=(255, 51, 0)
BLACK=(0,0,0)
ugreen=(0,255,0)
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
#list of impassale tiles
impassable = []
#list to store units for player, for now the enemy will have the same units, may let them pick in the future
player_army = []
enemy_army = []
#lists to hold the postitions of units in the player arm and in the enemy army

player_armyhighlight = []
player_armyOB = []

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
"Mcavalry":10,
"Bcavalry":10,
"swordsman":5,
"archer":5,
"pikemen":5,
"catapult":4
}
min_range = {
"Mcavalry":1,
"Bcavalry":2,
"swordsman":1,
"archer":2,
"pikemen":1,
"catapult":3
}

################################map classes

#####################maps-add the tilemap strings here###############################
map1 = [["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","L","F","M","FJ","F","W","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ]



#postitioning functiont
def postition(x,y):
    #x
    xend =((x%tilesize)*(tilesize)) +(0.5*tilesize)
    yend = ((y%tilesize)*(tilesize)) +(0.5*tilesize)
    return(xend,yend)

pygame.init()



#########################FUNCTION TO SCALE MAP IMAGES ###############
def scale(img):
    picture = pygame.image.load(img)
    picture = pygame.transform.scale(picture,(tilesize,tilesize))
    return picture

######################to scale units###################
def scaleunit(img):
    picture = pygame.image.load(img)
    #each icon will take up a 2 thirds of the tile its on and should be centred#########
    picture = pygame.transform.scale(picture,(unitsize,unitsize))
    return picture


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
        self.img = scale("water texture.PNG")


class mountain(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("newmountain texture.PNG")


class lake(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("lake texture.PNG")

        

class fjord(map):
    passable = True
    speedmod = 0.6
    attmod = 0.8
    defmod = 1.1
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("fjord texture.PNG")


class plains(map):
    passable = True
    speedmod = 1
    attmod = 1
    defmod = 1
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("newflat texture.PNG")


class gentleslope(map):
    passable = True
    speedmod = 0.8
    attmod = 0.9
    defmod = 1.2
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("gentleslope texture.PNG")


class steepslope(map):
    passable = True
    speedmod = 0.7
    attmod = 0.7
    defmod = 1.4
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("steepslope texture.PNG")


class hill(map):
    passable = True
    speedmod = 0.6
    attmod = 0.7
    defmod = 1.6
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("hill texture.PNG")



###################################################################

#########################################################unit classes
class unit:
##    health = 0
##    defence = 0
##    attack = 0
##    xpost = 0
##    ypost = 0
##    min_range = 0

    def gethealth(self):
        return self.health

    def getdefence(self):
        return self.defence

    def getxpost(self):
        return (int(self.xpost))

    def getypost(self):
        return(int(self.ypost))

    def updatepost(self,newpostx,newposty):
        xpost = newpostx
        ypost = newposty

    def highlight(self):
        x = (self.xpost -2 )
        y = (self.ypost + 2 )
        #change to lines or mod calculations before you draw
        pygame.draw.rect(DISPLAY,WHITE,(x,y,(unitsize+2),(unitsize+2)))
        pygame.display.flip()
    #def movement(self,newpostx,newposty)
        
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
    def __init__(self):
        self.icon = scaleunit('horseman.PNG')
        self.xpost = 150
        self.ypost = 150


#bow cavalry class
class Bcavalry(unit):
    health = health['Bcavalry']
    defence = defence['Bcavalry']
    attack = attack['Bcavalry']
    speed = speed['Bcavalry']
    min_range = min_range['Bcavalry']
    ranged = True
    img = pygame.image.load('Bcavalry scaled.PNG')
    def __init__(self):
        self.icon = scaleunit('horse archer.PNG')
        self.xpost = 100
        self.ypost = 100


#class swordsman
class swordsman(unit):
    health = health['swordsman']
    defence = defence['swordsman']
    attack = attack['swordsman']
    speed = speed['swordsman']
    min_range = min_range['swordsman']
    ranged = False
    img = pygame.image.load('swordsman.PNG')
    icon = 0
    def __init__(self):
        self.icon = scaleunit('swordsman.PNG')
        self.xpost = 50
        self.ypost = 50


#class archer
class archer(unit):
    health = health['archer']
    defence = defence['archer']
    attack = attack['archer']
    speed = speed['archer']
    min_range = min_range['archer']
    ranged = True
    #img = ADD IMAGE HERE
    def __init__(self):
        self.icon = scaleunit("archer icon.PNG")
        self.xpost = 200
        self.ypost = 200     


#class pikemen
class pikemen(unit):
    health = health['pikemen']
    defence = defence['pikemen']
    attack = attack['pikemen']
    speed = speed['pikemen']
    min_range = min_range['pikemen']
    ranged = False
    #img = ADD IMAGE HERE
    def __init__(self):        
        self.xpost = 300
        self.ypost = 300
        self.icon = scaleunit("pikeman.PNG")


#class catapult
class catapult(unit):
    health = health['catapult']
    defence = defence['catapult']
    attack = attack['catapult']
    speed = speed['catapult']
    min_range = min_range['catapult']
    ranged = True
    #img = ADD IMAGE HERE
    def __init__(self):
        self.xpost = 350
        self.ypost = 350
        self.icon = scaleunit("catapult.PNG")


#a star class for the node
        
class node():
    #occupied by a friend or foe
    friendoc = False
    foeoc = False
    #nodes postition
    xpos = 0
    ypos = 0
    #record parent
    parentx = 0
    parenty = 0
    #gcost
    distance_travelled = 0
    #f cost
    distance_togo = 0#heuristic cost
    H_cost = (distance_travelled + distance_togo)

    def updatetrav(self,parentx,parenty):
        if (parentx != self.xpos) and (parenty != self.ypost):
            dist = 14
        else:
            dist = 10
        travelled = self.distance_travelled + dist
        return travelled

    def updatetogo(self,destx,desty):
        DISTANCE = (((destx -self.xpost)**2) + (desty-self.ypost)**2)
        DISTANCE = int(round(DISTANCE**0.5))
        return DISTANCE
    def __init__(self,xpost,ypost):
        self.xpos = xpost
        self.ypos = ypost
        self.distance_travelled = 0
        
    
    
    

#function to round the tilenumber to the nearest tile
def tileround(x,tilesize):
    if (x>((x//tilesize)*tilesize)+(0.5*tilesize)):
        tilepost = ((x//tilesize)+1)
    else:
        x<((x//tilesize)*tilesize)+(0.5*tilesize)
        tilepost = (x//tilesize)
    return tilepost
        
        
        
    
#randomiser to make combat more indicidualised


def randomdmg():
    randmap = {
        1:0.6,
        2:0.8,
        3:1,
        4:1.2,
        5:1.4
        }
    random = random.randint(1,6)
    modifier = randmap.get(random)
    return modifier


###############choosing your screensize################
displaysize = {
1:64,
2:72,
3:96
}
####different sizes of icons corresponding to the tilesizes###
iconsize = {
1:38,
2:44,
3:58
}
sizechoice = input("enter 1 for small, 2 for medium and 3 for a large display")
done = False
while not done:
    if int(sizechoice) in displaysize:
        choice = int(sizechoice)
        tilesize = displaysize.get(choice)
        print(tilesize)
        unitsize = iconsize.get(choice)
        print(unitsize)
        DISPLAY = pygame.display.set_mode(((tilesize*10),(tilesize*10)))
        done = True


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
    unitchoice = int(unitchoice)
    print(menuemap.get(int(unitchoice)))
    player_army.append((menuemap.get(int(unitchoice))))
    if unitchoice == 1:
        player_armyOB.append(Mcavalry())
    elif unitchoice == 2:
        player_armyOB.append(Bcavalry())                       
    elif unitchoice ==3:
        player_armyOB.append(swordsman())
    elif unitchoice ==4:
        player_armyOB.append(archer())
    elif unitchoice ==5:
        player_armyOB.append(pikemen())
    elif unitchoice ==6:
        player_armyOB.append(catapult())

        


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


#setting the display
pygame.display.set_caption("Battle simulator")


#where the initialised map will be stored
mapOB = [[None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         ]
         

#initialising the map
newc = False
ccount = 0
newr = False
row = 0
columb = 0
#list of nodes for a star
node_list = [[None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         [None,None,None,None,None,None,None,None,None,None],
         ]
         
for i in range (10):

    for j in range (10):
        landtype = map1[i][j]#change map1 to mapchoice once the power to select a map is added
        if landtype == "F":
            mapOB[i][j] = plains(columb,row)
            node_list[i][j] = node(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "H":
            mapOB[i][j] = hill(columb,row)
            node_list[i][j] = node(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "W":
            mapOB[i][j] = water(columb,row)
            node_list[i][j] = None
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            impassable.append(mapOB[i][j])

        elif landtype == "M":
            mapOB[i][j] = mountain(columb,row)
            node_list[i][j] = None
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            impassable.append(mapOB[i][j])

        elif landtype == "FJ":
            mapOB[i][j] = fjord(columb,row)
            img = mapOB[i][j]
            node_list[i][j] = node(columb,row)
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "GS":
            mapOB[i][j] = gentleslope(columb,row)
            img = mapOB[i][j]
            node_list[i][j] = node(columb,row)
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "SS":
            mapOB[i][j] = steepslope(columb,row)
            img = mapOB[i][j]
            node_list[i][j] = node(columb,row)
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "L":
            mapOB[i][j] = lake(columb,row)
            node_list[i][j] = None
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            impassable.append(mapOB[i][j])

        if ccount == 10:
            newr = True
            columb = 0
            ccount = 0
        if (newc == True) and (ccount != 0):
            columb += tilesize
    if newr == True:
        row+=tilesize
pygame.display.flip()
          

    


#displaying the map


#----game loop#----------
while True:

# redrawing the background image
    newc = False
    ccount = 0
    newr = False
    row = 0
    columb = 0
    for i in range (10):

        for j in range (10):
            landtype = map1[i][j]#change map1 to mapchoice once the power to select a map is added
            if landtype == "F":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "H":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "W":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "M":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "FJ":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "GS":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "SS":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            elif landtype == "L":
                img = mapOB[i][j]
                DISPLAY.blit(img.img,(img.xpos,img.ypos))
                newc = True
                ccount +=1
                
            if ccount == 10:
                newr = True
                columb = 0
                ccount = 0
            if (newc == True) and (ccount != 0):
                columb += tilesize
        if newr == True:
            row+=tilesize
            
    pygame.display.flip()

    #drawing icons
    
    for i in range(len(player_armyOB)):
        icon = player_armyOB[i]

        DISPLAY.blit((icon.icon),((player_armyOB[i].xpost),(player_armyOB[i].ypost)))
        pygame.display.flip()

#highlighting#################################################
    
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    event1 = pygame.event.poll()

    if KEYDOWN == False:
        startpost.clear()
        startpost.append(mousex)
        startpost.append(mousey)
    pygame.event.poll()
    if (event1.type == pygame.MOUSEBUTTONDOWN) or ((pygame.mouse.get_pressed()[0])==True):
        endpost.clear()
        endpost.append(mousex)
        endpost.append(mousey)
        
        ######checking if a unit is within the higlighted square
        #establish a range within to check

  
        if startpost[0] <= endpost[0]:
            lowerxbound = startpost[0]
            upperxbound = endpost[0]

        else:
            lowerxbound = endpost[0]
            upperxbound =  startpost[0]

        if startpost[1] <= endpost[1]:      
            lowerybound = startpost[1]
            upperybound = endpost[1]

        else:
            lowerybound = endpost[1]
            upperybound = startpost[1]
                 
                    
        #if endpost[1] > startpost[1]:
         #   startpost[1] = endpost[1]
        if (endpost != startpost) and (KEYDOWN == True):

            pygame.draw.line(DISPLAY,BRICK,[startpost[0],startpost[1]],[endpost[0],startpost[1]],3)
            #line from start to end on the x
            pygame.draw.line(DISPLAY,BRICK,[startpost[0],startpost[1]],[startpost[0],endpost[1]],3)
            #line vertical
            pygame.draw.line(DISPLAY,BRICK,[endpost[0],endpost[1]],[startpost[0],endpost[1]],3)
            #line horizontal from end
            pygame.draw.line(DISPLAY,BRICK,[endpost[0],endpost[1]],[endpost[0],startpost[1]],3)
            pygame.display.flip()

                    #check x

            for i in range (len(player_armyOB)):

                if ((player_armyOB[i].getxpost()) >= lowerxbound) and ((player_armyOB[i].getxpost()) <= upperxbound):

                    #check y
                    if ((player_armyOB[i].getypost()) >= lowerybound) and ((player_armyOB[i].getypost()) <= upperybound):

                        player_armyhighlight.append(player_armyOB[i])
                        player_armyOB[i].highlight()
#redrawing
                        icon = player_armyOB[i]
                        DISPLAY.blit((icon.icon),((player_armyOB[i].xpost),(player_armyOB[i].ypost)))
                        pygame.display.flip()


        elif startpost == endpost:
            #time.sleep(0.1)
            KEYDOWN = True
    
    elif event1.type == pygame.MOUSEBUTTONUP:
        KEYDOWN = False
        #background()
        pygame.display.flip()
            
    else:
        pass

    if (pygame.mouse.get_pressed()[2])==True:
        destination = []
        destination.clear()
        destination.append(mousex)
        destination.append(mousey)
        #need to -1 to use these as index values
        destinationxcords = destination[0]//tilesize
        destinationycords = destination[1]//tilesize
        #grouping units for movement
        formcolumb = False
        if (len(player_armyhighlight)) >= 2:
            formcolumb = True
        else:
            formcolumb = False
        if formcolumb == True:
        #search within the cords for units within 2 tiles 
            #sort using bubble sort by speed
            #bubble sort function modified to compare speeds 

            xmin = 0
            xmax = 0
            ymin = 0
            ymax = 0
            n = len(player_armyhighlight)
         
            # Traverse through all array elements
            for i in range(n-2):
                #use to loop to fin the x and y point to form a columb on 
                if (player_armyhighlight[i].xpost//tilesize) <= xmin:
                    xmin = (player_armyhighlight[i].xpost//tilesize)

                elif (player_armyhighlight[i].xpost//tilesize) >= xmax:
                    xmax = player_armyhighlight[i].xpost//tilesize

                if (player_armyhighlight[i].ypost//tilesize) <= ymin:
                    ymin = player_armyhighlight[i].ypost//tilesize

                elif (player_armyhighlight[i].ypost//tilesize) >= ymax:
                    ymax = (player_armyhighlight[i].ypost//tilesize)
         
                # Last i elements are already in place
         
                if ((player_armyhighlight[i].speed) >= (player_armyhighlight[i+1].speed)) :
                    temp = player_armyhighlight.pop(i) 
                    #player_armyhighlight.insert(i,player_armyhighlight[i+1])
                    player_armyhighlight.insert((i+1),temp)
            #now that they are sorted move the units into a columb 
            #picking the head point of the columb
            xmid = int(round((xmax-xmin)/2))
            ymid= int(round((ymax-ymin)/2))
            columbx = (xmid*tilesize)+(0.5*tilesize)
            columby = (ymid*tilesize)+(0.5*tilesize)
            print("columb")
#            for i in range(len(player_armyhighlight)):
##########################################################################   A STAR####################################

            
        #movement code
##def move(x,y,unit):
##    #the x and y are the targets for the unit to move to ]
##    #the unit should be the head unit in the columb or the only unit
##
##    if tilesize ==64:
##        pixelmod = 1
##    elif tilesize == 72:
##        pixelmod = 1.125
##    elif tilesize == 96:
##        pixelmod =1.5
##
##    speed = unit.speed
##    xindex = (x//tilesize)
##    yindex = (x//tilesize)
##    mapmod = mapOB[xindex,yindex].speedmod
##    unitspeed = ((speed * mapmod) *pixelmod)
##    done = False
##    #pick the direction to move in
##
##    if (x  >= unit.xpost):
##        directionxmod = 1
##
##    elif ((x<= unit.xpost)):
##        directionxmod = -1
##
##    if y >= unit.ypost :
##        directionymod = 1
##
##    elif y <= unit.ypost:
##        directionymod = -1
##    print("chosen direction" & directionymod)
##
##    unitspeedx = unitspeed * directionxmod
##    unitspeedy = unitspeed* directionymod
##    
##    while done == False:
##        if (unit.xpost ==((x*tilesize)+(0.5*tilesize))) and ((unit.ypost) == ((y*tilesize)+(0.5*tilesize))):
##            done = True
##        print("move")
##        time.sleep(0.01)
##        unit.xpost = (unit.xpost + unitspeedx)
##        unit.ypost = (unit.ypost+unitspeedy)
###multithreading#moving into the columb


#movement function will be a modified version of a star with localised checks 



###################################################################
# a star,#insert error checking so that only coodinates which also have nodes are passed in ie check the pciked location and change to nearest tile if impassabl#need to update nodes beforehand to have h cost for the corect destination  
def astar(destinationx,destinationy,startx,starty):

    #loop sets the destinations of the nodes 
    endnode = (destinationx,destinationy)
    for i in range(len(node_list)):
        if node_list[i] == None:
            pass
        else:
            node_list[i].updatetogo(destinationx,destinationy)            

    openlist = []
    closedlist = []
    startnode = node_list((startx//tilesize),(starty//tilesize))
    found = False
    count = 0
    openlist.append(startnode)
    
    while found ==False:
        for i in range(len(openlist)):
            lowestfnode = []
            lowestf = 0
            if openlist[i].H_cost <= lowestf:
                lowestfnode = openlist[i]
                lowestf = openlist[i].H_cost
        current = lowestfnode
        openlist.remove(current)
        closedlist.append(current)
        
        if (current.xpos == destinationx) and (current.ypos == destinationy) :
            found = True
            
        x=current.xpos//tilesize
        y=current.ypos//tilesize
        #find each neighbour of the current
        xrows = current.xpos//tilesize
        yrows = current.ypos//tilesize
        listofneighbours = []
        left = True
        right = True
        top = True
        below = True
        if xrows ==0:
            left = False
        elif xrows == 10:
            right = False
        elif yrows == 0:
            top = False
        elif yrows == 10:
            below = False
            #l
        if left == True:
            listofneighbours.append(node[(y)][(x-1)])
            #ld
        if (left == True) and (below ==True):
            listofneighbours.append(node[(y+1)][(x-1)])
            #d
        if below == True:
            listofneighbours.append(node[(y+1)][(x)])
            #dr
        if (below == True)and(right == True):
            listofneighbours.append(node[(y+1)][(x+1)])
            #r
        if right == True:
            listofneighbours.append(node[(y)][(x+1)])
            #rt
        if (right ==True )and(top == True):
            listofneighbours.append(node[(y-1)][(x+1)])
            #t
        if top == True:
            listofneighbours.append(node[(y-1)][(x)])
            #tl
        if (top==True)and(left==True):
            listofneighbours.append(node[(y-1)][(x-1)])

        for i in range(len(listofneighbours)):
            
            pass
        
           
            
            
            
            
            
        
     
    
        
                
###########################################################################################################
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
