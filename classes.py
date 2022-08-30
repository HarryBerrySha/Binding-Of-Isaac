from view import *
import random, math


class room:
    def __init__(self, x, y, monsters, objects, isTreasureRoom, isStartRoom, isBossRoom):
        self.x = x
        self.y = y
        self.monsters = monsters  
        self.objects = objects
        self.isStartRoom = isStartRoom  
        self.isTreasureRoom = isTreasureRoom
        self.isBossRoom = isBossRoom

    def __repr__(self):
        return f'isStartRoom: {self.isStartRoom}\n isBossRoom: {self.isBossRoom} \n isTreasureRoom: {self.isTreasureRoom}'

class monsters:
    def __init__(self, app, x, y, health, isChampion, dmg, speed, size, dead):
        self.app = app
        self.x = x
        self.y = y
        self.health = health
        self.isChampion = isChampion
        self.speed = speed
        if(isChampion):
            self.dmg = dmg
            self.size = size
        else:
            self.dmg = dmg*2
            self.size = size*1.5
        self.dead = dead
        self.angle = 270

    def takeDmg(self, dmg):
        self.health-=dmg
        if(self.health<1):
            self.dead = True

    def isMonsterOverlap(self, monster):
        x = self.x
        y = self.y
        s = self.size
        x1 = monster.x
        y1 = monster.y
        s1 = monster.size
        if(x+s < x1-s1 or x-s > x1+s1 or y-s > y1+s1 or y+s < y1-s1) and not inRock(self.app, monster):
            return False
        return True

    def move(self):
        if(self.x<self.app.player.x):
            self.x += self.speed
            for monster in self.app.monsters:
                if(self!=monster):
                    if((self.isMonsterOverlap(monster) and monster.isMonsterOverlap(self))):
                        self.x-=self.speed
                elif(not isMoveLegal(self.app, self)):
                    self.x-=self.speed
        else:
            self.x -= self.speed
            for monster in self.app.monsters:
                if(self!=monster):
                    if((self.isMonsterOverlap(monster) and monster.isMonsterOverlap(self))):
                        self.x+=self.speed
                elif(not isMoveLegal(self.app, self)):
                    self.x+=self.speed
        if(self.y<self.app.player.y and isMoveLegal(self.app, self)):
            self.y += self.speed
            for monster in self.app.monsters:
                if(self!=monster):
                    if((self.isMonsterOverlap(monster) and monster.isMonsterOverlap(self))):
                        self.y-=self.speed
                elif(not isMoveLegal(self.app, self)):
                    self.y-=self.speed
        else:
            self.y -= self.speed
            for monster in self.app.monsters:
                if(self!=monster):
                    if((self.isMonsterOverlap(monster) and monster.isMonsterOverlap(self))):
                        self.y+=self.speed
                elif(not isMoveLegal(self.app, self)):
                    self.y+=self.speed
    
    def monsterHitPlayer(self):
        x = self.app.player.x
        y = self.app.player.y
        s = self.app.player.size
        distance = math.sqrt((x-self.x)**2+(y-self.y)**2)
        if(distance<=s+self.size):
            self.app.invincibilityTimer+=100
            self.app.player.takeDmg(self.dmg)
            return True
        return False

    def rangeAttack(self):
        self.app.enemyBullets.append(enemyBullet(self.app, self.dmg, self.x, self.y))

class squareMonst(monsters):
    def __init__(self, app, x, y, health, isChampion, dmg, speed, size, dead):
        super().__init__(app, x, y, health, isChampion, dmg, speed, size, dead)
        self.app = app
        self.x = x
        self.y = y
        self.health = health*(1.5**self.app.floorNum)
        self.maxHP = self.health
        self.isChampion = isChampion
        self.speed = speed
        if(not isChampion):
            self.dmg = dmg
            self.size = size
        else:
            self.dmg = dmg*2
            self.size = size*1.5
        self.dead = dead
        self.poisoned = False
    
    


class rock:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

class enemyBullet:
    def __init__(self, app, dmg, x, y):
        self.app = app
        self.dmg = dmg
        self.size = 10
        self.x = x
        self.y = y
        self.speed = 5
        self.startx = x
        self.starty = y
        dx = self.app.player.x-x
        dy = self.app.player.y-y
        self.dir = math.degrees(math.atan2(dy, dx))

    def move(self):
        if(self.x<self.app.player.x):
            self.x += self.speed
        else:
            self.x -= self.speed
        if(self.y<self.app.player.y):
            self.y += self.speed
        else:
            self.y -= self.speed
        if(not isMoveLegal(self.app, self)):
            self.app.enemyBullets.remove(self)

    def bulletHitPlayer(self):
        x = self.app.player.x
        y = self.app.player.y
        s = self.app.player.size
        distance = math.sqrt((x-self.x)**2+(y-self.y)**2)
        if(distance<=s+self.size):
            self.app.player.takeDmg(self.dmg)
            return True
        return False

#HELPER
def isMoveLegal(app, thing):
    x = thing.x
    y = thing.y
    if(x>app.marginx and x<app.width-app.marginx and y>app.marginy and y<app.height-app.marginy and not inRock(app, thing)):
        return True
    return False

#checks if two things are overlapping
def isOverlap(thing1, thing2):
        x = thing1.x
        y = thing1.y
        s = thing1.size
        x1 = thing2.x
        y1 = thing2.y
        s1 = thing2.size
        if(x+s < x1-s1 or x-s > x1+s1 or y-s > y1+s1 or y+s < y1-s1):
            return False
        return True

#checks if something is in a rock
def inRock(app, thing):
    for rock in app.rocks:
        if(isOverlap(rock, thing)):
            return True
    return False


class bullet:
    def __init__(self, app, dmg, size, x, y, speed, dir, range):
        self.app = app
        self.dmg = dmg
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.dir = dir
        self.range = range
        self.startx = x
        self.starty = y

    def bulletMove(self):
        if(self.dir=="Up"):
            self.y-=self.speed
        elif(self.dir=="Down"):
            self.y+=self.speed
        elif(self.dir=="Left"):
            self.x-=self.speed
        elif(self.dir=="Right"):
            self.x+=self.speed

    def bulletHitMonster(self):
        for monster in self.app.monsters:
            x = monster.x
            y = monster.y
            s = monster.size
            distance = math.sqrt((x-self.x)**2+(y-self.y)**2)
            if(distance<=s+self.size):
                monster.takeDmg(self.app.player.dmg)
                if(self.app.player.hasPoison):
                    monster.poisoned = True
                return True
        return False

    def isBulletLegal(self, dir, startx, starty):
        if(isMoveLegal(self.app, self)):
            if(dir=="Up"):
                if(self.y>=starty-self.range and not inRock(self.app, self)):
                    return True
                return False
            elif(dir=="Down"):
                if(self.y<=starty+self.range and not inRock(self.app, self)):
                    return True
                return False
            elif(dir=="Left"):
                if(self.x>=startx-self.range and not inRock(self.app, self)):
                    return True
                return False
            elif(dir=="Right"):
                if(self.x<=starty+self.range and not inRock(self.app, self)):
                    return True
                return False
        return False


def isInNorthDoor(app, x, y):
    doorWidth = 50
    doorHeight = 75
    if(x>app.width/2-doorWidth/2 and x<app.width/2+doorWidth/2):
        if(y>0 and y<doorHeight):
            return True
    return False

def isInSouthDoor(app, x, y):
    doorWidth = 50
    doorHeight = 100
    if(x>app.width/2-doorWidth/2 and x<app.width/2+doorWidth/2):
        if(y>app.height-doorHeight and y<app.height):
            return True
    return False

def isInWestDoor(app, x, y):
    doorWidth = 50
    doorHeight = 100
    if(x>0 and x<doorHeight):
        if(y>app.height/2-doorWidth/2 and y<app.height/2+doorWidth/2):
            return True
    return False

def isInEastDoor(app, x, y):
    doorWidth = 50
    doorHeight = 100
    if(x>app.width-doorHeight and x<app.width):
        if(y>app.height/2-doorWidth/2 and y<app.height/2+doorWidth/2):
            return True
    return False

def isInTrapDoor(app, x, y):
    doorx = app.width/2
    doory = app.height/2
    doorSize = 20
    if(x>doorx-doorSize and x<doorx+doorSize and y>doory-doorSize and y<doory+doorSize):
        return True
    return False

def isInBounds(app, x, y):
    if(x>=0 and x<len(app.map[app.floorNum]) and y>=0 and y<len(app.map[app.floorNum][0])):
        return True
    return False

class player:
    def __init__(self, app, health, firerate, dmg, speed, range, bulletv, x, y, roomx, roomy, floorNum):
        self.app = app
        self.health = health
        self.firerate = firerate
        self.dmg = dmg
        self.speed = speed #pixels per sec
        self.range = range
        self.x = x
        self.y = y
        self.bulletv = bulletv
        self.bsize = 20
        self.roomx = roomx
        self.roomy = roomy
        self.floorNum = floorNum
        self.dead = False
        self.size = 25
        self.upgrades = ['poison', 'dmg', 'hp up', 'hp down dmg up']
        self.hasPoison = False
    
    def takeDmg(self, dmg):
        self.health-=dmg
        if(self.health<1):
            self.dead = True

    def getStartRoom(self, app, floorNum, L):
        for row in range(len(L)):
            for col in range(len(L[row])):
                if(app.map[floorNum][row][col]!=0 and app.map[floorNum][row][col].isStartRoom):
                    return (row, col)

    def move(self, dir):
        if(dir=="s"):
            self.y+=self.speed
            if(not isMoveLegal(self.app, self)):
                self.y-=self.speed
        elif(dir=="w"):
            self.y-=self.speed
            if(not isMoveLegal(self.app, self)):
                self.y+=self.speed
        elif(dir=="a"):
            self.x-=self.speed
            if(not isMoveLegal(self.app, self)):
                self.x+=self.speed
        elif(dir=="d"):
            self.x+=self.speed
            if(not isMoveLegal(self.app, self)):
                self.x-=self.speed

        x = self.roomx
        y = self.roomy
        if(self.app.roomCleared and self.app.map[self.app.floorNum][self.roomx][self.roomy].isTreasureRoom and not self.app.upgradeReceived):
            self.app.upgradeReceived = True
            upgrade = random.choice(self.upgrades)
            #FINISH UPGRADES
            if(upgrade == 'dmg'):
                dmg = random.choice([1, 2, 3])
                self.dmg+=dmg
            elif(upgrade == 'poison'):
                self.hasPoison = True
            elif(upgrade == 'hp up'):
                hp = random.choice([5, 6, 7, 8, 9, 10])
                self.health+=hp
            elif(upgrade == 'hp down dmg up'):
                self.health-=5
                self.dmg+=5


        if(self.app.map[self.app.floorNum][self.roomx][self.roomy].isBossRoom and self.app.roomCleared and isInTrapDoor(self.app, self.x, self.y)):
            self.app.floorNum+=1
            if(self.app.floorNum>=self.app.numFloors):
                self.app.won = True
            else:
                self.app.upgradeReceived = False
                (self.roomx, self.roomy) = self.getStartRoom(self.app, self.app.floorNum, self.app.map[self.app.floorNum])
                self.reset()
        elif(self.app.roomCleared):
            if(isInBounds(self.app, x+1, y)):
                if(self.app.map[self.app.floorNum][x+1][y]!=0):
                    if(isInSouthDoor(self.app, self.x, self.y)):
                        self.roomx+=1
                        self.reset()  
            if(isInBounds(self.app, x-1, y)):
                if(self.app.map[self.app.floorNum][x-1][y]!=0):
                    if(isInNorthDoor(self.app, self.x, self.y)):
                        self.roomx-=1
                        self.reset()  
            if(isInBounds(self.app, x, y+1)):
                if(self.app.map[self.app.floorNum][x][y+1]!=0):
                    if(isInEastDoor(self.app, self.x, self.y)):
                        self.roomy+=1
                        self.reset()  
            if(isInBounds(self.app, x, y-1)):
                if(self.app.map[self.app.floorNum][x][y-1]!=0):
                    if(isInWestDoor(self.app, self.x, self.y)):
                        self.roomy-=1
                        self.reset()  

        

    def reset(self):
        self.app.roomCleared = False
        self.x = self.app.width/2
        self.y = self.app.height/2   
        self.app.bullets = []
        self.app.enemyBullets = []
        self.app.monsters = self.app.map[self.app.floorNum][self.roomx][self.roomy].monsters
        self.app.objects = self.app.map[self.app.floorNum][self.roomx][self.roomy].objects
        
        
    def fire(self, dir):
        self.app.bullets.append(bullet(self.app, self.dmg, self.bsize, self.x, self.y, self.bulletv, dir, self.range))
