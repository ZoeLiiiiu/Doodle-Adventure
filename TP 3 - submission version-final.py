from cmu_112_graphics import *
import random
import math

# CITATION:inspired by the game Doodle Jump: https://doodlejump.io/
# CITATION:loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
# CITATION:resizing image code from:
# https://www.geeksforgeeks.org/how-to-resize-image-in-python-tkinter/
# CITATION:background image from: 
# https://courses.cs.duke.edu/compsci308/cps108/fall10/code/src/vooga/games/doodlejump/resources/images/background.png
# CITATION:doodle image from: 
# https://img.favpng.com/21/21/5/doodle-jump-kinect-video-game-iphone-png-favpng-GFkKZAu193831b88W2c8Vstau.jpg
# CITATION:monster, doodle, and platform images from: 
# https://i.pinimg.com/originals/80/b2/bc/80b2bc94b33ca82cb3beb3fac4903886.jpg
# CITATION:other images from screen shot of Doodle Jump: https://doodlejump.io/
# CITATION:mode code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def appStarted(app):
    url = "https://courses.cs.duke.edu/compsci308/cps108/fall10/code/src/vooga/games/doodlejump/resources/images/background.png"
    app.doodleImageRight = app.loadImage("image/doodle.png")
    app.doodleImageLeft = app.loadImage("image/doodleFlipped.png")
    app.doodleImageUp = app.loadImage("image/doodleUp.png")
    app.monsterRight = app.loadImage("image/monsterRight.png")
    app.monsterLeft = app.loadImage("image/monsterLeft.png")
    app.flyingHatImage = app.loadImage("image/flyingHat.png")
    app.springImage = app.loadImage("image/spring.png")
    app.platformImage = app.loadImage("image/platform.png")
    app.movingPlatformImage = app.loadImage("image/movingPlatform.png")
    app.doodleX = app.width/2
    app.doodleY = app.height
    app.platforms = []
    app.platformsNum = 20
    app.platformLength = 30
    app.platformHeight = 5
    app.flyingHatHeight = 12
    app.flyingHatWidth = 15
    app.needFlyingHat = False
    app.flyingHat = []
    app.doodleHeight = 35
    app.doodleWidth = 40
    app.monsterWidth = 30
    app.monsterHeight = 35
    app.springHeight = 2*app.platformHeight
    app.springWidth = 2*app.platformHeight
    app.backgroundImage = app.loadImage(url)
    app.backgroundImage = app.backgroundImage.resize((400,600))
    app.doodleImageRight = app.doodleImageRight.resize((app.doodleWidth,
                                                        app.doodleHeight))
    app.doodleImageLeft = app.doodleImageLeft.resize((app.doodleWidth,
                                                      app.doodleHeight))
    app.doodleImageUp = app.doodleImageUp.resize((app.doodleWidth,
                                                  app.doodleHeight))
    app.monsterRight = app.monsterRight.resize((app.monsterWidth,
                                                app.monsterHeight))
    app.monsterLeft = app.monsterLeft.resize((app.monsterWidth,
                                              app.monsterHeight))
    app.flyingHatImage = app.flyingHatImage.resize((app.flyingHatWidth,
                                                    app.flyingHatHeight))
    app.springImage = app.springImage.resize((app.springWidth,
                                              app.springHeight))
    app.platformImage = app.platformImage.resize((app.platformLength,
                                                  app.platformHeight))
    app.movingPlatformImage = app.movingPlatformImage.resize((app.platformLength,
                                                              app.platformHeight))
    app.pause = False
    app.dDown = 0
    app.dUp = 0
    app.dLeft = 0
    app.dRight = 0
    app.aDown = 10
    app.aUp = 0
    app.aLeft = 0
    app.aRight = 0
    app.firstJump = True
    app.scrollMargin = app.height/2
    app.scrollY = 0
    app.score = 0
    app.previousScore = 0
    app.coins = 0
    app.coinsList = []
    app.springList = []
    app.coinR = app.platformHeight
    app.win = False
    app.coinsNum = None
    app.springNum =  random.randint(1,2)
    app.timerDelay = 70
    app.gameOver = False
    app.drawGameOverMessage = False
    app.shootingBullet = False
    app.bulletList = []
    app.monsterPosition = []
    app.movingPlatforms = []
    app.bulletR = app.platformHeight
    app.dBullet = 0
    app.shakingDistance = 5
    app.monsterCanDoFirstMove = False
    app.monsterXDistance = 0
    app.movingPlatformXDistance = 5
    app.movingPlatformsNum = 1
    app.platformsbreakable = 2
    app.previousPlatform = None
    app.startToFly = False
    app.mode = "menuMode"
    app.startGameButton = Button(app,app.width/2,app.height/2+30,
                                 "light blue","Start Game")
    app.playAgainButton = Button(app,app.width/2,app.height/2+30,
                                 "light blue","Play Again")
    app.instructionButton = Button(app,app.width/2,app.height/2-30,
                                   "light pink","Instruction")
    app.menuButtonInGameMode = Button(app,app.width/2,app.height/2-30,
                                      "orange","Back to Menu")
    app.menuButtonInInstructionMode = Button(app,app.width/2,app.height*(4/5),
                                             "orange","Back to Menu")
    app.doodleFaceDirection = "Right"
    app.previousFaceDirection = "Right"
    app.monsterFacingDirection = "Right"
    app.haveFlyingHat = False
    app.alreadyGetHat = False
    getPlatforms(app)
    getMovingPlatforms(app)
    getSpring(app)
    getCoins(app)

class Platform:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{(self.x,self.y)}"                                        

class movingPlatform(Platform):
    def changePosition(self,xDistance,yDistance):
        self.x += xDistance
        self.y += yDistance

class Monster:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def changePosition(self,xDistance,yDistance):
        self.x += xDistance
        self.y += yDistance
    def shaking(self,app):
        self.y += app.shakingDistance
        if app.shakingDistance == 5:
            app.shakingDistance = -5
        elif app.shakingDistance == -5:
            app.shakingDistance = 5  
    def __repr__(self):
        return f"monster is at {(self.x,self.y)}"

class FlyingHat:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def changePosition(self,xDistance,yDistance):
        self.x += xDistance
        self.y += yDistance
    def __repr__(self):
        return f"{(self.x,self.y)}"
        
class Bullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def BulletMove(self,yDistance):
        self.y += yDistance

class Button:
    def __init__(self,app,x,y,color,text):
        self.x = x
        self.y = y
        self.height = 30
        self.width = app.width/3
        self.color = color
        self.text = text
    def click(self,x,y):
        # check if is clicking in the button, return True or False
        if self.x - self.width/2 < x <self.x + self.width/2:
            if self.y - self.height/2 < y <self.y + self.height/2:
                return True
        return False     
    def draw(self,canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
                                self.x+self.width/2,self.y+self.height/2,
                                fill = self.color)
        canvas.create_text(self.x,self.y,text = self.text)

# restart the game
def restartGame(app):
    app.monsterFacingDirection = "Right"
    app.doodleFaceDirection = "Right"
    app.previousFaceDirection = "Right"
    app.alreadyGetHat = False
    app.haveFlyingHat = False
    app.needFlyingHat = False
    app.flyingHat = []
    app.platformsNum = 20
    app.doodleX = app.width/2
    app.platforms = []
    app.doodleX = app.width/2
    app.doodleY = app.height
    app.pause = False
    app.dDown = 0
    app.dUp = 0
    app.dLeft = 0
    app.dRight = 0
    app.aDown = 10
    app.aUp = 0
    app.aLeft = 0
    app.aRight = 0
    app.firstJump = True
    app.scrollMargin = app.height/2
    app.scrollY = 0
    app.score = 0
    app.previousScore = 0
    app.coins = 0
    app.coinsList = []
    app.springList = []
    app.win = False
    app.coinsNum = None
    app.springNum =  random.randint(1,2)
    app.gameOver = False
    app.drawGameOverMessage = False
    app.shootingBullet = False
    app.bulletList = []
    app.monsterPosition = []
    app.movingPlatforms = []
    app.monsterCanDoFirstMove = False
    app.dBullet = 0
    app.movingPlatformsNum = 1
    app.platformsbreakable = 2
    app.needFlyingHat = False
    app.flyingHat = []
    app.previousPlatform = None
    getPlatforms(app)
    getMovingPlatforms(app)
    getSpring(app)
    getCoins(app)

def needFlyingHat(app,platformsList):
    if app.scrollY == 0:
        app.needFlyingHat = True
    else:
        app.needFlyingHat = False
    
def getFlyingHat(app,platformsList):
    if app.needFlyingHat == True and app.flyingHat == [] and not app.alreadyGetHat:
        app.needFlyingHat = False
        highestPlatformY = app.height
        highestIndex = 0
        for i in range(len(platformsList)):
            if platformsList[i].y < highestPlatformY:
                highestPlatformY = platformsList[i].y
                highestIndex = i
        app.hightest = highestIndex
        x = platformsList[highestIndex].x
        # the center of the platform is the position we use to keep track of flying hat
        y = platformsList[highestIndex].y - app.platformHeight/2
        app. flyingHat = [FlyingHat(x,y)]

def renewFlyingHat(app):
    if app. flyingHat != [] and not app.alreadyGetHat:
        app. flyingHat[0].changePosition(0,app.scrollY)
        app. flyingHat = [app. flyingHat[0]]
        if app. flyingHat[0].y > app.height:
            app.flyingHat.pop()

def takeFlyingHat(app):
    if app.flyingHat != []:
        y = app. flyingHat[0].y
        x = app. flyingHat[0].x
        if app.dUp+app.dDown>=0 and y-abs(app.dDown + app.dUp)<=app.doodleY<=y+abs(app.dDown + app.dUp):
            if x-app.platformLength/2<=app.doodleX<=x+app.platformLength/2:
                app.alreadyGetHat = True
                app.haveFlyingHat = True
                app.flyingHat[0].x = app.doodleX
                app.flyingHat[0].y = app.doodleY + app.doodleHeight
                app.flyingHat.pop()
                return True
    if app.dUp >= 0:
        app.haveFlyingHat = False
    return False

   
# check if the new old platform is too close to the old one
def platformNotToClose(app,platforms,newX,newY):
    for platform in platforms:
        oldX = platform.x
        oldY = platform.y
        # make sure not too close with the other platform
        if abs(oldY - newY) <= app.platformHeight*4 and abs(oldX - newX) <= app.platformLength*2:
            return False
        # make sure not too close with the monster
        if app.monsterPosition != []:
            if abs(newY-(app.monsterPosition[0].y-app.monsterHeight/2)) <= 4*app.platformHeight and abs(newY-(app.monsterPosition[0].y+app.monsterHeight/2)) <= 4*app.platformHeight:
                return False
    return True

# check if the old platform is too far from the new one
# the function is make sure the game is winable
def platformNotToFar(app,platforms,newX,newY):
    if platforms == []:
        return True
    for platform in platforms:
        oldX = platform.x
        oldY = platform.y
        if abs(oldY - newY) < 80 and abs(oldX - newX) < 120:
            return True
    return False

def getSpring(app):
    # determine how may springs are we going to generate
    # determine which platform will the springs be on
    while len(app.springList) < app.springNum:
        springIndex = random.randint(0,9)
        x = app.platforms[springIndex].x
        y = app.platforms[springIndex].y - app.platformHeight/2
        if (x,y) not in app.springList and (x,y) not in app.coinsList:
            app.springList.append((x,y))
    
def renewSpring(app):
    springListRenew = []
    for spring in app.springList:
        x = spring[0]
        y = spring[1] + app.scrollY
        if y < app.height:
            springListRenew.append((x,y))
    # make sure the number of coin is stable
    while len(springListRenew) < app.springNum:
        springIndex = random.randint(0,9)
        x = app.platforms[springIndex].x
        y = app.platforms[springIndex].y - app.platformHeight/2
        if (x,y) not in app.springList and (x,y) not in app.coinsList:
            springListRenew.append((x,y))
    app.springList = springListRenew 
 
def jumpOnSpring(app):
    for spring in app.springList:
        # check if the doodle meet the coin
        if app.dUp+app.dDown>=0 and spring[1] -abs(app.dDown + app.dUp)+app.springHeight/2<=app.doodleY<=spring[1]+abs(app.dDown + app.dUp)+app.springHeight/2:
            if spring[0]-app.platformLength/2<=app.doodleX<=spring[0]+app.platformLength/2:
                return True
    return False

# make sure the doodle jump on the first platform
def getFirstPlatforms(app):
    x = random.randint(app.width//2 - app.doodleWidth//2,app.width//2 + app.doodleWidth//2)
    y = random.randint(app.height - 50 ,app.height - 5)
    y = (y//10)*10
    platform = Platform(x,y)
    app.platforms.append(platform)   

def getPlatforms(app):
    # getting the first platform to make sure that the player doesn't 
    # lose the game from the begining
    getFirstPlatforms(app)
    while len(app.platforms) < app.platformsNum:
        # using the midpoint to store the image position
        # so that it is easier for loading a image later
        possibleNewX = random.randint(30,app.width-30)
        possibleNewY = random.randint(5,app.height-5)
        possibleNewY = (possibleNewY//10)*10
        platform = Platform(possibleNewX,possibleNewY)
        if platformNotToClose(app,app.platforms,
                              possibleNewX,possibleNewY) and platformNotToFar(app,
                              app.platforms,possibleNewX,possibleNewY):
            app.platforms.append(platform)

def getMovingPlatforms(app):
    x = random.randint(app.width//2 - app.doodleWidth//2,
                       app.width//2 + app.doodleWidth//2)
    y = random.randint(app.height - 50 ,app.height - 5)
    y = (y//10)*10
    count = 0
    while len(app.movingPlatforms) < app.movingPlatformsNum:
        count += 1
        if count >= 100:
            break
        if platformNotToClose(app,app.platforms,x,y):
            platform = movingPlatform(x,y)
            app.movingPlatforms.append(platform)

def renewMovingPlatforms(app):
        count = 0
        movingPlatformsRenew = []
        for platform in app.movingPlatforms:
            x = platform.x
            y = platform.y + app.scrollY
            if y < app.height:
                movingPlatformsRenew.append(movingPlatform(x,y))
        while len(movingPlatformsRenew) < app.movingPlatformsNum:
            count += 1
            if count >= 100:
                app.movingPlatforms = movingPlatformsRenew
                break
            possibleNewX = random.randint(30,app.width-30)
            possibleNewY = random.randint(5,app.height/2)
            # make platform position divisible by 10,so they will look better
            possibleNewY = (possibleNewY//10)*10
            # check if two platforms are getting too far or too close
            if platformNotToClose(app,movingPlatformsRenew,possibleNewX,
                                  possibleNewY) and platformNotToClose(app,
                                  app.platforms,possibleNewX,possibleNewY):
                # app.movingPlatformFirstMove = True
                movingPlatformsRenew.append(movingPlatform(possibleNewX,
                                                           possibleNewY))
        app.movingPlatforms = movingPlatformsRenew
  
def moveMovingPlatforms(app):
        for platform in app.movingPlatforms:
            if platform.x > app.width - 50:
                app.movingPlatformXDistance = -5
            if platform.x < 50:
                app.movingPlatformXDistance = 5
            platform.changePosition(app.movingPlatformXDistance,0) 

# as the canvas scrolling up, the platform needs to be renewed
def renewPlatforms(app):
        count = 0
        platformsRenew = []
        for platform in app.platforms:
            x = platform.x
            y = platform.y + app.scrollY
            if y < app.height:
                platformsRenew.append(Platform(x,y))
        while len(platformsRenew) < app.platformsNum:
            count += 1
            if count >= 1000:
                app.platforms = platformsRenew
                break
            possibleNewX = random.randint(30,app.width-30)
            possibleNewY = random.randint(5,app.height/2)
            # make platform position divisible by 10,so they will look better
            possibleNewY = (possibleNewY//10)*10
            # check if two platforms are getting too far or too close
            if platformNotToClose(app,platformsRenew,possibleNewX,possibleNewY) and platformNotToFar(app,app.platforms,possibleNewX,possibleNewY):
                if platformNotToClose(app,app.movingPlatforms,possibleNewX,possibleNewY):
                    platformsRenew.append(Platform(possibleNewX,possibleNewY))
        app.platforms = platformsRenew
        # CITATION: try and excpet code from: 
        # https://www.cs.cmu.edu/~112/notes/notes-exceptions.html
        try:
            renewCoin(app)
        except:
            app.coinsList = []
        try:
            renewSpring(app)
        except:
            app.springList = []

def getCoins(app):
    # determine how may coins are we going to generate
    app.coinsNum = random.randint(3,5)
    # determine which platform will the coins be on
    while len(app.coinsList) < app.coinsNum:
        coinsIndex = random.randint(0,9)
        x = app.platforms[coinsIndex].x
        y = app.platforms[coinsIndex].y - app.platformHeight/2
        if (x,y) not in app.coinsList and (x,y) not in  app.springList:
            app.coinsList.append((x,y))

# when the coin is collected by doodle or getting out off the canvas bound
# new coin need to be generated
def renewCoin(app):
    coinsListRenew = []
    for coin in app.coinsList:
        x = coin[0]
        y = coin[1] + app.scrollY
        if y < app.height:
            coinsListRenew.append((x,y))
    # make sure the number of coin is stable
    while len(coinsListRenew) < app.coinsNum:
        coinsIndex = random.randint(0,9)
        x = app.platforms[coinsIndex].x
        y = app.platforms[coinsIndex].y - app.platformHeight/2
        if (x,y) not in app.coinsList and (x,y) not in  app.springList:
            coinsListRenew.append((x,y))
    app. coinsList = coinsListRenew      

# if the doodle encounter the coin
# the coin image disappear
# the total coin += 2
def doodleTakesCoin(app):
    for coin in app.coinsList:
        coinX = coin[0]
        coinY = coin[1]
        # check if the doodle meet the coin
        if app.dUp+app.dDown>=0 and coinY-abs(app.dDown + app.dUp)+app.coinR<=app.doodleY<=coinY+abs(app.dDown + app.dUp)+app.coinR:
            if coinX-app.platformLength/2<=app.doodleX<=coinX+app.platformLength/2:
                app.coinsList.remove(coin)
                app.coins += 2
                return

def checkWin(app):
    if app.coins >= 100:
        app.win = True

def calculateScore(app):
    if not app.gameOver:
        app.score += int(app.scrollY)

# the number of platform deceases while the player score higher
def changePlatformsAndCoinsNum(app):
    if app.score - app.previousScore >= 1000:
       app.platformsNum -= 2
       app.movingPlatformsNum += 1
       if app.movingPlatformsNum > 8:
           app.movingPlatformsNum = 8
       app.coins += 20
       if app.coins >= 20:
           getMonster(app)
       app.previousScore = app.score

def monsterIsLegal(app,x,y):
        if y <= app.doodleY - 100:
            for platform in app.platforms:
                if abs(platform.y-(y-app.monsterHeight/2)) <= 4*app.platformHeight and abs(platform.y-(y+app.monsterHeight/2)) <= 4*app.platformHeight:
                    return False
            return True
    
# start to generating monster after the coins is more than 20 
# generate a monster every 1000 pixels      
def getMonster(app):
    count = 0
    while app.monsterPosition == []:
        count += 1
        if count >= 50:
            break
        x = random.randint(50,app.width-50)
        y = random.randint(100,app.height/2)
        y = (y//10)*10
        if monsterIsLegal(app,x,y):
            app.monsterPosition.append(Monster(x,y))
            app.monsterCanDoFirstMove = True

# helper function that enable the monster scorlling up and down
def renewMonster(app):
    if app.monsterPosition != []:
        app.monsterPosition[0].changePosition(0,app.scrollY)
        app.monsterPosition = [app.monsterPosition[0]]
        if app.monsterPosition[0].y > app.height:
            app.monsterPosition.pop()
            app.monsterCanDoFirstMove = False

# let monstering shaking to give it more characterstics
def monsterShaking(app):
    for monster in app.monsterPosition:
        monster.shaking(app)

# the monster will move horizontal if there is no platform 60 pixels undreneath
def isMonsterMovingHorizontal(app):
        for platform in app.platforms:
            if app.monsterPosition[0].y+app.monsterHeight/2+60 > platform.y:
                return False
        return True   

# enable monster to move horizontally and vertically
def monsterMovingHorizontal(app):
        if app.monsterPosition != []:
            if app.monsterCanDoFirstMove:
                if isMonsterMovingHorizontal(app):
                    if app.monsterPosition[0].x > app.width/2:
                        app.monsterFacingDirection = "Left"
                        app.monsterXDistance = -10
                        app.monsterCanDoFirstMove = False
                    else:
                        app.monsterFacingDirection = "Right"
                        app.monsterXDistance = 10
                        app.monsterCanDoFirstMove = False
                    app.monsterPosition[0].changePosition(app.monsterXDistance,
                                                          app.scrollY)
            else:
                if app.monsterPosition[0].x > app.width - 50:
                        app.monsterFacingDirection = "Left"
                        app.monsterXDistance = -10
                if app.monsterPosition[0].x < 50:
                        app.monsterFacingDirection = "Right"
                        app.monsterXDistance = 10
                app.monsterPosition[0].changePosition(app.monsterXDistance,
                                                      app.scrollY)             
# check if bomping of monster, if bump, gameOver
def bumpOnMonster(app):
    if app.monsterPosition != [] and not app.haveFlyingHat:
        monsterX = app.monsterPosition[0].x
        monsterY = app.monsterPosition[0].y
        if app.dUp + app.dDown <= 0 and monsterY + app.monsterHeight/2 - abs(app.dDown + app.dUp) <= app.doodleY <= monsterY + app.monsterHeight/2 + abs(app.dDown + app.dUp):
            if app.doodleX + app.doodleWidth > monsterX - app.monsterWidth/2 and app.doodleX - app.doodleWidth < monsterX + app.monsterWidth/2:
                app.doodleY = monsterY + app.monsterHeight
                app.dUp = 0
                app.dDown = 0
                app.aUp = 0
                return True
    return False 

# killing the monster by shooting bullet to it
def shootingBullet(app):
    if not app.pause and not app.gameOver:
        app.bulletX = app.doodleX
        app.bulletY = app.doodleY - app.doodleHeight/2
        app.bulletList.append(Bullet(app.bulletX,app.bulletY))
        app.dBullet = -80

def renewBullet(app):
    for bullet in app.bulletList:
        bullet.BulletMove(app.dBullet)
    if app.bulletList!= [] and app.bulletList[-1].y < 0:
        app.doodleFaceDirection = app.previousFaceDirection

def bulletHitMonster(app,bullet):
    # check if the doodle meet the coin
    if app.monsterPosition != []:
        if bullet.y+app.dBullet<=app.monsterPosition[0].y<=bullet.y-app.dBullet:
            if app.monsterPosition[0].x-app.monsterWidth/2<bullet.x<app.monsterPosition[0].x+app.monsterWidth/2:
                return True
        return False

def bulletKillMonster(app):
    for bullet in app.bulletList:
        if bulletHitMonster(app,bullet):
            app.bulletList.remove(bullet)
            app.monsterPosition.pop()

# CITATION:mode code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes   
def gameMode_timerFired(app):
        checkWin(app)
        if not app.pause:
            if app.firstJump:
                app.aUp = -50
                app.firstJump = False
            app.dDown += app.aDown
            app.dUp += app.aUp
            app.dLeft += app.aLeft
            app.dRight += app.aRight
            app.doodleY = app.doodleY + app.dUp + app.dDown
            app.doodleX = (app.doodleX + app.dLeft + app.dRight)%app.width
            calculateScore(app)
            doodleMove(app)
            doodleVisible(app)
            renewPlatforms(app)
            renewMovingPlatforms(app)
            calculateScore(app)
            changePlatformsAndCoinsNum(app)
            renewMonster(app)
            renewBullet(app)
            monsterShaking(app)
            bulletKillMonster(app)
            monsterMovingHorizontal(app)
            moveMovingPlatforms(app)
            needFlyingHat(app,app.platforms)
            getFlyingHat(app,app.platforms)
            renewFlyingHat(app)
            takeFlyingHat(app)
            if bumpOnMonster(app):
                app.gameOver = True
                app.doodleFaceDirection = "Right"

def menuMode_mousePressed(app,event):
    if app.startGameButton.click(event.x,event.y):
        app.mode = "gameMode"
        restartGame(app)
    if app.instructionButton.click(event.x,event.y):
        app.mode = "instructionMode"

def instructionMode_mousePressed(app,event):
    if app.menuButtonInInstructionMode.click(event.x,event.y):
        app.mode = "menuMode"  

def gameMode_mousePressed(app,event):
    if app.gameOver or app.win:
        if app.menuButtonInGameMode.click(event.x,event.y):
            app.mode = "menuMode" 
        if app.playAgainButton.click(event.x,event.y):
            restartGame(app)
        
def gameMode_keyPressed(app,event):
    if event.key == "r":
        restartGame(app)  
    if event.key == "w":
        app.win = True
    if not app.win:
        if event.key == "Left":
            app.doodleFaceDirection = "Left"
            app.previousFaceDirection = "Left"
            app.aLeft = - 20
            app.aRight = 5
        if event.key == "Right":
            app.doodleFaceDirection = "Right"
            app.previousFaceDirection = "Right"
            app.aLeft = - 5
            app.aRight = 20
        if event.key == "p":
            app.pause = not app.pause
        if event.key == "m":
                getMonster(app)
        if event.key == "Space":
            app.doodleFaceDirection = "Up"
            shootingBullet(app)
          

# micmic the doodle't move with elasticity and gravity
# jumping up if step on a platform
# always fallingdown
def doodleMove(app):
    if app.gameOver:
        app.dUp = 0
        app.aUp = 0
    # set the horizontal accelaration
    # the accelaration get to 0 immediately after key press
    if app.win:
        # after new, the doodle will no longer appear on the canvas
        app.doodleY = 0
        app.doodleX = 0
        app.dUp = 0
        app.aUp = 0
        app.dDown = 0
    app.aUp = 0
    if app.aLeft != 0 and app.aLeft != -5:
        app.aLeft = 0
    elif app.aRight != 0 and app.aRight != 5:
        app.aRight = 0
    if app.dLeft + app.dRight == 0:
        app.aLeft = 0
        app.aRight = 0
    for platform in app.platforms:
        platformY = platform.y
        platformX = platform.x
        # chek if it is stepping ona platform by checking if doodleY is within 
        # platform Y + speed and platform - speed
        # also cheecking if doodleX is half inside the platform
        if doodleJumpingOnPlatform(app,platformX, platformY) or doodleJumpingOnMonster(app):
            if takeFlyingHat(app):
                app.aUp = -90               
            elif not jumpOnSpring(app) and not app.haveFlyingHat:
                app.aUp = -50
            elif jumpOnSpring(app) and not app.haveFlyingHat:
                app.aUp = -70    
            doodleTakesCoin(app)
            app.dLeft = 0
            app.dRight = 0
            app.aLeft = 0
            app.aRight = 0
            app.dUp = 0
            app.dDown = 0
            app.doodleY = platformY - app.platformHeight/2
            jumpOnSpring(app)
            return
    app.aUp = 0
    for platform in app.movingPlatforms:
        if doodleJumpingOnMovingPlatform(app,platform.x, platform.y):
            app.aUp = -50
            app.dLeft = 0
            app.dRight = 0
            app.aLeft = 0
            app.aRight = 0
            app.dUp = 0
            app.dDown = 0
            app.doodleY = platform.y - app.platformHeight/2
            return      
    app.aUp = 0 

def doodleJumpingOnPlatform(app,platformX, platformY):
    if not app.gameOver: #and not app.win:
        if app.dUp + app.dDown >= 0 and platformY - app.platformHeight/2 - abs(app.dDown + app.dUp) <= app.doodleY <= platformY - app.platformHeight/2 + abs(app.dDown + app.dUp):
            # To jump on a unmove platform, doodle must be half inside the platform
            if platformX - app.platformLength/2 <= app.doodleX <= platformX + app.platformLength/2:
                return True
    return False

def doodleJumpingOnMonster(app):
    if not app.gameOver and app.monsterPosition != [] and not app.haveFlyingHat:
        monsterY = app.monsterPosition[0].y
        monsterX = app.monsterPosition[0].x
        if app.dUp + app.dDown >= 0 and monsterY - app.monsterHeight/2 - abs(app.dDown + app.dUp) <= app.doodleY <= monsterY - app.monsterHeight/2 + abs(app.dDown + app.dUp):
            # as long as the doodle touch the monster when jumping down, 
            # it will be detected as jumping on the monster
            if app.doodleX + app.doodleWidth > monsterX - app.monsterWidth/2 and app.doodleX - app.doodleWidth < monsterX + app.monsterWidth/2:
                app.doodleY = app.monsterPosition[0].y - app.monsterHeight/2
                app.monsterPosition.pop()
                return True
    return False

def doodleJumpingOnMovingPlatform(app,platformX, platformY):
    if not app.gameOver:
        if app.dUp + app.dDown >= 0 and platformY - app.platformHeight/2 - abs(app.dDown + app.dUp) <= app.doodleY <= platformY - app.platformHeight/2 + abs(app.dDown + app.dUp):
            # To jump on a moving platform, doodle must be half inside the platform
            if platformX - app.platformLength/2 <= app.doodleX <= platformX + app.platformLength/2:
                return True
    return False
    
# CITATION:learn scorlling from course website: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# doodle is always at the lower part of the screen
# if it jumps to the upper part, the screen will scroll down by 20
def doodleVisible(app):
    if app.haveFlyingHat:
        app.scrollY = -(app.dUp)
    elif (app.doodleY < app.scrollMargin):
        app.scrollY = -(app.dUp)*(1/2)
    elif app.doodleY > app.height:
        app.gameOver = True
        if app.dDown != 0:
            app.scrollY = -(app.dDown)*(9/10)
        else:
            app.scrollY = 150
        app.doodleY += app.scrollY  
        if app.doodleY > app.height:
            app.drawGameOverMessage = True 
    else:
        app.scrollY = 0

# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def drawDoodle(app,canvas):
    if app.doodleFaceDirection == "Right":
        canvas.create_image(app.doodleX, app.doodleY-app.doodleHeight/2, 
                            image=ImageTk.PhotoImage(app.doodleImageRight))
    elif app.doodleFaceDirection == "Left":
        canvas.create_image(app.doodleX, app.doodleY-app.doodleHeight/2, 
                            image=ImageTk.PhotoImage(app.doodleImageLeft))
    elif app.doodleFaceDirection == "Up":
        canvas.create_image(app.doodleX, app.doodleY-app.doodleHeight/2, 
                            image=ImageTk.PhotoImage(app.doodleImageUp))
           
# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def drawPlatforms(app,canvas):
    for platform in app.platforms:
        x = platform.x
        y = platform.y
        canvas.create_image(x, y,image=ImageTk.PhotoImage(app.platformImage))

# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def drawMovingPlatforms(app,canvas):
    for platform in app.movingPlatforms:
        x = platform.x
        y = platform.y
        canvas.create_image(x, y,
                            image=ImageTk.PhotoImage(app.movingPlatformImage))

def drawCoins(app,canvas):
    for coin in app.coinsList:
        x = coin[0]
        y = coin[1] - app.coinR
        canvas.create_oval(x-app.coinR,y-app.coinR,x+app.coinR,y+app.coinR,
                           width = 0.1,fill = "orange")

# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def drawSpring(app,canvas):
    for spring in app.springList:
        x = spring[0]
        y = spring[1] - app.springHeight/2
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.springImage))

def drawScoreAndCoins(app,canvas):
    canvas.create_rectangle(0,0,app.width,40,fill = "orange",width = 0)
    canvas.create_text(10,20,text = f"score:{app.score}",anchor = "w")
    canvas.create_text(app.width - 10,20,text = f"coins:{app.coins}",
                       anchor = "e")


def drawWinMessage(app,canvas):
    if app.win: 
        canvas.create_rectangle(0,40,app.width,80,fill = "pink",width = 0)
        canvas.create_text(app.width/2,60,text = "You Win!!")
        canvas.create_rectangle(app.width/4,app.height/2-90,app.width*(3/4),
                                app.height/2+90,
                                fill = "white",width = 0)
        app.menuButtonInGameMode.draw(canvas)
        app.playAgainButton.draw(canvas)
        
# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def drawMonster(app,canvas):
    for monster in app.monsterPosition:
        monsterX = monster.x
        monsterY = monster.y
        if app.monsterFacingDirection == "Left":
            canvas.create_image(monsterX, monsterY, 
                                image=ImageTk.PhotoImage(app.monsterLeft))
        elif app.monsterFacingDirection == "Right":
            canvas.create_image(monsterX, monsterY, 
                               image=ImageTk.PhotoImage(app.monsterRight))
# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def drawFlyingHat(app,canvas):
    for hat in app.flyingHat:
        x = hat.x
        y = hat.y
        canvas.create_image(x, y-app.flyingHatHeight/2, 
                                image=ImageTk.PhotoImage(app.flyingHatImage))

def drawGameOverMessage(app,canvas):
    if not app.win and app.drawGameOverMessage: 
        canvas.create_rectangle(0,40,app.width,80,fill = "light blue",width = 0)
        canvas.create_text(app.width/2,60,text = "Game Over!!")
        if app.doodleY > app.height:
            app.menuButtonInGameMode.draw(canvas)
            app.playAgainButton.draw(canvas)

def drawBullet(app,canvas):
    for bullet in app.bulletList:
        canvas.create_oval(bullet.x-app.bulletR,bullet.y-app.bulletR,
                           bullet.x+app.bulletR,bullet.y+app.bulletR,
                           fill = "white")
        
# CITATION: loading image code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
# CITATION: mode code from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes 
def menuMode_redrawAll(app,canvas):
    canvas.create_image(app.width/2, app.height/2, 
                        image=ImageTk.PhotoImage(app.backgroundImage)) 
    canvas.create_text(app.width/2,20,text = "Welcome To Dooodle Adventure!",
                       font = 'Arial 12 bold')
    app.startGameButton.draw(canvas)
    app.instructionButton.draw(canvas)
  
def gameMode_redrawAll(app,canvas):
    canvas.create_image(app.width/2, app.height/2, 
                        image=ImageTk.PhotoImage(app.backgroundImage)) 
    drawSpring(app,canvas)
    drawPlatforms(app,canvas)
    drawMovingPlatforms(app,canvas)
    drawCoins(app,canvas)
    drawFlyingHat(app,canvas)
    drawMonster(app,canvas)
    drawBullet(app,canvas)
    drawDoodle(app,canvas)
    drawScoreAndCoins(app,canvas)
    drawWinMessage(app,canvas)
    drawGameOverMessage(app,canvas)

# method of drawing message is from previous HW: HW7 one-dimension connect 4
def instructionMode_redrawAll(app,canvas):
    canvas.create_image(app.width/2, app.height/2, 
                        image=ImageTk.PhotoImage(app.backgroundImage))  
    canvas.create_text(app.width/2,20,text = "Dooodle Adventure Instruction",
                       font = 'Arial 12 bold')
    messages =["In the game,", 
               "the player controls the doodle to go left or right", 
               "by pressing Left or Right Key.",
                "so that the doodle can jump on a platform and go upward.",
                "If the doodle doesn't step on a platform, it will fall,", 
                "and the game is over.",
                "The doodle can collect the coins that appear on the platform.",
                "The doodle will also get a 20-coin reward,",
                "for every 1000 pixels it jumps up. ",
                "While the doodle is jumping up, monsters may appear.",
                "If the doodle bumps on a monster, ",
                "the game is over. ",
                "Doodle can kill the monster by shooting bullets toward it,",
                "or stepping on it.",
                "Press Space Key to shoot bullet.",
                "The doodle can get a flying hat only once in a game.",
                "The game will be pause if pressing 'p' key.",
                "The flying hat helps doodle go further"
                "To win the game", 
                "the doodle needs to collect 100 coins."]
    for i in range(len(messages)):
        line = messages[i]
        canvas.create_text(app.width/2,20+2*20 + 1.5*i*12,
                           anchor = "n",font = f'Arial 10',
                           text = line)
    app.menuButtonInInstructionMode.draw(canvas)   

runApp (width = 400,height = 600)   