import pygame
from pygame import mixer
from pygame.locals import *
import math, random, time, sys


# set up the window sizes
screenWidth = 400
screenHeight = 400
window = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)

pygame.display.set_caption('Beat Hazard')

# colors of the objects
PLAYER = (255, 96, 96)
ENEMY = (255, 0, 0)
POWERUP = (0, 255, 0)


class Player(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.xChange = 0
        self.yChange = 0
        self.vel = 3
        self.health = 500
        self.image = pygame.image.load('Player.png')
        self.playerImage = pygame.transform.scale(self.image, (self.size, self.size))

    def rotationAngle(self, mouseX, mouseY):
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

    def playerCollision(self):
        self.health -= 10
        return self.health
    
    def usePowerUp(self):
        pass

    def drawPlayer(self, angle = 0):
        # from https://www.pygame.org/docs/ref/transform.html 
        newPlayerImage = pygame.transform.rotate(self.playerImage, angle // 1)
        window.blit(newPlayerImage, (self.x, self.y))

class Blast(object):
    def __init__(self, startX, startY, endX, endY):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.speed = 5
        image = pygame.image.load('blast.png')
        self.image = pygame.transform.flip(image, False, True)

    @staticmethod
    def getAngle(startX, startY, endX, endY):
        changeX = endX - startX
        changeY = - endY + startY
        if changeX == 0:
            if changeY >= 0:
                return 90
            else:
                return 270
        if changeX < 0:
            diff = startX - endX
            angle = 180 + Blast.getAngle(startX, startY, startX + diff, endY)
            if endY == 0:
                return 180
            elif endY > 0:
                return 180 - angle
            elif endY < 0:
                return - abs(180 + angle)
        angle = math.atan(changeY / changeX)
        degrees = angle * 180 / math.pi
        print(degrees)
        return degrees

    def fire(self):
        return Blast.getAngle(self.startX + player.size / 2, \
            self.startY + player.size / 2, self.endX, self.endY)

    def drawBlast(self):
        pass

class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def getBounds(x, y, width, height):
        pass

class EnemyShip(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def shoot(self, direction):
        pass

class SmallEnemyShip(EnemyShip):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size
        self.health = 20
        self.image = pygame.image.load('smallShip.png')

class MediumEnemyShip(EnemyShip):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 50
        self.health = 100
        # self.image = pygame.image.load('mediumShip.png')

class LargeEnemyShip(EnemyShip):
    def __init(self, x, y):
        super().__init__(x, y)
        self.size = 80
        self.health = 400

class Asteroid(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = random.randint(40, 60)
        self.size = self.health

bg = pygame.image.load('background.jpg')
cursor = pygame.image.load('targetAim.png')
cursorImage = pygame.transform.scale(cursor, (20, 20))

def cursor(x, y):
    window.blit(cursorImage, (x, y))

def drawAll(mouseX, mouseY, angle):
    window.blit(bg, (0, 0))
    # draw rectangle
    # pygame.draw.rect(window, PLAYER, \
    #     (player.x, player.y, player.size, player.size))
    player.drawPlayer(angle)
    cursor(mouseX - 10, mouseY - 10)
    pygame.display.update()

# main loop
player = Player(screenWidth / 2 - 25, screenHeight / 2 - 25, 50)
running = True
while running:
    pygame.time.delay(25)
    # check the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.yChange = -1
            if (event.key == pygame.K_DOWN):
                player.yChange = 1
            if event.key == pygame.K_RIGHT:
                player.xChange = 1
            if event.key == pygame.K_LEFT:
                player.xChange = -1
            if event.key == pygame.K_SPACE:
                player.usePowerUp
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_UP) :
                player.yChange = 0
            if event.key == pygame.K_DOWN:
                player.yChange = 0
            if event.key == pygame.K_RIGHT:
                player.xChange = 0
            if event.key == pygame.K_LEFT:
                player.xChange = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            blast = Blast(player.x, player.y, mouseX, mouseY)
            blast.fire()
    player.x, player.y = player.x + player.xChange * player.vel , \
        player.y + player.yChange * player.vel
    if player.x < 0:
        player.x = 0
    if player.x + player.size > screenWidth:
        player.x = screenWidth - player.size
    if player.y < 0:
        player.y = 0
    if player.y + player.size > screenHeight:
        player.y = screenHeight - player.size
    # hide cursor and set cursor image
    pygame.mouse.set_visible(False)
    # check the mouse position for rotation
    mouseX, mouseY = pygame.mouse.get_pos()
    playerAngle = player.rotationAngle(mouseX, mouseY)
    drawAll(mouseX, mouseY, playerAngle)

pygame.quit()
