from cmu_112_graphics import *
from classes import *

def drawTitleScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
                            image=ImageTk.PhotoImage(app.titleScreen))
def drawWinScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
                            image=ImageTk.PhotoImage(app.winScreen))
def drawRoomBackground(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
                            image=ImageTk.PhotoImage(app.roomImage))

def drawHelpScreen(app, canvas):
    helpText = ["wasd to move", "arrow keys to shoot", "h for help screen", 
                "b to teleport to the 'boss room'", "c to clear a room without killing the monsters", 
                "r to restart", "press 1, 2, 3, 4, or 5 to change number of floors",
                "press h again to close the help screen"]
    y = app.height/2-(len(helpText)*20)/2
    width = 235
    height = (len(helpText)*20)/2+10
    canvas.create_rectangle(app.width/2-width, app.height/2-height, app.width/2+width, app.height/2+height, fill = "white")
    for help in helpText:
        canvas.create_text(app.width/2, y, text=help, font='Arial 15 bold', fill = 'black')
        y += 20

def isInBounds(app, x, y):
    if(x>=0 and x<len(app.map[app.floorNum]) and y>=0 and y<len(app.map[app.floorNum][0])):
        return True
    return False

def drawRocks(app, canvas):
    for i in range(len(app.rocks)):
        x = app.rocks[i].x
        y = app.rocks[i].y
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.rockImage))

def drawMonsters(app, canvas):
    for i in range(len(app.monsters)):
        if(not app.monsters[i].dead):
            x = app.monsters[i].x
            y = app.monsters[i].y
            s = app.monsters[i].size
            canvas.create_rectangle(x-s, y-s, x+s, y+s, fill = "red")

def drawMonsterHealth(app, canvas):
    healthLength = 35
    yOffset = 45
    for monster in app.monsters:
        canvas.create_rectangle(monster.x-healthLength, monster.y-yOffset, monster.x+healthLength, monster.y-(yOffset-10), fill = 'black')
        percentHealth = monster.health/monster.maxHP
        canvas.create_rectangle(monster.x-healthLength+2, monster.y-(yOffset-2), monster.x-healthLength+2+(healthLength*2-4)*percentHealth, monster.y-(yOffset-10+2), fill = 'red')

def drawPlayerStats(app, canvas):
    canvas.create_text(75, 20,
                                text=f"HP: {app.player.health}", anchor = 'n', font='Arial 15 bold', fill = 'white')
    canvas.create_text(75, 50,
                                text=f"dmg: {app.player.dmg}", anchor = 'n', font='Arial 15 bold', fill = 'white')
    if(app.player.hasPoison):
        poison = 'yes'
    else:
        poison = 'no'
    canvas.create_text(115, 100, text=f"Has Poison: {poison}", font='Arial 15 bold', fill = 'white')

def drawDeathText(app, canvas):
    canvas.create_text(app.width/2, app.height/2,
                                text="YOU DIED", font='Helvetica 100 bold')
    canvas.create_text(app.width/2, app.height/2+100,
                                text="Press 'r' to restart", font='Arial 30 bold')
def drawRoom(app, canvas):
    drawRoomBackground(app, canvas)
    x = app.player.roomx
    y = app.player.roomy
    doorWidth = 50
    doorHeight = 75
    if(app.roomCleared):
        if(isInBounds(app, x+1, y)):
            if(app.map[app.floorNum][x+1][y]!=0):
                canvas.create_rectangle(app.width/2+doorWidth/2, app.height-doorHeight, app.width/2-doorWidth/2, app.height, fill = "black")
        if(isInBounds(app, x-1, y)):
            if(app.map[app.floorNum][x-1][y]!=0):
                canvas.create_rectangle(app.width/2+doorWidth/2, 0, app.width/2-doorWidth/2, doorHeight, fill = "black")
        if(isInBounds(app, x, y+1)):
            if(app.map[app.floorNum][x][y+1]!=0):
                canvas.create_rectangle(app.width, app.height/2-doorWidth/2, app.width-doorHeight, app.height/2+doorWidth/2, fill = "black")
        if(isInBounds(app, x, y-1)):
            if(app.map[app.floorNum][x][y-1]!=0):
                canvas.create_rectangle(0, app.height/2-doorWidth/2, doorHeight, app.height/2+doorWidth/2, fill = "black")
        if(app.map[app.floorNum][x][y].isBossRoom):
            drawDoorToNextFloor(app, canvas)
    drawMonsters(app, canvas)
    drawMonsterHealth(app, canvas)
    drawRocks(app, canvas)
    
def drawDoorToNextFloor(app, canvas):
    x = app.width/2
    y = app.height/2
    s = 30
    canvas.create_rectangle(x-s, y-s, x+s, y+s, fill = "black")

def drawPlayer(app, canvas):
    canvas.create_image(app.player.x, app.player.y, 
                            image=ImageTk.PhotoImage(app.playerHead))
    # r = 25

def drawBullets(app, canvas): 
    for bullet in app.bullets:
        x = bullet.x
        y = bullet.y
        r = bullet.size/2
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = "light blue")

    for bullet in app.enemyBullets:
        x = bullet.x
        y = bullet.y
        r = bullet.size/2
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = "red")