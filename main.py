'''
Citations

Songs in Songs Folder: - all songs found on youtube and then converted into mp3 and wav
I Want It That Way - Backstreet Boys - https://www.youtube.com/watch?v=4fndeDfaWCg
Lovely - Billie Eilish feat. Khalid - https://www.youtube.com/watch?v=V1Pl8CzNzCw
Best Part - Daniel Caesar feat. H.E.R - https://www.youtube.com/watch?v=iKk6_2-AAGc
comethru - Jeremy Zucker - https://www.youtube.com/watch?v=jO2viLEW-1A
m.A.A.d City - Kencrick Lamar Remix - https://www.youtube.com/watch?v=MrEXbOrkz-0
Day 'N Nite (nightmare) - Kid Cudi - https://www.youtube.com/watch?v=VrDfSZ_6f4U
A Milli (Remix) - Lil Wayne (K.Theory) - https://www.youtube.com/watch?v=xlDLd8MBkeE
Numb - Linkin' Park - https://www.youtube.com/watch?v=kXYiU_JCYtU
Pirates of the Carribbean Soundtrack Main Theme Song - Hans Zimmer - https://www.youtube.com/watch?v=K3pU67zxPOM
Bangarang - Skrillex feat. Sirah - https://www.youtube.com/watch?v=cR2XilcGYOo
Dance Monkey - Tones and I - https://www.youtube.com/watch?v=Z7GqmzFinEw
Mantra - Troyboi - https://www.youtube.com/watch?v=VUqELNBrevk
Waves - Kanye West - https://www.youtube.com/watch?v=ML8Yq1Rd6I0

Images:
Asteroids Images (AsteroidAnimation.png) - https://opengameart.org/content/spinning-asteroid-animation
background images (background.jpg) - https://tinyurl.com/qtonth2
    different shades of background made through filters
blast (blue) (blast.png)- https://www.deviantart.com/saodvd/art/DragonBall-Ki-Ball-2-593830720
blast (red) (enemyBlast.png)- https://www.deviantart.com/venjix5/art/Red-Energy-Ball-775672784
Power Ups
    Health (healthBoost.png) - https://webstockreview.net/explore/clipart-cross-medic/
    Damage (damageBoost.png)- https://ya-webdesign.com/image/kirby-air-png/372947.html
    Speed (speedBoost.png) - https://www.amazon.com/Webfryslan-Game-Booster/dp/B01JA4C284
    destroy all (destroyBoost.png) - http://clipart-library.com/free/explosion-gif-transparent.html
Green Arrow in Song Menu (GreenArrow.png) - https://www.freeiconspng.com/img/16641
Player (player.png) - https://steamcommunity.com/sharedfiles/filedetails/?id=1700539566
Small Ship (smallShip.png) - https://www.freepngs.com/space-craft-pngs
Medium Ship (mediumShip.png) - https://beathazard.fandom.com/wiki/BH_Ultra_Enemies
Large Ship (largeShip.png) - https://opengameart.org/content/spaceship-6-0
Missile (missile.png) - https://premiumbpthemes.com/explore/rocket-ship-clipart-real.html
Pause / Play Button (pauseButton.png / playButton.png) - https://www.vectorstock.com/royalty-free-vector/play-pause-stop-forward-buttons-set-vector-5090299
Cursor / Target Aim (targetAim.png) - https://pngriver.com/target-png-transparent-image-free-4811/transparent-target-aim-png-image/
Beat Harzard Logo (titleLogo.png) - https://gameflip.com/item/beat-hazard-ultra/4a802ce3-da34-4346-9aaf-b2b809ba73b5
'''

import pygame
# from pygame import mixer
# from pygame.locals import *
import math, random, time
from audioAnalysis import *
from mutagen.mp3 import MP3
from songList import *
# ignore the deprecation warnings https://docs.python.org/3/library/warnings.html
import warnings
warnings.filterwarnings("ignore")
# set up the window sizes
screenWidth = 1000
screenHeight = 600
infoHeight = 50
window = pygame.display.set_mode((screenWidth, screenHeight + infoHeight), 0, 32)
pygame.display.set_caption('Beat Hazard')

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)

# Button class with text inside it
# Button Class inspired by and modified from https://www.youtube.com/watch?v=4_9twnEduFA
class Button(object):
    def __init__(self, text, centerX, centerY, sizeX, sizeY, textSize):
        self.centerX = centerX
        self.centerY = centerY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.x = self.centerX - self.sizeX / 2
        self.y = self.centerY - self.sizeY / 2
        self.color = SILVER
        self.selectedColor = GREEN
        self.fontName = pygame.font.match_font('Arial')
        self.text = text
        self.textSize = textSize
        self.selected = False

    # Draw Text function inspired by http://kidscancode.org/blog/2016/08/pygame_shmup_part_7/
    def drawText(self, surface, color = BLACK):
        font = pygame.font.Font(self.fontName, self.textSize)
        textSurface = font.render(self.text, True, color)
        textBox = textSurface.get_rect()
        textBox.midtop = (self.centerX, self.centerY - self.textSize / 2)
        surface.blit(textSurface, textBox)
    
    def drawButton(self, surface):
        if self.selected:
            pygame.draw.rect(surface, self.selectedColor, (self.x, self.y, self.sizeX, self.sizeY))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.sizeX, self.sizeY))
        self.drawText(surface)


def getAngle(startX, startY, endX, endY):
    '''
    takes in two points and returns the angle of the line between those points
    and the x-axis
    Parameters: 4 ints
    Returns: angle, int
    '''
    dx = endX - startX
    dy = endY - startY
    # if either dX or dY is zero, so that atan doesn't crash
    if dy == 0:
        if dx >= 0:
            return 0
        else:
            return 180
    elif dx == 0:
        if dy >= 0:
            return 90
        else:
            return 270
    elif dx > 0 and dy > 0:
        angle = math.atan(dy / dx)
    elif dx < 0 and dy > 0:
        angle = math.atan(dy / dx) + math.pi
    elif dx > 0 and dy < 0:
        angle = math.atan(dy / dx) + 2 * math.pi
    elif dx < 0 and dy < 0:
        angle = math.atan(dy / dx) + math.pi
    degrees = angle * 180 / math.pi
    return degrees

def getMagnitude(vector):
    '''
    takes in a vector and returns its magnitude
    Parameters: tuple
    Returns: int
    '''
    xComp = vector[0]
    yComp = vector[1]
    return math.sqrt((xComp)**2 + (yComp)**2)

def getUnitVector(vector):
    '''
    takes in a vector and returns its unit vector
    Param: tuple
    returns: tuple
    '''
    xComp = vector[0]
    yComp = vector[1]
    magnitude = getMagnitude(vector)
    unitX = xComp / magnitude
    unitY = yComp / magnitude
    return (unitX, unitY)

def isInRange(x, y):
    '''
    takes in the x and y coordinates and returns whether it is visible in
    the game
    Param: 2 ints
    retruns: bool
    '''
    return (0 <= x <= screenWidth) and (0 <= y <= screenHeight)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def isCollision(x1, y1, size1, x2, y2, size2):
    '''
    Returns if two objects are touching
    Param: 6 ints
    Returns: bool
    '''
    d = distance(x1, y1, x2, y2)
    if d <= size1 / 2 + size2 / 2:
        return True
    return False

class Player(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.centerX = self.x + self.size / 2
        self.centerY = self.y + self.size / 2
        self.xChange = 0
        self.yChange = 0
        self.vel = 3
        self.totalHealth = 500
        self.health = self.totalHealth
        self.image = pygame.image.load('Player.png')
        self.playerImage = pygame.transform.scale(self.image, (self.size, self.size))

    def rotationAngle(self, mouseX, mouseY):
        '''
        takes the mouse position and returns the angle in degrees the player 
        image must rotate to follow the cursor
        Param: 2 ints
        Returns: int
        '''
        centerX = self.x + self.size / 2
        centerY = self.y + self.size / 2
        if mouseX > centerX:
            diff = mouseX - centerX
            return -Player.rotationAngle(self, centerX - diff, mouseY)
        if mouseX - centerX == 0:
            if mouseY - centerY >= 0:
                return 180
            else:
                return 0
        angle = math.atan((mouseY - centerY) / (mouseX - centerX)) - \
            math.pi / 2
        return -(angle * 180 / math.pi)

    def drawPlayer(self, angle = 0):
        '''
        draws the player with the correct rotation angle
        Param: int
        returns: None
        '''
        self.centerX = self.x + self.size / 2
        self.centerY = self.y + self.size / 2
        # from https://www.pygame.org/docs/ref/transform.html 
        newPlayerImage = pygame.transform.rotate(self.playerImage, angle)
        window.blit(newPlayerImage, (self.x, self.y))
        

# Load Power Up images
healthImage = pygame.image.load('healthBoost.png')
speedImage = pygame.image.load('speedBoost.png')
damageImage = pygame.image.load('damageBoost.png')
destroyImage = pygame.image.load('destroyBoost.png')

class PowerUp(object):
    def __init__(self, centerX, centerY):
        self.size = 30
        self.centerX = centerX
        self.centerY = centerY
        self.x = self.centerX - self.size / 2
        self.y = self.centerY - self.size / 2
        self.image = 1

    def drawPowerUp(self):
        window.blit(self.image, (self.x, self.y))

# create subclasses for the different types of powerUps
class MoreDamage(PowerUp):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.image = pygame.transform.scale(damageImage, (self.size, self.size))

class MoreSpeed(PowerUp):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.image = pygame.transform.scale(speedImage, (self.size, self.size))

class MoreHealth(PowerUp):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.image = pygame.transform.scale(healthImage, (self.size, self.size))

class DestroyEnemies(PowerUp):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.image = pygame.transform.scale(destroyImage, (self.size, self.size))

# takes in the initial position and the final position and travels in a straight line
# until blast collides with something or is not in range
class Blast(object):
    def __init__(self, startX, startY, endX, endY):
        self.size = 20
        self.startX = startX - 20
        self.startY = startY - 20
        self.centerX = self.startX + self.size / 2
        self.centerY = self.startY + self.size / 2
        self.endX = endX
        self.endY = endY
        self.vector = (endX - startX , endY - startY)
        self.unitVector = getUnitVector(self.vector)
        self.speed = 20
        self.collided = False
        image = pygame.image.load('blast.png')
        self.image = pygame.transform.scale(image, (20, 20))
        self.damage = 10
        
    def drawBlast(self):
        '''
        draws the blast with the directly towards where mouse pressed
        param: self
        return: None
        '''
        changeX = self.speed * self.unitVector[0]
        changeY = self.speed * self.unitVector[1]
        self.startX += changeX
        self.startY += changeY
        self.centerX += changeX
        self.centerY += changeY
        window.blit(self.image, (self.startX, self.startY))

# subclass for red enemy blast
class EnemyBlast(Blast):
    def __init__(self, startX, startY, endX, endY):
        super().__init__(startX, startY, endX, endY)
        # change the image
        image = pygame.image.load('enemyBlast.png')
        self.image = pygame.transform.scale(image, (15, 15))
        self.speed = 15
        self.damage = 10

# images of the different types of asteroids
a0 = pygame.image.load('asteroid0.png')
a1 = pygame.image.load('asteroid1.png')
a2 = pygame.image.load('asteroid2.png')
a3 = pygame.image.load('asteroid3.png')
a4 = pygame.image.load('asteroid4.png')

# asteroid images during collision
# found on google images
# filtered / changed color with windows photos app
ac0 = pygame.image.load('asteroid0Collide.png')
ac1 = pygame.image.load('asteroid1Collide.png')
ac2 = pygame.image.load('asteroid2Collide.png')
ac3 = pygame.image.load('asteroid3Collide.png')
ac4 = pygame.image.load('asteroid4Collide.png')

asteroids = [a0, a1, a2, a3, a4]
asteroidsCollide = [ac0, ac1, ac2, ac3, ac4]

class Asteroid(object):
    def __init__(self, targetX, targetY, startX = "a", startY = "a"):
        self.targetX = targetX
        self.targetY = targetY
        if startX == startY == "a":
            # picks a random corner to start from
            self.startX = random.choice([0, screenWidth])
            self.startY = random.choice([0, screenHeight])
        else:
            self.startX = startX
            self.startY = startY
        self.size = random.randint(40, 60)
        self.centerX = self.startX + self.size / 2
        self.centerY = self.startY + self.size / 2
        self.totalHealth = 20
        self.health = self.totalHealth
        # choose random speed for asteroid
        self.speed = random.randint(2, 4)
        self.vector = (self.targetX - self.startX, self.targetY - self.startY)
        self.unitVector = getUnitVector(self.vector)
        i = random.randint(0, 4)
        image = asteroids[i]
        imageCollide = asteroidsCollide[i]
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.imageCollide = pygame.transform.scale(imageCollide, (self.size, self.size))
        
    def drawAsteroid(self):
        # moves asteroid to where the player was located with the unit vector and speed
        changeX = self.speed * self.unitVector[0]
        changeY = self.speed * self.unitVector[1]
        self.startX += changeX
        self.startY += changeY
        self.centerX += changeX
        self.centerY += changeY
        if self.health == self.totalHealth:
            window.blit(self.image, (self.startX, self.startY))
        else:
            # if asteroid lost health, change the image to asteroid collided
            window.blit(self.imageCollide, (self.startX, self.startY))
        # draw health bar
        pygame.draw.rect(window, (255, 0, 0), \
            (self.startX, self.startY + self.size / 8, self.size, self.size / 20))
        pygame.draw.rect(window, (0, 255, 0), \
            (self.startX, self.startY + self.size / 8, \
                (self.health / self.totalHealth) * self.size, self.size / 20))

class EnemyShip(object):
    def __init__(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY
        bound = random.choice([1, 2, 3, 4])
        self.size = 200
        #left wall
        if bound == 1:
            self.startX = -self.size
            self.startY = random.randint(0, screenHeight)
        # top wall
        elif bound == 2:
            self.startX = random.randint(0, screenWidth)
            self.startY = -self.size
        # right wall
        elif bound == 3:
            self.startX = screenWidth
            self.startY = random.randint(0, screenHeight)
        # bottom wall
        else:
            self.startX = random.randint(0, screenWidth)
            self.startY = screenHeight
        self.centerX = self.startX + self.size / 2
        self.centerY = self.startY + self.size / 2
        self.speed = 3
        self.move = True
        self.shoot = not self.move
        self.image = 1
        self.counter = 0
        self.totalHealth = 500
        self.health = self.totalHealth

    def shoot(self, targetX, targetY):
        if isinstance(self, LargeShip):
            if self.shoot:
                game.missileList.append(Missile(self.centerX + 20, self.centerY + 20))
        else:
            if self.shoot:
                game.enemyBlastList.append(EnemyBlast(self.centerX + 20, self.centerY + 20, \
                    targetX + 10, targetY + 10))
        
    def drawShip(self):
        if self.move: 
            self.targetX = game.player.centerX
            self.targetY = game.player.centerY
            self.centerX = self.startX + self.size / 2
            self.centerY = self.startY + self.size / 2
            vector = (self.targetX - self.centerX, self.targetY - self.centerY)
            unitVector = getUnitVector(vector)
            # change the enemy position so that it follows the player
            changeX = unitVector[0] * self.speed
            changeY = unitVector[1] * self.speed
            self.startX += changeX
            self.centerX += changeX
            self.startY += changeY
            self.centerY += changeY
            d = distance(self.centerX, self.centerY, game.player.centerX, game.player.centerY)
            # for large ships, stops moving and starts shooting missiles
            if isinstance(self, LargeShip):
                if d <= min(screenWidth, screenHeight) / 2.25 and isInRange(self.centerX, self.centerY):
                    self.move = False
                    self.shoot = True
            # for small and medium ships, stops moving and starts shooting bullets
            else:
                if d <= min(screenWidth, screenHeight) / 3 and isInRange(self.centerX, self.centerY):
                    self.move = False
                    self.shoot = True
        else:
            self.counter += 1
            if self.counter % 30 == 0:
                EnemyShip.shoot(self, game.player.centerX, game.player.centerY)
        # rotate the ship so it points to the player center at all times
        angle = - getAngle(self.centerX, self.centerY, game.player.centerX, game.player.centerY)
        newImage = pygame.transform.rotate(self.image, angle)
        window.blit(newImage, (self.startX, self.startY))
        # health bar
        pygame.draw.rect(window, (255, 0, 0), (self.startX, \
            self.startY + self.size / 8, self.size, self.size / 20))
        pygame.draw.rect(window, (0, 255, 0), (self.startX, self.startY + self.size / 8, \
                (self.health / self.totalHealth) * self.size, self.size / 20))

class SmallShip(EnemyShip):
    def __init__(self, targetX, targetY):
        super().__init__(targetX, targetY)
        self.size = 40
        self.totalHealth = 20
        self.health = self.totalHealth
        self.image = pygame.image.load('smallShip.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

class MediumShip(EnemyShip):
    def __init__(self, targetX, targetY):
        super().__init__(targetX, targetY)
        self.size = 100
        self.totalHealth = 50
        self.health = self.totalHealth
        self.image = pygame.image.load('mediumShip.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

class LargeShip(EnemyShip):
    def __init__(self, targetX, targetY):
        super().__init__(targetX, targetY)
        self.size = 150
        self.totalHealth = 100
        self.health = self.totalHealth
        self.image = pygame.image.load('largeShip.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

# missile tracks the player position until collision
class Missile(object):
    def __init__(self, startX, startY):
        self.startX = startX
        self.startY = startY
        self.sizeX = 60
        self.sizeY = 30
        self.centerX = self.startX + self.sizeX / 2
        self.centerY = self.startY + self.sizeY / 2
        self.collided = False
        self.speed = 3
        self.totalHealth = 15
        self.health = self.totalHealth
        self.image = pygame.image.load('missile.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.sizeX, self.sizeY))

    def drawMissile(self):
        targetX = game.player.centerX
        targetY = game.player.centerY
        self.centerX = self.startX + self.sizeX / 2
        self.centerY = self.startY + self.sizeY / 2
        # move the missile towards the player
        vector = (targetX - self.centerX, targetY - self.centerY)
        unitVector = getUnitVector(vector)
        changeX = unitVector[0] * self.speed
        changeY = unitVector[1] * self.speed
        self.startX += changeX
        self.startY += changeY
        # rotate the missile to face the player
        angle = - getAngle(self.centerX, self.centerY, game.player.centerX, game.player.centerY)
        newImage = pygame.transform.rotate(self.image, angle)
        window.blit(newImage, (self.startX, self.startY))
        
# background images - multiple filters - changes with beat
bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))
bg1 = pygame.image.load('backgroundBeat1.jpg')
bg1 = pygame.transform.scale(bg1, (screenWidth, screenHeight))
bg2 = pygame.image.load('backgroundBeat2.jpg')
bg2 = pygame.transform.scale(bg2, (screenWidth, screenHeight))
bg3 = pygame.image.load('backgroundBeat3.jpg')
bg3 = pygame.transform.scale(bg3, (screenWidth, screenHeight))
bg4 = pygame.image.load('backgroundBeat4.jpg')
bg4 = pygame.transform.scale(bg4, (screenWidth, screenHeight))
# cursor image - target
cursor = pygame.image.load('targetAim.png')
cursorImage = pygame.transform.scale(cursor, (20, 20))
pauseButton = pygame.image.load('pauseButton.png')
pauseButton = pygame.transform.scale(pauseButton, (30, 30))
playButton = pygame.image.load('playButton.png')
playButton = pygame.transform.scale(playButton, (30, 30))
leftArrow = pygame.image.load('GreenArrow.png')
leftArrow = pygame.transform.scale(leftArrow, (40, 30))
rightArrow = pygame.transform.rotate(leftArrow, 180)
logo = pygame.image.load('titleLogo.jpg')
logo = pygame.transform.scale(logo, (300, 300))

def cursor(x, y):
    # puts target image over the cursor
    window.blit(cursorImage, (x, y))

# Game Class : contains the game loop , splashscreen and gameover screen
class Game(object):
    def __init__(self):
        self.running = False
        self.player = Player(screenWidth / 2 - 25, screenHeight / 2 - 25, 50)
        self.blastList = []
        self.asteroidList = []
        self.shipList = []
        self.enemyBlastList = []
        self.powerUpsOnSceen = []
        self.missileList = []
        self.asteroidsHit = 0
        self.smallShipsHit = 0
        self.mediumShipsHit = 0
        self.largeShipsHit = 0
        self.missilesHit = 0
        self.powerUpsUsed = 0
        self.clock = pygame.time.Clock()
        self.difficulty = None
        self.spawn = None
        self.additionalDamage = 0
        self.isBeat = 0
        self.fontName = pygame.font.match_font('Tomorrow')
        self.wavFiles = getWavFiles('./songs')
        self.mp3Files = getMP3Files('./songs')
        self.songNames = getSongNames(self.wavFiles)
        self.songNumber = 0
        self.mp3 = self.mp3Files[0]
        self.wav = self.wavFiles[0]
        self.song = pygame.mixer.music.load(self.mp3)
        audio = MP3(self.mp3)
        self.songLength = audio.info.length * 1000
        self.t = 0
        self.percent = 0

    # drawText function inspired by and modified from 
    # http://kidscancode.org/blog/2016/08/pygame_shmup_part_7/
    def drawText(self, text, centerX, centerY, size = 20, color=(255, 255, 255)):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textBox = textSurface.get_rect()
        textBox.midtop = (centerX, centerY)
        window.blit(textSurface, textBox)

    def mainMenu(self):
        waiting = True
        while waiting:
            window.blit(bg, (0,0))
            window.blit(logo, (screenWidth / 2 - 150, screenHeight / 6))
            playButton = Button("Choose Song", screenWidth / 3, screenHeight * 4 / 5, \
                screenWidth / 9, screenHeight / 12, 20)
            playButton.drawButton(window)
            helpButton = Button("How To Play", 2 * screenWidth / 3, screenHeight * 4 /5, \
                screenWidth / 9, screenHeight / 12, 20)
            helpButton.drawButton(window)
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if (playButton.x <= mouseX <= playButton.x + playButton.sizeX) and \
                        (playButton.y <= mouseY <= playButton.y + playButton.sizeY):
                        waiting = False
                        self.songScreen()
                    if (helpButton.x <= mouseX <= helpButton.x + helpButton.sizeX) and \
                        (helpButton.y <= mouseY <= helpButton.y + helpButton.sizeY):
                        waiting = False
                        self.instructionsScreen()
            pygame.draw.rect(window, SILVER, (0, screenHeight, screenWidth, infoHeight))
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            cursor(mx - 10, my - 10)
            pygame.display.update()

    def instructionsScreen(self):
        waiting = True
        self.player.y = screenHeight / 4
        while waiting:
            window.blit(bg, (0,0))
            self.drawText("Instructions", screenWidth / 2, screenHeight / 10, size = 70)
            self.drawText("Move the Player with the Arrow Keys", screenWidth / 2, screenHeight / 2 - 80, size = 20)
            self.drawText("Mouse Click to Shoot!", screenWidth / 2, screenHeight / 2 - 40, size = 20)
            self.drawText("Shoot down the asteroids and enemy ships for as long as you can until the song stops", \
                screenWidth / 2, screenHeight / 2 , size = 20)
            self.drawText("Collect Power Ups throughout the game", \
                screenWidth / 2, screenHeight / 2 + 40, size = 20)
            # draw Power ups
            self.drawText("Health Boost", \
                screenWidth / 5, screenHeight / 2 + 80, size = 20)
            health = MoreHealth(screenWidth * 3 /10, screenHeight / 2 + 95)
            health.drawPowerUp()
            self.drawText("Speed Boost", \
                screenWidth * 2 / 5, screenHeight / 2 + 80 , size = 20)
            speed = MoreSpeed(screenWidth / 2, screenHeight / 2 + 95)
            speed.drawPowerUp()
            self.drawText("Damage Boost", \
                screenWidth * 3 / 5, screenHeight / 2 + 80, size = 20)
            damage = MoreDamage(screenWidth *7/10, screenHeight / 2 + 95)
            damage.drawPowerUp()
            self.drawText("Destroy All", \
                screenWidth * 4 / 5, screenHeight / 2 + 80, size = 20)
            destroy = DestroyEnemies(screenWidth *9/10, screenHeight / 2 + 95)
            destroy.drawPowerUp()
            playButton = Button("Choose Song", screenWidth / 3, screenHeight * 4 / 5, \
                screenWidth / 9, screenHeight / 12, 20)
            playButton.drawButton(window)
            menuButton = Button("Return to Main Menu", 2 * screenWidth / 3, screenHeight * 4 /5, \
                screenWidth / 9, screenHeight / 12, 14)
            menuButton.drawButton(window)
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                # Move Player
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.yChange = -1
                    if (event.key == pygame.K_DOWN):
                        self.player.yChange = 1
                    if event.key == pygame.K_RIGHT:
                        self.player.xChange = 1
                    if event.key == pygame.K_LEFT:
                        self.player.xChange = -1
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_UP):
                        self.player.yChange = 0
                    if event.key == pygame.K_DOWN:
                        self.player.yChange = 0
                    if event.key == pygame.K_RIGHT:
                        self.player.xChange = 0
                    if event.key == pygame.K_LEFT:
                        self.player.xChange = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    self.blastList.append(Blast(self.player.centerX + 10, self.player.centerY + 10, \
                        mouseX + 10, mouseY + 10))
                    if (playButton.x <= mouseX <= playButton.x + playButton.sizeX) and \
                        (playButton.y <= mouseY <= playButton.y + playButton.sizeY):
                        waiting = False
                        self.songScreen()
                    if (menuButton.x <= mouseX <= menuButton.x + menuButton.sizeX) and \
                        (menuButton.y <= mouseY <= menuButton.y + menuButton.sizeY):
                        waiting = False
                        self.mainMenu()
            # moves the player   
            self.player.x, self.player.y = self.player.x + self.player.xChange * self.player.vel , \
                self.player.y + self.player.yChange * self.player.vel
            if self.player.x < 0:
                self.player.x = 0
            if self.player.x + self.player.size > screenWidth:
                self.player.x = screenWidth - self.player.size
            if self.player.y < 0:
                self.player.y = 0
            if self.player.y + self.player.size > screenHeight:
                self.player.y = screenHeight - self.player.size
            pygame.draw.rect(window, SILVER, (0, screenHeight, screenWidth, infoHeight))
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            # gets the rotation angle so player faces the cursor
            playerAngle = self.player.rotationAngle(mx, my)
            self.player.drawPlayer(playerAngle)
            for blast in self.blastList:
                blast.drawBlast()
                if not isInRange(blast.centerX, blast.centerY):
                    self.blastList.remove(blast)
            cursor(mx - 10, my - 10)
            pygame.display.update()

    def songScreen(self):
        self.difficulty = None
        self.spawn = None
        waiting = True
        quit = False
        # create the buttons and displays the songs
        # show difficulty and spawn options
        songButton = Button(f'{self.songNames[self.songNumber]}', screenWidth / 2,\
            screenHeight / 2, screenWidth / 2.5, screenHeight / 12, 20)
        easyButton = Button("Easy", screenWidth / 5, screenHeight * 7 / 10, \
                screenWidth / 9, screenHeight / 12, 20)
        mediumButton = Button("Medium", screenWidth * 2/ 5, screenHeight * 7 / 10, \
                screenWidth / 9, screenHeight / 12, 20)
        hardButton = Button("Hard", screenWidth * 3 / 5, screenHeight * 7 / 10, \
                screenWidth / 9, screenHeight / 12, 20)
        insaneButton = Button("Insane", screenWidth * 4 / 5, screenHeight * 7 / 10, \
                screenWidth / 9, screenHeight / 12, 20)
        beatButton = Button("Beat", screenWidth * 2 / 3, screenHeight * 10 / 11, \
                screenWidth / 9, screenHeight / 12, 20)
        randomButton = Button("Random", screenWidth / 3, screenHeight * 10 / 11, \
                screenWidth / 9, screenHeight / 12, 20)
        playButton = Button("Play", screenWidth / 2, screenHeight + infoHeight / 2, \
            screenWidth, infoHeight, 20)
        chooseText = False
        while waiting:
            window.blit(bg, (0,0))
            self.drawText("Choose Song", screenWidth / 2, screenHeight / 7, size = 70)
            self.drawText("Select Difficulty", screenWidth / 2, screenHeight *3/ 5, size = 20)
            self.drawText('Select How to Spawn Enemies', screenWidth / 2, screenHeight * 4 / 5, size = 20)
            songButton.drawButton(window)
            easyButton.drawButton(window)
            mediumButton.drawButton(window)
            hardButton.drawButton(window)
            insaneButton.drawButton(window)
            beatButton.drawButton(window)
            randomButton.drawButton(window)
            playButton.drawButton(window)
            window.blit(leftArrow, (screenWidth / 4, screenHeight / 2.1))
            window.blit(rightArrow, (screenWidth *3 / 4 - 40, screenHeight / 2.1))
            if chooseText:
                playButton.text = 'Choose Difficulty and Method Of Enemy Spawn Before Play'
            self.clock.tick(15)
            songButton.text = f'{self.songNames[self.songNumber]}'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if (easyButton.x <= mouseX <= easyButton.x + easyButton.sizeX) and \
                        (easyButton.y <= mouseY <= easyButton.y + easyButton.sizeY):
                        self.difficulty = 'Easy'
                        # change button background to green if selected
                        easyButton.selected = True
                        for button in [mediumButton, hardButton, insaneButton]:
                            button.selected = False
                        # waiting = False
                    if (mediumButton.x <= mouseX <= mediumButton.x + mediumButton.sizeX) and \
                        (mediumButton.y <= mouseY <= mediumButton.y + mediumButton.sizeY):
                        self.difficulty = 'Medium'
                        mediumButton.selected = True
                        for button in [easyButton, hardButton, insaneButton]:
                            button.selected = False
                        # waiting = False
                    if (hardButton.x <= mouseX <= hardButton.x + hardButton.sizeX) and \
                        (hardButton.y <= mouseY <= hardButton.y + hardButton.sizeY):
                        self.difficulty = 'Hard'
                        hardButton.selected = True
                        for button in [mediumButton, easyButton, insaneButton]:
                            button.selected = False
                        # waiting = False
                    if (insaneButton.x <= mouseX <= insaneButton.x + insaneButton.sizeX) and \
                        (insaneButton.y <= mouseY <= insaneButton.y + insaneButton.sizeY):
                        self.difficulty = 'Insane'
                        insaneButton.selected = True
                        for button in [mediumButton, hardButton, easyButton]:
                            button.selected = False
                        # waiting = False
                    if (beatButton.x <= mouseX <= beatButton.x + beatButton.sizeX) and \
                        (beatButton.y <= mouseY <= beatButton.y + beatButton.sizeY):
                        beatButton.selected = True
                        randomButton.selected = False
                        self.spawn = 'Beat'
                    if (randomButton.x <= mouseX <= randomButton.x + randomButton.sizeX) and \
                        (randomButton.y <= mouseY <= randomButton.y + randomButton.sizeY):
                        randomButton.selected = True
                        beatButton.selected = False
                        self.spawn = 'Random'
                    # check if arrow pressed, then change the song number, display a different song
                    if (screenWidth / 4 <= mouseX <= screenWidth / 4 + 40) and \
                        (screenHeight / 2.1 <= mouseY <= screenHeight / 2.1 + 30):
                        self.songNumber -= 1
                        if self.songNumber <= 0:
                            self.songNumber = 0
                    if (screenWidth *3 / 4 - 40 <= mouseX <= screenWidth *3 / 4) and \
                        (screenHeight / 2.1 <= mouseY <= screenHeight / 2.1 + 30):
                        self.songNumber += 1
                        if self.songNumber >= len(self.songNames) - 1:
                            self.songNumber = len(self.songNames) - 1
                    if (playButton.x <= mouseX <= playButton.x + playButton.sizeX) and \
                        (playButton.y <= mouseY <= playButton.y + playButton.sizeY):
                        if self.spawn != None and self.difficulty != None:
                            waiting = False
                        else:
                            chooseText = True
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            cursor(mx - 10, my - 10)
            pygame.display.update()
        if not quit:
            self.newGame()

    # reset the initial parameters
    def newGame(self):
        self.player = Player(screenWidth / 2 - 25, screenHeight / 2 - 25, 50)
        self.blastList = []
        self.asteroidList = []
        self.shipList = []
        self.enemyBlastList = []
        self.powerUpsOnSceen = []
        self.missileList = []
        self.asteroidsHit = 0
        self.smallShipsHit = 0
        self.mediumShipsHit = 0
        self.largeShipsHit = 0
        self.missilesHit = 0
        self.powerUpsUsed = 0
        self.clock = pygame.time.Clock()
        self.additionalDamage = 0
        self.isBeat = 0
        self.fontName = pygame.font.match_font('Arial')
        # set the mp3 and wav file to song selected
        self.mp3 = self.mp3Files[self.songNumber]
        self.wav = self.wavFiles[self.songNumber]
        self.song = pygame.mixer.music.load(self.mp3)
        self.times = getTimes(self.wav)
        # used to get the length of the MP3 file - uses mutagen library
        # https://stackoverflow.com/questions/6936393/find-the-length-of-a-song-with-pygame
        # user: HyopeR
        audio = MP3(self.mp3)
        # get length in milliseconds
        self.songLength = audio.info.length * 1000
        self.t = 0
        # score of the game is the percentage of the song completed
        self.percent = 0
        pygame.mixer.music.play()
        self.running = True
        self.run()
    
    def pauseScreen(self):
        waiting = True
        while waiting:
            window.blit(bg, (0,0))
            self.drawText(f'Song: {self.songNames[self.songNumber]}', screenWidth / 2, \
                screenHeight / 25, size = 20)
            self.drawText(f'Difficulty: {self.difficulty}', screenWidth / 2, \
                screenHeight / 25 + 40, size = 20)
            self.drawText("Paused", screenWidth / 2, screenHeight / 5, size = 70)
            # shows number of enemies destroyed and powerups used
            self.drawText(f"Asteroids Destroyed: {self.asteroidsHit}", screenWidth / 2, screenHeight / 2, size = 20)
            self.drawText(f"Small Ships Destroyed: {self.smallShipsHit}", screenWidth / 2, screenHeight / 2 + 40, size = 20)
            self.drawText(f"Medium Ships Destroyed: {self.mediumShipsHit}", screenWidth / 2, screenHeight / 2 + 80, size = 20)
            self.drawText(f"Large Ships Destroyed: {self.largeShipsHit}", screenWidth / 2, screenHeight / 2 + 120, size = 20)
            self.drawText(f"Missiles Destroyed: {self.missilesHit}", screenWidth / 2, screenHeight / 2 + 160, size = 20)
            self.drawText(f"Power Ups Used: {self.powerUpsUsed}", screenWidth / 2, screenHeight / 2 + 200, size = 20)
            self.drawText(f'Score: {self.percent}%', screenWidth / 2, screenHeight * 2/5, size = 30)
            # initialize resume and menu button
            resumeButton = Button("Resume", screenWidth / 3, screenHeight * 4 / 5, \
                screenWidth / 9, screenHeight / 12, 20)
            resumeButton.drawButton(window)
            menuButton = Button("Return to Main Menu", 2 * screenWidth / 3, screenHeight * 4 /5, \
                screenWidth / 9, screenHeight / 12, 14)
            menuButton.drawButton(window)
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if (screenWidth - 40 <= mouseX <= screenWidth) and \
                        (screenHeight <= mouseY <= screenHeight + infoHeight):
                        waiting = False
                        self.running = True
                        pygame.mixer.music.unpause()
                        self.run()
                    if (resumeButton.x <= mouseX <= resumeButton.x + resumeButton.sizeX) and \
                        (resumeButton.y <= mouseY <= resumeButton.y + resumeButton.sizeY):
                        waiting = False
                        self.running = True
                        pygame.mixer.music.unpause()
                        self.run()
                    if (menuButton.x <= mouseX <= menuButton.x + menuButton.sizeX) and \
                        (menuButton.y <= mouseY <= menuButton.y + menuButton.sizeY):
                        waiting = False
                        self.mainMenu()
            pygame.draw.rect(window, SILVER, (0, screenHeight, screenWidth, infoHeight))
            pygame.draw.rect(window, (255, 0, 0), (0, screenHeight, screenWidth / 3, infoHeight))
            pygame.draw.rect(window, (0, 255, 0), (0, screenHeight, \
                screenWidth * self.player.health / (3 * self.player.totalHealth), infoHeight))
            self.drawText(f'Health: {self.player.health} / {self.player.totalHealth}', screenWidth / 10 , screenHeight + 5, size = 30)
            window.blit(playButton, (screenWidth - 40, screenHeight + 10))
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            cursor(mx - 10, my - 10)
            pygame.display.update()

    def win(self):
        waiting = True
        while waiting:
            window.blit(bg, (0,0))
            self.drawText(f'Song: {self.songNames[self.songNumber]}', screenWidth / 2, \
                screenHeight / 25, size = 20)
            self.drawText(f'Difficulty: {self.difficulty}', screenWidth / 2, \
                screenHeight / 25 + 40, size = 20)
            self.drawText("You Win!!!", screenWidth / 2, screenHeight / 5, size = 70)
            # show stats of game
            self.drawText(f"Asteroids Destroyed: {self.asteroidsHit}", screenWidth / 2, screenHeight / 2, size = 20)
            self.drawText(f"Small Ships Destroyed: {self.smallShipsHit}", screenWidth / 2, screenHeight / 2 + 40, size = 20)
            self.drawText(f"Medium Ships Destroyed: {self.mediumShipsHit}", screenWidth / 2, screenHeight / 2 + 80, size = 20)
            self.drawText(f"Large Ships Destroyed: {self.largeShipsHit}", screenWidth / 2, screenHeight / 2 + 120, size = 20)
            self.drawText(f"Missiles Destroyed: {self.missilesHit}", screenWidth / 2, screenHeight / 2 + 160, size = 20)
            self.drawText(f"Power Ups Used: {self.powerUpsUsed}", screenWidth / 2, screenHeight / 2 + 200, size = 20)
            self.drawText('Your Score: 100%', screenWidth / 2, screenHeight *2 / 5, size = 30)
            replayButton = Button("Replay", screenWidth / 3, screenHeight * 4 / 5, \
                screenWidth / 9, screenHeight / 12, 20)
            replayButton.drawButton(window)
            menuButton = Button("Return to Main Menu", 2 * screenWidth / 3, screenHeight * 4 /5, \
                screenWidth / 9, screenHeight / 12, 14)
            menuButton.drawButton(window)
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if (replayButton.x <= mouseX <= replayButton.x + replayButton.sizeX) and \
                        (replayButton.y <= mouseY <= replayButton.y + replayButton.sizeY):
                        waiting = False
                        self.newGame()
                    if (menuButton.x <= mouseX <= menuButton.x + menuButton.sizeX) and \
                        (menuButton.y <= mouseY <= menuButton.y + menuButton.sizeY):
                        waiting = False
                        self.mainMenu()
            pygame.draw.rect(window, SILVER, (0, screenHeight, screenWidth, infoHeight))
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            cursor(mx - 10, my - 10)
            pygame.display.update()

    def gameOver(self):
        waiting = True
        while waiting:
            window.blit(bg, (0,0))
            self.drawText(f'Song: {self.songNames[self.songNumber]}', screenWidth / 2, \
                screenHeight / 25, size = 20)
            self.drawText(f'Difficulty: {self.difficulty}', screenWidth / 2, \
                screenHeight / 25 + 40, size = 20)
            self.drawText("GAME OVER", screenWidth / 2, screenHeight / 5, size = 70)
            # show stats of the game
            self.drawText(f"Asteroids Destroyed: {self.asteroidsHit}", screenWidth / 2, screenHeight / 2, size = 20)
            self.drawText(f"Small Ships Destroyed: {self.smallShipsHit}", screenWidth / 2, screenHeight / 2 + 40, size = 20)
            self.drawText(f"Medium Ships Destroyed: {self.mediumShipsHit}", screenWidth / 2, screenHeight / 2 + 80, size = 20)
            self.drawText(f"Large Ships Destroyed: {self.largeShipsHit}", screenWidth / 2, screenHeight / 2 + 120, size = 20)
            self.drawText(f"Missiles Destroyed: {self.missilesHit}", screenWidth / 2, screenHeight / 2 + 160, size = 20)
            self.drawText(f"Power Ups Used: {self.powerUpsUsed}", screenWidth / 2, screenHeight / 2 + 200, size = 20)
            self.drawText(f'Your Score: {self.percent}%', screenWidth / 2, \
                screenHeight * 2 / 5, size = 30)
            replayButton = Button("Replay", screenWidth / 3, screenHeight * 4 / 5, \
                screenWidth / 9, screenHeight / 12, 20)
            replayButton.drawButton(window)
            menuButton = Button("Return to Main Menu", 2 * screenWidth / 3, \
                screenHeight * 4 /5, screenWidth / 9, screenHeight / 12, 14)
            menuButton.drawButton(window)
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if (replayButton.x <= mouseX <= replayButton.x + replayButton.sizeX) and \
                        (replayButton.y <= mouseY <= replayButton.y + replayButton.sizeY):
                        waiting = False
                        self.newGame()
                    if (menuButton.x <= mouseX <= menuButton.x + menuButton.sizeX) and \
                        (menuButton.y <= mouseY <= menuButton.y + menuButton.sizeY):
                        waiting = False
                        self.mainMenu()
            pygame.draw.rect(window, SILVER, (0, screenHeight, screenWidth, infoHeight))
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            cursor(mx - 10, my - 10)
            pygame.display.update()


    def drawAll(self, mouseX, mouseY, playerAngle):
        # drawAll(self, mouseX, mouseY, playerAngle)
        # draw the player
        self.player.drawPlayer(playerAngle)
        # Draw the blasts and check if the blasts are in the boundaries
        for blast in self.blastList:
            if isInRange(blast.startX, blast.startY) and not blast.collided:
                blast.drawBlast()
            else: self.blastList.remove(blast)
        # draw the asteroids and check if they are in the bounds
        # Also check for asteroid and player collision
        for asteroid in self.asteroidList:
            if isCollision(asteroid.centerX, asteroid.centerY, asteroid.size, \
                self.player.centerX, self.player.centerY, self.player.size):
                self.player.health -= 10
                asteroid.health -= 5
            if not isInRange(asteroid.startX,asteroid.startY)\
                and not isInRange(asteroid.startX + asteroid.size, \
                    asteroid.startY + asteroid.size):
                self.asteroidList.remove(asteroid)
            if asteroid.health <= 0:
                self.asteroidList.remove(asteroid)
            asteroid.drawAsteroid()
        # check for blasts and asteroid collision and reduce asteroid health
        # if asteroid is destroyed, set up powerups
        randInt = random.randint(1, 100)
        for asteroid in self.asteroidList:
            for blast in self.blastList:
                if isCollision(asteroid.centerX, asteroid.centerY, asteroid.size, \
                    blast.centerX, blast.centerY, blast.size):
                    blast.collided = True
                    asteroid.health -= (blast.damage + self.additionalDamage)
                    if asteroid.health <= 0:
                        self.asteroidsHit += 1
                        # likeliness to get powerUps depend on difficulty
                        if self.difficulty == 'Easy':
                            if randInt in range(1, 31): 
                                powerUpNum = random.randint(1, 12)
                                if powerUpNum in range(1, 3):
                                    powerUp = DestroyEnemies(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(3, 6):
                                    powerUp = MoreHealth(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(6, 9):
                                    powerUp = MoreSpeed(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(9, 13):
                                    powerUp = MoreDamage(asteroid.centerX, asteroid.centerY)
                                self.powerUpsOnSceen.append(powerUp)
                        elif self.difficulty == 'Medium':
                            if randInt in range(1, 21): 
                                powerUpNum = random.randint(0, 20)
                                if powerUpNum in range(0, 3):
                                    powerUp = DestroyEnemies(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(3, 9):
                                    powerUp = MoreHealth(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(9, 15):
                                    powerUp = MoreSpeed(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(15, 21):
                                    powerUp = MoreDamage(asteroid.centerX, asteroid.centerY)
                                self.powerUpsOnSceen.append(powerUp)
                        elif self.difficulty == 'Hard' or self.difficulty == "Insane":
                            if randInt in range(1, 11): 
                                powerUpNum = random.randint(0, 20)
                                if powerUpNum in range(0, 3):
                                    powerUp = DestroyEnemies(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(3, 9):
                                    powerUp = MoreHealth(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(9, 15):
                                    powerUp = MoreSpeed(asteroid.centerX, asteroid.centerY)
                                elif powerUpNum in range(15, 21):
                                    powerUp = MoreDamage(asteroid.centerX, asteroid.centerY)
                                self.powerUpsOnSceen.append(powerUp)
        # draw missile and check for missile / blast and missile / player collision
        for missile in self.missileList:
            missile.drawMissile()
            for blast in self.blastList:
                if isCollision(blast.centerX, blast.centerY, blast.size, \
                    missile.centerX, missile.centerY, missile.sizeX):
                    blast.collided = True
                    missile.health -= (blast.damage + self.additionalDamage)
            if missile.health <= 0:
                self.missilesHit += 1
                self.missileList.remove(missile)
            elif isCollision(self.player.centerX, self.player.centerY, self.player.size, \
                missile.centerX, missile.centerY, missile.sizeX):
                self.player.health -= 15
                self.missileList.remove(missile)
        # draw enemy ships, add to power up list if enemy is destroyed
        for enemy in self.shipList:
            if enemy.health <= 0:
                # likeliness of power up depends on difficulty
                # higher the difficulty --> less of a chance for power up
                if self.difficulty == 'Easy':
                    if randInt in range(1, 31): 
                        powerUpNum = random.randint(1, 12)
                        if powerUpNum in range(1, 3):
                            powerUp = DestroyEnemies(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(3, 6):
                            powerUp = MoreHealth(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(6, 9):
                            powerUp = MoreSpeed(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(9, 13):
                            powerUp = MoreDamage(enemy.centerX, enemy.centerY)
                        self.powerUpsOnSceen.append(powerUp)
                elif self.difficulty == 'Medium':
                    if randInt in range(1, 25): 
                        powerUpNum = random.randint(0, 20)
                        if powerUpNum in range(0, 3):
                            powerUp = DestroyEnemies(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(3, 9):
                            powerUp = MoreHealth(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(9, 15):
                            powerUp = MoreSpeed(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(15, 21):
                            powerUp = MoreDamage(enemy.centerX, enemy.centerY)
                        self.powerUpsOnSceen.append(powerUp)
                elif self.difficulty == 'Hard' or self.difficulty == "Insane":
                    if randInt in range(1, 20): 
                        powerUpNum = random.randint(0, 20)
                        if powerUpNum in range(0, 3):
                            powerUp = DestroyEnemies(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(3, 9):
                            powerUp = MoreHealth(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(9, 15):
                            powerUp = MoreSpeed(enemy.centerX, enemy.centerY)
                        elif powerUpNum in range(15, 21):
                            powerUp = MoreDamage(enemy.centerX, enemy.centerY)
                        self.powerUpsOnSceen.append(powerUp)
                # keep track of number of ships destroyed
                if isinstance(enemy, SmallShip):
                    self.smallShipsHit += 1
                elif isinstance(enemy, MediumShip):
                    self.mediumShipsHit += 1
                elif isinstance(enemy, LargeShip):
                    self.largeShipsHit += 1
                self.shipList.remove(enemy)
            enemy.drawShip()
        # draw blasts and remove if it has already collided with something or it is off the screen
        for blast in self.enemyBlastList:
            if isInRange(blast.startX, blast.startY) and not blast.collided:
                blast.drawBlast()
            else: self.enemyBlastList.remove(blast)
        # collision between blast and enemies
        for enemy in self.shipList:
            for blast in self.blastList:
                if isCollision(enemy.centerX, enemy.centerY, enemy.size, \
                    blast.centerX, blast.centerY, blast.size):
                    enemy.health -= (blast.damage + self.additionalDamage)
                    blast.collided = True
        for blast in self.enemyBlastList:
            if isCollision(self.player.centerX, self.player.centerY, self.player.size, \
                blast.centerX, blast.centerY, blast.size):
                self.player.health -= 10
                blast.collided = True
        # draw each power up on the screen
        for powerUp in self.powerUpsOnSceen:
            powerUp.drawPowerUp()
            if not isInRange(powerUp.x, powerUp.y) or not isInRange(powerUp.x +\
                 powerUp.size, powerUp.y + powerUp.size):
                 self.powerUpsOnSceen.remove(powerUp)
            # if power up collides with the player, apply the effects
            elif isCollision(self.player.centerX, self.player.centerY, \
                self.player.size, powerUp.x, powerUp.y, powerUp.size):
                # add to game stats
                self.powerUpsUsed += 1
                if isinstance(powerUp, DestroyEnemies):
                    # clears enemies
                    self.shipList = []
                    self.asteroidList = []
                    self.enemyBlastList = []
                    self.missileList = []
                elif isinstance(powerUp, MoreHealth):
                    self.player.health += 100
                    if self.player.health >= self.player.totalHealth:
                        self.player.health = self.player.totalHealth
                elif isinstance(powerUp, MoreDamage):
                    self.additionalDamage += 5
                elif isinstance(powerUp, MoreSpeed):
                    self.player.vel += 0.5
                self.powerUpsOnSceen.remove(powerUp)
        pygame.draw.rect(window, SILVER, (0, screenHeight, screenWidth, infoHeight))
        # draw Pause button
        window.blit(pauseButton, (screenWidth - 40, screenHeight + 10))
        pygame.draw.rect(window, (255, 0, 0), (0, screenHeight, screenWidth / 3, infoHeight))
        pygame.draw.rect(window, (0, 255, 0), (0, screenHeight, \
            screenWidth * self.player.health / (3 * self.player.totalHealth), infoHeight))
        pygame.draw.rect(window, (0, 0, 255), (0, screenHeight - 10, \
            screenWidth * self.t / self.songLength, 10))
        self.drawText(f'Health: {self.player.health} / {self.player.totalHealth}', \
            screenWidth / 10 , screenHeight + 5, size = 30)
        self.drawText(f'Difficulty: {self.difficulty}', screenWidth / 2, \
            screenHeight + 5, size = 30, color = BLACK)
        # show score / percentage of song completed
        self.drawText(f'Completed: {self.percent} %', screenWidth * 3 / 4, \
            screenHeight + 5, size = 30, color = BLACK)
        # draw the cursor with a helper function
        cursor(mouseX - 10, mouseY - 10)
        pygame.display.update()

    def run(self):
        while self.running:
            t = pygame.mixer.music.get_pos()
            # change the background every beat
            if self.isBeat % 10 == 0 or self.isBeat % 10 == 9:
                window.blit(bg, (0, 0))
            elif self.isBeat % 10 == 1 or self.isBeat % 10 == 8:
                window.blit(bg1, (0, 0))
            elif self.isBeat % 10 == 2 or self.isBeat % 10 == 7:
                window.blit(bg2, (0, 0))
            elif self.isBeat % 10 == 3 or self.isBeat % 10 == 6:
                window.blit(bg3, (0, 0))
            if self.isBeat % 10 == 4 or self.isBeat % 10 == 5:
                window.blit(bg4, (0, 0))
            self.clock.tick(30)
            # check the events
            # code from https://www.pygame.org/docs/ref/key.html
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.yChange = -1
                    if (event.key == pygame.K_DOWN):
                        self.player.yChange = 1
                    if event.key == pygame.K_RIGHT:
                        self.player.xChange = 1
                    if event.key == pygame.K_LEFT:
                        self.player.xChange = -1
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_UP):
                        self.player.yChange = 0
                    if event.key == pygame.K_DOWN:
                        self.player.yChange = 0
                    if event.key == pygame.K_RIGHT:
                        self.player.xChange = 0
                    if event.key == pygame.K_LEFT:
                        self.player.xChange = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if (screenWidth - 40 <= mouseX <= screenWidth) and \
                        (screenHeight <= mouseY <= screenHeight + infoHeight):
                        self.running = False
                        pygame.mixer.music.pause()
                        self.pauseScreen()
                    self.blastList.append(Blast(self.player.centerX + 10, \
                        self.player.centerY + 10, mouseX + 10, mouseY + 10)) 
            # moves the player   
            self.player.x, self.player.y = self.player.x + self.player.xChange * self.player.vel , \
                self.player.y + self.player.yChange * self.player.vel
            if self.player.x < 0:
                self.player.x = 0
            if self.player.x + self.player.size > screenWidth:
                self.player.x = screenWidth - self.player.size
            if self.player.y < 0:
                self.player.y = 0
            if self.player.y + self.player.size > screenHeight:
                self.player.y = screenHeight - self.player.size
            # hide cursor and set cursor image
            pygame.mouse.set_visible(False)
            self.t = pygame.mixer.music.get_pos()
            percent = self.t * 100/ self.songLength
            self.percent = round(percent, 1)
            # if player chose random mode: enemies spawn randomly
            if self.spawn == "Random":
                randomNum = random.randint(1, 1000)
                if self.difficulty == "Easy":
                    if randomNum > 998:
                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                    # generate small or medium ship
                    if randomNum < 5:
                        randTypeShip= random.randint(1, 100)
                        if randTypeShip < 70:
                            self.shipList.append(SmallShip(self.player.centerX, self.player.centerY))
                        else:
                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                elif self.difficulty == "Medium":
                    if randomNum > 995:
                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                    # generate small or medium ship
                    if randomNum < 10:
                        randTypeShip= random.randint(1, 100)
                        if randTypeShip < 60:
                            self.shipList.append(SmallShip(self.player.centerX, self.player.centerY))
                        else:
                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                elif self.difficulty == "Hard":
                    if randomNum > 990:
                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                    # generate small, medium, or large ship
                    # greater chance to appear per frame than small and medium
                    if randomNum < 15:
                        randTypeShip= random.randint(1, 100)
                        if randTypeShip < 45:
                            self.shipList.append(SmallShip(self.player.centerX, self.player.centerY))
                        elif randTypeShip < 80:
                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                        else:
                            self.shipList.append(LargeShip(self.player.x, self.player.y))
                elif self.difficulty == "Insane":
                    if randomNum > 980:
                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                    # generate small medium or large ship
                    # generated enemies most frequently
                    if randomNum < 20:
                        randTypeShip= random.randint(1, 100)
                        if randTypeShip < 40:
                            self.shipList.append(SmallShip(self.player.centerX, self.player.centerY))
                        elif randTypeShip < 75:
                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                        else:
                            self.shipList.append(LargeShip(self.player.x, self.player.y))
            if len(self.times) >= 1:
                if self.times[0] <= t:
                    # if player chose to spawn enemies on beat
                    # similar ot random: harder the difficulty --> more frequent 
                    # enemy spawns
                    if self.spawn == "Beat":
                        if self.difficulty == "Easy":
                            randNum = random.randint(0, 100)
                            if randNum < 20:
                                randEnemy = random.randint(1, 10)
                                if randEnemy < 8:
                                    if len(self.asteroidList) < 10:
                                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                                else:
                                    if len(self.shipList) < 8:
                                        randShip = random.randint(1, 4)
                                        if randShip == 4:
                                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                                        else:
                                            self.shipList.append(SmallShip(self.player.x, self.player.y))
                        elif self.difficulty == "Medium":
                            randNum = random.randint(0, 100)
                            if randNum < 33:
                                randEnemy = random.randint(1, 10)
                                if randEnemy < 7:
                                    if len(self.asteroidList) < 15:
                                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                                else:
                                    if len(self.shipList) < 10:
                                        randShip = random.randint(1, 5)
                                        if randShip > 3:
                                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                                        else:
                                            self.shipList.append(SmallShip(self.player.x, self.player.y))
                        elif self.difficulty == "Hard":
                            randNum = random.randint(0, 100)
                            if randNum < 35:
                                randEnemy = random.randint(1, 10)
                                if randEnemy < 5:
                                    if len(self.asteroidList) < 25:
                                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                                else:
                                    if len(self.shipList) < 15:
                                        randShip = random.randint(1, 10)
                                        if randShip > 5:
                                            self.shipList.append(SmallShip(self.player.x, self.player.y))
                                        elif randShip > 1:
                                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                                        else:
                                            self.shipList.append(LargeShip(self.player.x, self.player.y))
                        elif self.difficulty == "Insane":
                            randNum = random.randint(0, 100)
                            if randNum < 50:
                                randEnemy = random.randint(1, 10)
                                if randEnemy < 6:
                                    if len(self.asteroidList) < 25:
                                        self.asteroidList.append(Asteroid(self.player.x, self.player.y))
                                else:
                                    if len(self.shipList) < 20:
                                        randShip = random.randint(1, 10)
                                        if randShip > 5:
                                            self.shipList.append(SmallShip(self.player.x, self.player.y))
                                        elif randShip > 2:
                                            self.shipList.append(MediumShip(self.player.x, self.player.y))
                                        else:
                                            self.shipList.append(LargeShip(self.player.x, self.player.y))
                    self.isBeat += 1
                    self.times.pop(0)
            # check the mouse position for player rotation
            mouseX, mouseY = pygame.mouse.get_pos()
            playerAngle = self.player.rotationAngle(mouseX, mouseY)
            # if song is over player wins
            if self.percent >= 99.9:
                self.running = False
                pygame.mixer.music.stop()
                self.win()
            # if player dies, go to game over mode
            if self.player.health <= 0:
                self.running = False
                pygame.mixer.music.stop()
                self.gameOver()
            self.drawAll(mouseX, mouseY, playerAngle)

pygame.init()
game = Game()
game.mainMenu()
pygame.quit()