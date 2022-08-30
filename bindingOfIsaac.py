#################################################
#Term Project
# name:Harry Sha
# andrew id:hsha
# Recitation C
#################################################

from cmu_112_graphics import *
from classes import *
from view import *
import random, math


#################################################
# image citations
#################################################
#player sprite citation
#https://www.pngegg.com/en/png-pevmu

#title screen citation
#https://www.mobygames.com/game/windows/binding-of-isaac-rebirth/screenshots/gameShotId,739622/

#win screen smiley citation
#https://www.istockphoto.com/vector/thumb-up-emoticon-gm157030584-22287357

#rock sprite citation
#https://www.reddit.com/r/bindingofisaac/comments/6wo2qo/finding_marked_rocks_in_the_womb_etc/

#################################################
# main app
#################################################

def playBindingOfIsaac():
    runApp(width=915, height=500)

#################################################
# map generation
#################################################

def make2DList(rows, cols):
    return [([0]*cols) for row in range(rows)]

#recursive map generation using back tracking. 
def createRoom(app, x, y, floor, numRooms, isTreasureRoom, isBossRoom, isStartRoom):
    if(isFloorComplete(floor, numRooms)):
        return True
    app.monsters = []
    monsterPos = [(100, 100), (app.width-100, 100), (app.width-100, app.height-100), (100, app.height-100)]
    if(isTreasureRoom or isBossRoom or isStartRoom):
        numMobs = 0
        if(isStartRoom):
            floor[x][y] = room(x, y, [], [], False, True, False)
            startdirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for i in range(len(startdirs)):
                startdir = random.choice(startdirs)
                startdirs.remove(startdir)
                (row, col) = startdir
                if(roomIsValid(floor, x+row, y+col)):
                    giveUp = random.choice([True, True, True, False])
                    if(not giveUp):
                        return createRoom(app, x+row, y+col, floor, numRooms, False, False, False)
    else:
        numMobs = random.choice([1, 2, 3])
    for i in range(numMobs):
        (monsterx, monstery) = random.choice(monsterPos)
        monsterPos.remove((monsterx, monstery))
        isChampion = random.choice([True, False])
        mob = 'square'
        if(mob=='square'):
            mob = squareMonst(app, monsterx, monstery, 6, isChampion, 1, 1, 20, False)
        app.monsters.append(mob)
    app.rocks = []
    pos = 175
    objectPos = [(pos, pos), (app.width-pos, pos), (app.width-pos, app.height-pos), (200, app.height-pos)]
    for i in range(random.choice([0, 1, 2, 3, 4])):
        (rockx, rocky) = random.choice(objectPos)
        objectPos.remove((rockx, rocky))
        r = rock(rockx, rocky, 20)
        app.rocks.append(r)
    floor[x][y] = room(x, y, app.monsters, app.rocks, isTreasureRoom, isStartRoom, isBossRoom)
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dir in range(len(dirs)):
        dir = random.choice(dirs)
        dirs.remove(dir)
        (row, col) = dir
        if(roomIsValid(floor, x+row, y+col)):
            giveUp = random.choice([True, False])
            if(not giveUp):
                return createRoom(app, x+row, y+col, floor, numRooms, False, False, False)
    return False

#adds boss room and treasure room attributes to the same room(the last room). 
def addSpecialRooms(app):
    ends = []
    for floor in app.map:
        ends = getEnds(floor)
        choice = random.choice(ends)
        choice.isBossRoom = True
        choice.isTreasureRoom = True

def indexInBounds(floor, x, y):
    if(x<0 or x>=len(floor) or y<0 or y>=len(floor[0])):
        return False
    return True

def roomIsValid(floor, x, y):
    if(not indexInBounds(floor, x, y)):
        return False
    adjacentRooms = 0
    if(floor[x][y]==0):
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for i in dirs:
            (row, col) = i
            if(indexInBounds(floor, x+row, y+col) and floor[x+row][y+col]!=0):
                adjacentRooms+=1
        if(adjacentRooms<2):
            return True
    return False

#checks if the floor generated is complete
def isFloorComplete(floor, numRooms):
    rooms = 0
    for row in range(len(floor)):
        for col in range(len(floor[row])):
            if(floor[row][col]!=0):
                rooms+=1
    if(rooms==numRooms):
        return True
    return False

def randNumRooms(floorNum):
    return 5 + random.choice([1, 2]) + floorNum*2

def createFloor(app, floorNum):
    floor = make2DList(9, 9)
    x = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
    y = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
    numRooms = randNumRooms(floorNum)
    if(createRoom(app, x, y, floor, numRooms, False, False, True)):
        return floor
    return createFloor(app, floorNum)
    

def createMap(app, numFloors):
    floorNum = 0
    map = []
    while(floorNum!=numFloors):
        floorNum+=1
        map.append(createFloor(app, floorNum))
    return map

def getStartRoom(app, floorNum, L):
    for row in range(len(L)):
        for col in range(len(L[row])):
            if(app.map[floorNum][row][col]!=0 and app.map[floorNum][row][col].isStartRoom):
                return (row, col)

#gets the dead ends in the map
def getEnds(floor):
    deadEnds = []
    adjacentRooms = 0
    for row in range(len(floor)):
        for col in range(len(floor[row])):
            if(floor[row][col]!=0 and not floor[row][col].isStartRoom):
                adjacentRooms = 0
                dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for i in dirs:
                    (drow, dcol) = i
                    if(indexInBounds(floor, row+drow, col+dcol) and floor[row+drow][col+dcol]!=0):
                        adjacentRooms+=1
                if(adjacentRooms==1):
                    deadEnds.append(floor[row][col])
    return deadEnds


#################################################
# app start
#################################################

def appStarted(app):
    app.timerDelay = 1
    app.won = False
    app.helpScreen = True
    app.gameStarted = False
    app.gameOver = False
    app.roomCleared = False
    app.upgradeReceived = False
    app.invincibilityTimer = 0
    app.poisonTimer = 0
    app.marginx = 45
    app.marginy = 25
    #default numFloors
    app.numFloors = 3
    app.floorNum = 0
    app.map = createMap(app, app.numFloors)
    addSpecialRooms(app)
    (x, y) = getStartRoom(app, app.floorNum, app.map[0])
    
    app.player = player(app, 50, 1, 3, 4, 600, 5, app.width/2, app.height/2, x, y, app.floorNum)
    app.playerIsMoving = False
    app.playerDir = "w"
    
    app.enemyBullets = []
    app.enemyBulletTimer = 0
    app.bullets = []
    app.bulletTimer = 0
    modelPath = "models/"

    app.titleScreen = app.loadImage(modelPath + "titleScreen.jpg")
    app.titleScreen = app.scaleImage(app.titleScreen, 1/2)

    app.winScreen = app.loadImage(modelPath + "smile.jpg")
    app.winScreen = app.scaleImage(app.winScreen, 5/6)

    app.playerHead = app.loadImage(modelPath + "phFwd.png")

    app.roomImage = app.loadImage(modelPath + "roomBackground.png")
    app.roomImage = app.scaleImage(app.roomImage, 2/3)

    app.rockImage = app.loadImage(modelPath + "rock.png")
    app.rockImage = app.scaleImage(app.rockImage, 1/3)

def getBossRoom(app):
    for row in range(len(app.map[app.floorNum])):
        for col in range(len(app.map[app.floorNum][row])):
            if(app.map[app.floorNum][row][col]!=0 and app.map[app.floorNum][row][col].isBossRoom):
                return (row, col)


def keyPressed(app, event):
    if(not app.gameStarted):
        if(event.key=='Space'):
            app.gameStarted = True
    else:
        if(not app.gameOver and not app.won):
            moves = set(['w', 'a', 's', 'd'])
            fireDir = set(["Up", "Down", "Left", "Right"])
            if(event.key in moves):
                app.playerDir = event.key
                app.playerIsMoving = True
            elif(app.bulletTimer>=1000*(1/app.player.firerate) and event.key in fireDir):
                app.player.fire(event.key)
                app.bulletTimer = 0
            elif(event.key=="b"):
                app.roomCleared = False
                app.bullets = []
                app.enemyBullets = []
                (app.player.roomx, app.player.roomy) = getBossRoom(app)
            elif(event.key=="c"):
                app.roomCleared = True
            elif(event.key=="h"):
                app.helpScreen = not app.helpScreen
        if(event.key=="r"):
            reset(app)
        elif(event.key=='1'):
                app.numFloors = 1
                reset(app)
        elif(event.key=='2'):
                app.numFloors = 2
                reset(app)
        elif(event.key=='3'):
                app.numFloors = 3
                reset(app)
        elif(event.key=='4'):
                app.numFloors = 4
                reset(app)
        elif(event.key=='5'):
                app.numFloors = 5
                reset(app)

#reset without numFloors being set to another value
def reset(app):
    app.won = False
    app.helpScreen = True
    app.gameStarted = False
    app.gameOver = False
    app.roomCleared = False
    app.upgradeReceived = False
    app.invincibilityTimer = 0
    app.poisonTimer = 0
    app.floorNum = 0
    app.map = createMap(app, app.numFloors)
    addSpecialRooms(app)
    (x, y) = getStartRoom(app, app.floorNum, app.map[0])
    app.player = player(app, 50, 1, 3, 10, 600, 5, app.width/2, app.height/2, x, y, app.floorNum)
    app.playerIsMoving = False
    app.playerDir = "w"
    app.enemyBullets = []
    app.enemyBulletTimer = 0
    app.bullets = []
    app.bulletTimer = 0


def keyReleased(app, event):
    if(event.key==app.playerDir):
        app.playerIsMoving = False

def timerFired(app):
    if(not app.won and not app.gameOver):
        #makes sure the monsters and rocks are loaded 
        app.monsters = app.map[app.floorNum][app.player.roomx][app.player.roomy].monsters
        app.rocks = app.map[app.floorNum][app.player.roomx][app.player.roomy].objects
        if(app.monsters==[]):
            app.roomCleared = True
        #invincibility "frames" for the player
        app.invincibilityTimer+=app.timerDelay
        if(app.invincibilityTimer==1000):
            app.invincibilityTimer = 0
        if(app.player.hasPoison):
            app.poisonTimer+=app.timerDelay
        for monster in app.monsters:
            if(monster.poisoned and app.poisonTimer>1000):
                app.poisonTimer = 0
                monster.takeDmg(1)
            if(monster.dead):
                app.monsters.remove(monster)
            else:
                #MONSTER DECISION MAKING
                distance = math.sqrt((monster.x-app.player.x)**2 + (monster.y-app.player.y)**2)
                if(distance>300):
                    if(app.enemyBulletTimer==0):
                        monster.rangeAttack()
                else:
                    monster.move()
                if(app.invincibilityTimer==0 and monster.monsterHitPlayer()):
                    if(app.player.dead):
                        app.gameOver = True
        app.bulletTimer+=app.timerDelay
        for bullet in app.bullets:
            bullet.bulletMove()
            if(bullet.bulletHitMonster() or not bullet.isBulletLegal(bullet.dir, bullet.startx, bullet.starty)):
                app.bullets.remove(bullet)
        app.enemyBulletTimer+=app.timerDelay
        if(app.enemyBulletTimer==5000):
            app.enemyBulletTimer = 0
        for bullet in app.enemyBullets:
            bullet.move()
            if(app.invincibilityTimer==0 and bullet.bulletHitPlayer()):
                app.enemyBullets.remove(bullet)
                if(app.player.dead):
                        app.gameOver = True
        if(app.playerIsMoving):
            app.player.move(app.playerDir)

#################################################
# draw
#################################################

def redrawAll(app, canvas):
    if(app.gameStarted):
        if(not app.won):
            if(not app.gameOver):
                drawRoom(app, canvas)
                drawBullets(app, canvas)
                drawPlayer(app, canvas)
                drawPlayerStats(app, canvas)
                if(app.helpScreen):
                    drawHelpScreen(app, canvas)
            else:
                drawDeathText(app, canvas)
        else:
            drawWinScreen(app, canvas)
    else:
        drawTitleScreen(app, canvas)

#################################################
# main
#################################################

def main():
    playBindingOfIsaac()

if __name__ == '__main__':
    main()