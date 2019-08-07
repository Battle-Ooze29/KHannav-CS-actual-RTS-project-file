import pygame, pygame.font, pygame.event, pygame.draw, string,time
from pygame.locals import*
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


#to find the tile the unit is on
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
        x = (self.xpost + 10)
        y = (self.ypost - 10)
        #change to lines or mod calculations before you draw
        pygame.draw.rect(DISPLAY,WHITE,(x,y,30,30))
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
        player_armyOB.apend(pikemen())
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
for i in range (10):

    for j in range (10):
        landtype = map1[i][j]#change map1 to mapchoice once the power to select a map is added
        if landtype == "F":
            mapOB[i][j] = plains(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "H":
            mapOB[i][j] = hill(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "W":
            mapOB[i][j] = water(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "M":
            mapOB[i][j] = mountain(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "FJ":
            mapOB[i][j] = fjord(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "GS":
            mapOB[i][j] = gentleslope(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "SS":
            mapOB[i][j] = steepslope(columb,row)
            img = mapOB[i][j]
            DISPLAY.blit(img.img,(img.xpos,img.ypos))
            newc = True
            ccount +=1
            
        elif landtype == "L":
            mapOB[i][j] = lake(columb,row)
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
#highlighting#################################################
    
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    event1 = pygame.event.wait()

    if KEYDOWN == False:
        startpost.clear()
        startpost.append(mousex)
        startpost.append(mousey)
    pygame.event.get()
    if (event1.type == pygame.MOUSEBUTTONDOWN) or ((pygame.mouse.get_pressed()[0])==True):
        endpost.clear()
        endpost.append(mousex)
        endpost.append(mousey)
        print(player_armyOB[1].getxpost())
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

        #check x

        for i in range (int(len(player_armyOB))-1):
            print(len(player_armyOB))
            if ((player_armyOB[i].getxpost()) >= lowerxbound) and ((player_armyOB[i].getxpost()) <= upperxbound):
                print("work")
                #check y
                if ((player_armyOB[i].getypost()) >= lowerybound) and ((player_armyOB[i].getypost()) <= upperybound):
                    print("valid")
                    player_armyhighlight.append(player_armyOB[i])
                    player_armyOB[i].highlight()
                else:
                    pass
            else:
                pass


                 
                    
        #if endpost[1] > startpost[1]:
         #   startpost[1] = endpost[1]
        if (endpost != startpost) and (KEYDOWN == True):
            #pygame.draw.polygon(DISPLAY, BRICK,((startpost[0],startpost[1]),(endpost[0],endpost[1])),5 )
            #background()
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
        #background()
        pygame.display.flip()
            
    else:
        pass


###########################################################################################################
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
