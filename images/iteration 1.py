#importing libraries which I will need
import pygame, pygame.font, pygame.event, pygame.draw, string,time,random,concurrent.futures
from math import *
from pygame.locals import*
import time
import math
import threading
import pygame
#colors which I may delete if not used but will keep for now
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
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
#charge constants
chargemod = 1.2
positive = +1
negative = -15
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
        ["F","F","F","F","F","M","W","F","F","F"],
        ["F","F","F","F","F","H","W","F","F","F"],
        ["F","F","F","F","F","F","W","F","F","F"],
        ["F","W","F","L","F","M","FJ","F","W","F"],
        ["F","M","F","F","F","F","F","H","W","F"],
        ["F","FJ","F","F","F","F","F","H","H","F"],
        ["F","F","F","F","F","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","W","F"],
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

#water
class water(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("water texture.PNG")

#mountain
class mountain(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("newmountain texture.PNG")

#lake
class lake(map):
    passable = False
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("lake texture.PNG")

       
#fjord
class fjord(map):
    passable = True
    speedmod = 0.6
    attmod = 0.8
    defmod = 1.1
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("fjord texture.PNG")

#plains
class plains(map):
    passable = True
    speedmod = 1
    attmod = 1
    defmod = 1
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("newflat texture.PNG")

#gentleslope
class gentleslope(map):
    passable = True
    speedmod = 0.8
    attmod = 0.9
    defmod = 1.2
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("gentleslope texture.PNG")

#steepslope
class steepslope(map):
    passable = True
    speedmod = 0.7
    attmod = 0.7
    defmod = 1.4
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("steepslope texture.PNG")

#hill
class hill(map):
    passable = True
    speedmod = 0.6
    attmod = 0.7
    defmod = 1.6
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.img = scale("hill texture.PNG")


#########################################################unit classes
class unit:
    localdestx = 0
    localdesty = 0
    destpostx = 0
    destposty = 0
    #destination for pathfinding 
    #functions output attributes when needed
    def gethealth(self):
        return self.health

    def getdefence(self):
        return self.defence

    def getxpost(self):
        return (int(self.xpost))

    def getypost(self):
        return(int(self.ypost))
    #updates the coordinates
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
        self.xpost = 80
        self.ypost = 250


#class archer
class archer(unit):
    health = health['archer']
    defence = defence['archer']
    attack = attack['archer']
    speed = speed['archer']
    min_range = min_range['archer']
    ranged = True
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
    def __init__(self):
        self.xpost = 350
        self.ypost = 350
        self.icon = scaleunit("catapult.PNG")


#a star class for the node
       
class node():
    impassable = False 
    #occupied by a friend or foe
    friendoc = False
    foeoc = False
    #nodes postition
    xpos = 0
    ypos = 0
    #record parent
    parentx = 0
    parenty = 0
    #tcost- the speed modifier of the terrain type
    tcost = 1
    #gcost-this is the distance from the start postition
    prevg = 0
    gcost = 0
    #f cost-this is the distance left to travel from that node to the end node
    fcost = 0
    #overall cost- this is the total heuristic, found by summing teh g,f and t cost
    H_cost = 0
#updating the distance travelled
    #looks at parent
    #calculates cost to move to the current tile and adds the cost

    def updateH(self):
        self.H_cost = (((self.prevg+(self.gcost*self.tcost)))+(self.fcost))

    def updatetrav(self,startx,starty,prevx,prevy):
        #updates the distance from the destination this is the g cost
        self.prevg = self.gcost
        DISTANCE = positive(positive((((self.xpos//tilesize)+1)-((prevx//tilesize)+1)) + positive(((self.ypos//tilesize)+1)-((prevy//tilesize)+1))))
        self.gcost = DISTANCE


    #updates distance to go
    def updatetogo(self,destx,desty):
        DISTANCE = positive(((positive((destx//tilesize)+1) -((self.xpos//tilesize+1)))) + ((positive((desty//tilesize)+1))-((self.xpos//tilesize)+1)))
        self.fcost = DISTANCE

#updates where the parent node is
    def updateparent (self,px,py):
        if px!=self.parentx:
            self.parentx = px//tilesize
        if py!=self.parenty:
            self.parenty =py//tilesize


#constructor for the node
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
       
#threading class
#class thread(threading.Thread):

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


#lists for movement##########################
InTransit = [1,2,3,4,5,6]
InTransit[0] = [None,0,0,0,0,0,0,0,0]
InTransit[1] = [None,0,0,0,0,0,0,0,0]
InTransit[2] = [None,0,0,0,0,0,0,0,0]
InTransit[3] = [None,0,0,0,0,0,0,0,0]
InTransit[4] = [None,0,0,0,0,0,0,0,0]
InTransit[5] = [None,0,0,0,0,0,0,0,0]
#(unit,currentx,currenty,localx,localy,xspeed,yspeed,destx,dest,y)######
#list of paths for moving
TranditPaths= [None,None,None,None,None,None]

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
#gets an input from the user for what tilesize they want
#menue to select your unit types
menuemap = {
    1:"Mcavalry",
    2:"Bcavalry",
    3:"swordsman",
    4:"archer",
    5:"pikemen",
    6:"catapult"
}
done = False
#visual menue to select your screen size
DISPLAY = pygame.display.set_mode(((500),(500)))
mouse_pos = []





#1st menue
while done == False:
    
    DISPLAY.fill(blue)
    #creates the different pieces of text
    font = pygame.font.Font('freesansbold.ttf', 32)
    text1 = font.render('Small', True, green, blue)
    text2 = font.render('Medium', True, green, blue)
    text3 = font.render('Large', True, green, blue)
    text4 = font.render('Choose a screen size', True, green, blue)
    #rectangles the text will be assigned to 
    textRect1 = text1.get_rect()#s
    textRect2= text2.get_rect()#M
    textRect3 = text3.get_rect()#L
    textRect4 = text4.get_rect()#this is the text at the top
    #setting the postitions of the rectangels of the text
    textRect1.center = (100, 100)
    textRect2.center = (250 , 100)
    textRect3.center = (400, 100)
    textRect4.center = (250, 25)
    #display the text to the display
    DISPLAY.blit(text1, textRect1)
    DISPLAY.blit(text2, textRect2)
    DISPLAY.blit(text3, textRect3)
    DISPLAY.blit(text4, textRect4)
    #creates the buttons
    buttonS = pygame.Rect(75,300,50,50)
    buttonM = pygame.Rect(225,300,50,50)
    buttonL = pygame.Rect(375,300,50,50)
    #draws the buttons 
    pygame.draw.rect(DISPLAY,green,(75,300,50,50))
    pygame.draw.rect(DISPLAY,green,(225,300,50,50))
    pygame.draw.rect(DISPLAY,green,(375,300,50,50))
    pygame.display.update()
    #takes in inputs 
    event = pygame.event.wait()
    #checks what it is and which button has been clicked which sets the tile and unit size
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if buttonS.collidepoint(mouse_pos):
            choice = 1
            tilesize = displaysize.get(choice)
            unitsize = iconsize.get(choice)
            done = True
        elif buttonM.collidepoint(mouse_pos):
            choice = 2
            tilesize = displaysize.get(choice)
            unitsize = iconsize.get(choice)
            done = True
        elif buttonL.collidepoint(mouse_pos):
            choice = 3
            tilesize = displaysize.get(choice)
            unitsize = iconsize.get(choice)
            done = True








#INITIALISING THE LIST OF NODES AND THE MAP OBJECTS#
#it displays the map 
newc = False
ccount = 0
newr = False
row = 0
columb = 0
#list for the initialised map nodes 
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
#nested loop so that the 10 columbs are done and then the loops loves down to the next row
    for j in range (10):
        #each of these if statements will run depending on the piece of text in that postition in the map
            # they will add an initialised objecgt to the map objects list and do the same for a node at the same postition
            #they will then blit the image of that tile at its given coordinates
        landtype = map1[i][j]
        if landtype == "F":
            mapOB[i][j] = plains(columb,row)
            node_list[i][j] = node(columb,row)
            newc = True
            ccount +=1
           
        elif landtype == "H":
            mapOB[i][j] = hill(columb,row)
            node_list[i][j] = node(columb,row)
            newc = True
            ccount +=1
           
        elif landtype == "W":
            mapOB[i][j] = water(columb,row)
            node_list[i][j] = None
            newc = True
            ccount +=1
            impassable.append(mapOB[i][j])

        elif landtype == "M":
            mapOB[i][j] = mountain(columb,row)
            node_list[i][j] = None
            newc = True
            ccount +=1
            impassable.append(mapOB[i][j])

        elif landtype == "FJ":
            mapOB[i][j] = fjord(columb,row)
            node_list[i][j] = node(columb,row)
            newc = True
            ccount +=1
           
        elif landtype == "GS":
            mapOB[i][j] = gentleslope(columb,row)
            node_list[i][j] = node(columb,row)
            newc = True
            ccount +=1
           
        elif landtype == "SS":
            mapOB[i][j] = steepslope(columb,row)
            node_list[i][j] = node(columb,row)
            newc = True
            ccount +=1
           
        elif landtype == "L":
            mapOB[i][j] = lake(columb,row)
            node_list[i][j] = None
            newc = True
            ccount +=1
            impassable.append(mapOB[i][j])
#ensures that it loops the correct number of times
        if ccount == 10:
            newr = True
            columb = 0
            ccount = 0
        if (newc == True) and (ccount != 0):
            columb += tilesize
    if newr == True:
        row+=tilesize



            

#2nd menue
count = 0
done = False
choice = False
while done == False:
    #if no unit is currently selected
    if choice == False:
        DISPLAY = pygame.display.set_mode(((500),(500)))
        DISPLAY.fill(blue)
        #setting the fonts and pieces of text
        font = pygame.font.Font('freesansbold.ttf', 32)
        text0 = font.render('0', True, green, blue)
        text1 = font.render('1', True, green, blue)
        text2 = font.render('2', True, green, blue)
        text3 = font.render('3', True, green, blue)
        text4 = font.render('4', True, green, blue)
        text5 = font.render('5', True, green, blue)
        text6 = font.render('6', True, green, blue)
        heading = font.render('choose your units', True, green, blue)
        #assigning text to rectangles
        textRect0 = text0.get_rect()#0
        textRect1 = text1.get_rect()#1
        textRect2= text2.get_rect()#2
        textRect3 = text3.get_rect()#3
        textRect4 = text4.get_rect()#4
        textRect5 = text5.get_rect()#5
        textRect6= text6.get_rect()#6
        textRect7 = heading.get_rect()#the heading

        #setting the postitions of the rectangles
        textRect0.center = (255, 400)
        textRect1.center = (255 , 400)
        textRect2.center = (255, 400)
        textRect3.center = (255, 400)
        textRect4.center = (255, 400)
        textRect5.center = (255 , 400)
        textRect6.center = (255, 400)
        textRect7.center = (250, 25)#the heading 

        #definingbuttons
        b1 = pygame.Rect(55,335,unitsize,unitsize)
        b2 = pygame.Rect(135,335,unitsize,unitsize)
        b3= pygame.Rect(215,335,unitsize,unitsize)
        b4= pygame.Rect(295,335,unitsize,unitsize)
        b5= pygame.Rect(375,335,unitsize,unitsize)
        b6= pygame.Rect(455,335,unitsize,unitsize)

        #entering the icons for the units
        icon1 =scaleunit('horseman.PNG')
        icon2 =scaleunit('horse archer.PNG')
        icon3 =scaleunit('swordsman.PNG')
        icon4 =scaleunit("archer icon.PNG")
        icon5 =scaleunit("pikeman.PNG")
        icon6 =scaleunit("catapult.PNG")

        #blitting the images to the display
        DISPLAY.blit(icon1,(55,335))
        DISPLAY.blit(icon2,(135,335))
        DISPLAY.blit(icon3,(215,335))
        DISPLAY.blit(icon4,(295,335))
        DISPLAY.blit(icon5,(375,335))
        DISPLAY.blit(icon6,(455,335))
        DISPLAY.blit(heading, textRect7)
        pygame.display.update()

        #the loop will end if 6 units have been selected 
        if count == 6:
            done = True
        event = pygame.event.wait()
        #gets the inputs and checks which button has been pressed, depending on the button it will initialise a unit and add it to the unit list
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if b1.collidepoint(mouse_pos):
                player_armyOB.append(Mcavalry())
                count +=1
                choice = True
            if b2.collidepoint(mouse_pos):
                player_armyOB.append(Bcavalry())
                count +=1
                choice = True
            if b3.collidepoint(mouse_pos):
                player_armyOB.append(swordsman())
                count +=1
                choice = True
            if b4.collidepoint(mouse_pos):
                player_armyOB.append(archer())
                count +=1
                choice = True
            if b5.collidepoint(mouse_pos):
                player_armyOB.append(pikemen())
                count +=1
                choice = True
            if b6.collidepoint(mouse_pos):
                player_armyOB.append(catapult())
                count +=1
                choice = True
                
#if a unit is selcted 
    if choice == True:
        #it displays the map 
        DISPLAY = pygame.display.set_mode(((tilesize*10),(tilesize*10)))
        newc = False
        ccount = 0
        newr = False
        row = 0
        columb = 0

        for i in range (10):
            #nested loop so that the 10 columbs are done and then the loops loves down to the next row
            for j in range (10):
                #each of these if statements will run depending on the piece of text in that postition in the map
                    # they will add an initialised objecgt to the map objects list and do the same for a node at the same postition
                    #they will then blit the image of that tile at its given coordinates
                landtype = map1[i][j]
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
                    impassable.append(mapOB[i][j])

                elif landtype == "M":
                    img = mapOB[i][j]
                    DISPLAY.blit(img.img,(img.xpos,img.ypos))
                    newc = True
                    ccount +=1
                    impassable.append(mapOB[i][j])

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
                    impassable.append(mapOB[i][j])
        #ensures that it loops the correct number of times
                if ccount == 10:
                    newr = True
                    columb = 0
                    ccount = 0
                if (newc == True) and (ccount != 0):
                    columb += tilesize
            if newr == True:
                row+=tilesize
        pygame.display.flip()

    #this then displays the units on the map 
    
        for i in range(len(player_armyOB)):
            icon = player_armyOB[i]
            #displays the corresponding icon of that unit type tot he map at the postitions of the unit
            DISPLAY.blit((icon.icon),((player_armyOB[i].xpost),(player_armyOB[i].ypost)))
            pygame.display.flip()

        location = False
        #if a location on the map hasnt been selected 
        while location == False:
            event = pygame.event.wait()
            #if its a click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                y=mouse_pos[1]
                maxy = tilesize*5
                if y > maxy:#bbelow the y value i.e in the players half of the map
                    x = mouse_pos[0]
                    #sets the x and y coordinates of the unit
                    if node_list[x//tilesize][y//tilesize] != None:
                        
                        if mapOB[y//tilesize][x//tilesize].passable == True:
                            if node_list[x//tilesize][y//tilesize].friendoc == False:
                                player_armyOB[count-1].xpost = (x//tilesize)*tilesize
                                player_armyOB[count-1].ypost = (y//tilesize)*tilesize
                                location = True
                                choice= False
                            else:
                                pass
                    else:
                        print("NOONE")

                
                    
DISPLAY = pygame.display.set_mode(((tilesize*10),(tilesize*10)))                   
#function to make a numebr positive
def positive(number):
    if number < 0:
        number = (number * -1)
        return number
    else:
        return number
done_input = False

#setting the display
pygame.display.set_caption("Battle simulator")



newc = False
ccount = 0
newr = False
row = 0
columb = 0


#DRAWING THE MAP FROM THE TEXT
for i in range (10):
    #nested loop so that the 10 columbs are done and then the loops loves down to the next row
    for j in range (10):
        #each of these if statements will run depending on the piece of text in that postition in the map
            # they will add an initialised objecgt to the map objects list and do the same for a node at the same postition
            #they will then blit the image of that tile at its given coordinates
        landtype = map1[i][j]
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
#ensures that it loops the correct number of times
        if ccount == 10:
            newr = True
            columb = 0
            ccount = 0
        if (newc == True) and (ccount != 0):
            columb += tilesize
    if newr == True:
        row+=tilesize
pygame.display.flip()
         


#setting up the clock
Clock = pygame.time.Clock
clock = Clock()

###################################################################
# a star,#insert error checking so that only coodinates which also have nodes are passed in ie check the pciked location and change to nearest tile if impassabl#need to update nodes beforehand to have h cost for the corect destination  

def astar(destinationx,destinationy,startx,starty):
    lowesttogo = 10000000
    #SETTING THE STARTNODE
    startnode = node_list[(starty//tilesize)][(startx//tilesize)]
    endnode = node_list[destinationy][destinationx]
    #initialising lists to use in the algo
    shortest = 0
    openlist = []
    closedlist = []
    openlist.append(startnode)
    #starting node
    current = startnode
    lowesttogonode = current
    #loops through and sets the destinations of the nodes,this will then be used to calculate the heuristic

   
    found = False
    count = 0
    while found ==False:
        #togo is the distance from that node to the destination
        #isse found openlist is 0 so this loop isnt running, prospective neighbours are not being added

        lowesth =100
        for i in range((len(openlist))):
            if openlist[i].H_cost < lowesth:
                lowesttogonode = openlist[i]
                lowesth = openlist[i].H_cost
        openlist.remove(lowesttogonode)
        current = lowesttogonode

        closedlist.append(current)
        if ((current.xpos//tilesize) == (destinationx)) and ((current.ypos//tilesize) == (destinationy)):
            pathlist = []
            node = endnode
            #need to follow the nodes to append to a list starting at the end
            while node != startnode:
                pathlist.append(current)
                current = node_list[current.parenty][current.parentx]
                node = current
                if node ==startnode:
                    print(pathlist)
                    return True

        else:
            #tested-workds
            x=0
            y=0
            x=(current.xpos)//tilesize
            y=(current.ypos)//tilesize
            #find each neighbour of the current
            xrows = current.xpos//tilesize
            yrows = current.ypos//tilesize
            listofneighbours = []
            #finding neighbours
            left = True
            right = True
            top = True                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            below = True
            if xrows ==0:
                left = False
            if xrows == 9:
                right = False
            if yrows == 0:
                top = False
            if yrows == 9:
                below = False
                #l
            if left == True:
                listofneighbours.append(node_list[(y)][(x-1)])
                #ld
            if (left == True) and (below ==True):
                listofneighbours.append(node_list[(y+1)][(x-1)])
                #d
            if below == True:
                listofneighbours.append(node_list[(y+1)][(x)])
                #dr
            if (below == True)and(right == True):
                listofneighbours.append(node_list[(y+1)][(x+1)])
                #r
            if right == True:
                listofneighbours.append(node_list[(y)][(x+1)])
                #rt
            if (right ==True )and(top == True):
                listofneighbours.append(node_list[(y-1)][(x+1)])
                #t
            if top == True:
                listofneighbours.append(node_list[(y-1)][(x)])
                #tl
            if (top==True)and(left==True):
                listofneighbours.append(node_list[(y-1)][(x-1)])

#using while loops to loop through the lists and remove elements, cant use for as the length of the list changes
            #removes nodes which are none
            #removes nodes in openlist and closed list to prevent duplicates
            listtodelete = []
            for i in range(len(listofneighbours)):
                if listofneighbours[i] == None:
                    listtodelete.append(listofneighbours[i])
                for k in range(len(closedlist)):
                    if closedlist[k] == listofneighbours[i]:
                        listtodelete.append(listofneighbours[i])
                for k in range(len(openlist)):
                    if listofneighbours[i] == openlist[k]:
                        listtodelete.append(listofneighbours[i])

            templist = [x for x in listofneighbours if x not in (listtodelete)]
            listofneighbours = templist


    #set the f cost
    #set the parent of this node to current
    #if neighbour is not in open then add to open
#check if the new path is shorter
            for i in range (len(listofneighbours)):
                listofneighbours[i].updatetrav(startnode.xpos,startnode.ypos,current.xpos,current.ypos)
                listofneighbours[i].updatetogo(destinationx,destinationy)
                listofneighbours[i].updateparent(current.xpos,current.ypos)
                listofneighbours[i].tcost = (mapOB[current.ypos//tilesize][current.xpos//tilesize]).speedmod
                listofneighbours[i].updateH()
                #now i have the list of valid neighbours and will pick the best option
                openlist.append(listofneighbours[i])




#take the destinations and the unit  being moved
def move(x,y,unit):
    #the x and y are the targets for the unit to move to ]
    #the unit should be the head unit in the columb or the only unit

    if tilesize ==64:
        pixelmod = 1
    elif tilesize == 72:
        pixelmod = 1.125
    elif tilesize == 96:
        pixelmod =1.5

   
    while done == False:
        if (unit.xpost ==((x*tilesize)+(0.5*tilesize))) and ((unit.ypost) == ((y*tilesize)+(0.5*tilesize))):
            done = True
        else:#setting the speed, this has to be redone each loop due to terrian costs
            speed = unit.speed
            xindex = (x//tilesize)
            yindex = (x//tilesize)
            mapmod = mapOB[xindex,yindex].speedmod
            unitspeed = ((speed * mapmod) *pixelmod)
            done = False
            currentnode = node_list[xindex][yindex]
            #getting the next node, looking at child of current node
            nextNodex = currentnode.childx
            nextNodey = currentnode.childy
            #pick the  direction direction to move in
           
            if (nextNodex  >= unit.xpost):
                directionxmod = 1

            elif ((nextNodex<= unit.xpost)):
                directionxmod = -1

            if nextNodey >= unit.ypost :
                directionymod = 1

            elif nextNodey <= unit.ypost:
                directionymod = -1
            print("chosen direction" & directionymod)

            unitspeedx = unitspeed * directionxmod
            unitspeedy = unitspeed* directionymod
            print("move")
            time.sleep(0.01)                                                                                                                                  
            unit.xpost = (unit.xpost + unitspeedx)
            unit.ypost = (unit.ypost+unitspeedy)
    if done == True:
        return None






#----game loop#----------
while True:
    #this ensures the loop only runs 60 times per second
    clock.tick_busy_loop(60)

# redrawing the background image
#same loop as earlier but removed everything which initialised an object this just reads the map and then blits the images to the screen
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
   
    #loops by the number of uits chosen by the player, fixed for now
    for i in range(len(player_armyOB)):
        icon = player_armyOB[i]
    #displays the corresponding icon of that unit type tot he map at the postitions of the unit
        DISPLAY.blit((icon.icon),((player_armyOB[i].xpost),(player_armyOB[i].ypost)))
        pygame.display.flip()

#highlighting#################################################
    #gets the mouse postitions
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    #gets an event
    event1 = pygame.event.poll()
    #check what the event is

    #this clears the held information as the button has been released so the highlight is complete
    if KEYDOWN == False:
        startpost.clear()
        startpost.append(mousex)
        startpost.append(mousey)
   
    pygame.event.poll()
#if the mouse is clicked or is held down then th code to highlight the units and draw a corresponding square on the map runs
    if  ((pygame.mouse.get_pressed()[0])==True):#(event1.type == pygame.MOUSEBUTTONDOWN) or----removed code
    #the start is immedietely stored and now the end is stored and refreshed as long as left mouse button is held
        endpost.clear()
        endpost.append(mousex)
        endpost.append(mousey)
        player_armyhighlight = []    
       
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
                 
                   
        #this draws the highlight square but only if the mouse has actually moved
        if (endpost != startpost) :#and (KEYDOWN == True):

            pygame.draw.line(DISPLAY,BRICK,[startpost[0],startpost[1]],[endpost[0],startpost[1]],3)
            #line from start to end on the x
            pygame.draw.line(DISPLAY,BRICK,[startpost[0],startpost[1]],[startpost[0],endpost[1]],3)
            #line vertical
            pygame.draw.line(DISPLAY,BRICK,[endpost[0],endpost[1]],[startpost[0],endpost[1]],3)
            #line horizontal from end
            pygame.draw.line(DISPLAY,BRICK,[endpost[0],endpost[1]],[endpost[0],startpost[1]],3)
            pygame.display.flip()

                   
            #checking if the unit is within the range
            for i in range (len(player_armyOB)):
                #shows that this loop does run 6 times
                #checks if its in the x range
                if ((player_armyOB[i].getxpost()) >= lowerxbound) and ((player_armyOB[i].getxpost()) <= upperxbound):
                    #only checks y if its within the x range to minimise the number of checks run
                    #checks the y range
                    if ((player_armyOB[i].getypost()) >= lowerybound) and ((player_armyOB[i].getypost()) <= upperybound):
                        #adds the unit to a list of highlighted units
                        player_armyhighlight.append(player_armyOB[i])
                        #runs the highlight function which is held in the class definition for the units
                        player_armyOB[i].highlight()
                        #redrawing the units over the highlight square
                        icon = player_armyOB[i]
                        DISPLAY.blit((icon.icon),((player_armyOB[i].xpost),(player_armyOB[i].ypost)))
                        pygame.display.flip()

        #if the startpost and he endpost are the same then the mouse hasnt moved so nothing new needs to be drawn
        elif startpost == endpost:
            #time.sleep(0.1)
            KEYDOWN = True
           # player_armyhighlight = []
    #if the event is a right click instead then it means that rather than highlghting that a destination for mvement is being set or a target if its an enemy unit    
    elif event1.type == pygame.MOUSEBUTTONUP:
        KEYDOWN = False
        #background()
        pygame.display.flip()
           
    elif (pygame.mouse.get_pressed()[2])==True:  
        #sets the destination coordinated
        destination = []
        #destination.clear()
        #destination.append(mousex)
        #destination.append(mousey)
        #rounds the destination coordinates to a specific tile index
        destinationxcords = (mousex//tilesize)
        destinationycords = (mousey//tilesize)

        


    ###################################################################
    #picking destinations for units
    #loop by number of units higlighted and append the desstinations to a list then assign a destination to each unit in order of the units speed
        spacesneeded = len(player_armyhighlight)
        destx = destinationxcords//tilesize
        desty = destinationycords//tilesize
        listofdests = []
        initial = mapOB[destx][desty]
        current = initial

        for i in range (spacesneeded):
            if i == 0:
                if current.passable == True:
                   listofdests.append[current]
            if i == 1:
                current = mapOB[(destx-1)][desty]
                if current.passable == True:
                    listofdests.append[current]
            if i == 2:
                current = mapOB[(destx-1)][(desty-1)]
                if current.passable ==True:
                    listofdests.append[current]
            if i ==3:
                current = mapOB[destx][(desty-1)]
                if current.passable ==True:
                    listofdests.append[current]
            if i ==4:
                current = mapOB[(destx+1)][desty]
                if current.passable ==True:
                    listofdests.append[current]
            if i == 5:
                current = mapOB[(destx+1)][(desty+1)]
                if current.passable ==True:
                    listofdests.append[current]
        if ((len(player_armyhighlight))) == 1:
            path = astar(destinationxcords,destinationycords,player_armyhighlight[0].xpost,player_armyhighlight[0].ypost)
            #movement = move(destination[0],destination[1],player_armyhighlight[0].xpost,player_armyhighlight[0].ypost)
            print("path has been found")
            pass
        print (path)

#MOVEMENT FUNCTION PLAN

##########################################################################   A STAR####################################
#movement function will be a modified version of a star with localised checks

##    if __name == "__main__":
##        format = "%(asctime)s: %(message)s"
##        logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
##        with concurrent.futures.ThreadPoolExecuter(max_workers=6)as executer:
##            for index in range(6):
##                
##      

###########################################################################################################
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True



	
