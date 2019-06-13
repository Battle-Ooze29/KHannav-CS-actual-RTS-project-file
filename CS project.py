import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import*
WHITE=(255,255,255)
blue=(0,0,255)
lblue=(0,255,255)
BRICK=(255, 51, 0)
BLACK=(0,0,0)
green=(0,255,0)
YELLOW = (255,255,0)
GREY = (128,128,128)
dmg = 0
healthmod
unit = [Mcavalry,Bcavalry,swordsman,archers,pikemen,catapult]
terrain = [positive,negative,flat]
Player1units =[]
Player2units=[]
#unit properties
health = {
"Mcavalry":75,
"Bcavalry":75,
"swordsman":90,
"archers":70,
"pikemen":90,
"catapult":50
}
defence = {
"Mcavalry":50,
"Bcavalry":50,
"swordsman":65,
"archers":45,
"pikemen":70,
"catapult":30
}
#to find the gradie
pygame.init()

DISPLAY = pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption("Battle simulator")
#class declarations
done = False
class terrain(pygame.sprite.Sprite):
    def__init__(self,x,y,tile):
        pygame.sprite.Sprite.__init__(self);
        self.
class water(terrain):
    self.passable = False
    self.gradient = 0
    self.icon = #insert icon here
    def getpass:
        return passable
    def getgrad:
        return self.gradient
class hill(terrain):
    self.passable = True
    self.gradient = 1
    self.icon = #insert icon
    def getpass:
        return passable
    def getgrad:
        return self.gradient
class flatland(terrain):
    self.passable = True
    self.gradient = 0.0001
    self.icon = #insert icon
    def getpass:
        return passable
    def getgrad:
        return self.gradient
    
#-----------------------------------------------
class unit:
    def health(self,unit):
        self.health = health[unit]
    def defence(self,unit):
        self.defence = defence[unit] 
    def attack(self,unit):
        self.attack = (attack[unit])
    def damage(self,damage):
        self.health = (self.health - damage)
    def attackterrain(self,terrainmodatt):
        self.attack = (self.attack * terrainmodatt)
    def defenceterrain(self,terrainmoddef):
        self.defence = (self.defense * terrainmoddef)
    def gethealth(self):
        return self.health
    def getdefence(self):
        return self.defence
#----------------------------------------------
    
def name():
    pygame.init()
    screen = pygame.display.set_mode((480, 360))
    name = ""
    font = pygame.font.Font(None, 50)
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                    name = ""
            elif evt.type == QUIT:
                return
        screen.fill((0, 0, 0))
        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()  
        
   # while not done:
    #    pygame.time.clock():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    
        
