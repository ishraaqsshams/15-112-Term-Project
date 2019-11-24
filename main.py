import pygame
from pygame import mixer
from pygame.locals import *
import math, random, time, sys

# set up the window sizes
screenWidth = 1000
screenHeight = 600
window = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
pygame.display.set_caption('Beat Hazard')

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
        self.health = 500
        self.image = pygame.image.load('Player.png')
        self.playerImage = pygame.transform.scale(self.image, (self.size, self.size))

    def rotationAngle(self, mouseX, mouseY):
        '''
        takes the mouse position and returns the angle in degrees the player 
        image must rotate to follow the cursor
        Param: 2 ints
        Returns: angle, int
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

    def playerCollision(self):
        '''
        If player collides with enemy, it loses 10 health points
        Param: self
        return: None
        '''
        self.health -= 10
    
    def usePowerUp(self):
        pass

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

class Blast(object):
    def __init__(self, startX, startY, endX, endY):
        self.size = 20
        self.startX = startX -20
        self.startY = startY -20
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
        # self.image = pygame.transform.flip(image, True, True)    

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


class EnemyBlast(Blast):
    def __init__(self, startX, startY, endX, endY):
        super().__init__(startX, startY, endX, endY)
        # change the image
        image = pygame.image.load('enemyBlast.png')
        self.image = pygame.transform.scale(image, (15, 15))
        self.speed = 15

# images of the different types of asteroids
# found on google images
a0 = pygame.image.load('asteroid0.png')
a1 = pygame.image.load('asteroid1.png')
a2 = pygame.image.load('asteroid2.png')
a3 = pygame.image.load('asteroid3.png')
a4 = pygame.image.load('asteroid4.png')

# asteroid images during collision
# found on google images
ac0 = pygame.image.load('asteroid0Collide.png')
ac1 = pygame.image.load('asteroid1Collide.png')
ac2 = pygame.image.load('asteroid2Collide.png')
ac3 = pygame.image.load('asteroid3Collide.png')
ac4 = pygame.image.load('asteroid4Collide.png')

asteroids = [a0, a1, a2, a3, a4]
asteroidsCollide = [ac0, ac1, ac2, ac3, ac4]

class Asteroid(object):
    def __init__(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY
        self.startX = random.choice([0, screenWidth])
        self.startY = random.choice([0, screenHeight])
        self.size = random.randint(40, 60)
        self.centerX = self.startX + self.size / 2
        self.centerY = self.startY + self.size / 2
        self.gotHit = 0
        self.speed = random.randint(2, 4)
        self.vector = (self.targetX - self.startX, self.targetY - self.startY)
        self.unitVector = getUnitVector(self.vector)
        i = random.randint(0, 4)
        image = asteroids[i]
        imageCollide = asteroidsCollide[i]
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.imageCollide = pygame.transform.scale(imageCollide, (self.size, self.size))
        

    def drawAsteroid(self):
        # moves asteroid to where the player was located
        changeX = self.speed * self.unitVector[0]
        changeY = self.speed * self.unitVector[1]
        self.startX += changeX
        self.startY += changeY
        self.centerX += changeX
        self.centerY += changeY
        if self.gotHit == 0:
            window.blit(self.image, (self.startX, self.startY))
        else:
            window.blit(self.imageCollide, (self.startX, self.startY))

class EnemyShip(object):
    def __init__(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY
        bound = random.choice([1, 2, 3, 4])
        #left wall
        if bound == 1:
            self.startX = 0
            self.startY = random.randint(0, screenHeight)
        # top wall
        elif bound == 2:
            self.startX = random.randint(0, screenWidth)
            self.startY = 0
        # right wall
        elif bound == 3:
            self.startX = screenWidth
            self.startY = random.randint(0, screenHeight)
        else:
            self.startX = random.randint(0, screenWidth)
            self.startY = screenHeight
        self.size = 200
        self.centerX = self.startX + self.size / 2
        self.centerY = self.startY + self.size / 2
        self.speed = 3
        self.move = True
        self.shoot = not self.move
        self.image = 1
        self.counter = 0

            
    def shoot(self, targetX, targetY):
        if self.shoot:
            enemyBlastList.append(EnemyBlast(self.centerX + 20, self.centerY + 20, \
                targetX + 10, targetY + 10))
        
    def drawShip(self):
        if self.move:
            self.targetX = player.centerX
            self.targetY = player.centerY
            self.centerX = self.startX + self.size / 2
            self.centerY = self.startY + self.size / 2
            vector = (self.targetX - self.centerX, self.targetY - self.centerY)
            unitVector = getUnitVector(vector)
            changeX = unitVector[0] * self.speed
            changeY = unitVector[1] * self.speed
            self.startX += changeX
            self.centerX += changeX
            self.startY += changeY
            self.centerY += changeY
            d = distance(self.centerX, self.centerY, player.centerX, player.centerY)
            if d <= min(screenWidth, screenHeight) / 3:
                self.move = False
                self.shoot = True
        else:
            self.counter += 1
            if self.counter % 30 == 0:
                EnemyShip.shoot(self, player.centerX, player.centerY)
        # rotate the ship so it points to the player center at all times
        angle = - getAngle(self.centerX, self.centerY, player.centerX, player.centerY)
        newImage = pygame.transform.rotate(self.image, angle)
        window.blit(newImage, (self.startX, self.startY))


class SmallShip(EnemyShip):
    def __init__(self, targetX, targetY):
        super().__init__(targetX, targetY)
        self.size = 50
        self.health = 20
        self.image = pygame.image.load('smallShip.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

class MediumShip(EnemyShip):
    def __init__(self, targetX, targetY):
        super().__init__(targetX, targetY)
        self.size = 100
        self.health = 50
        self.image = pygame.image.load('mediumShip.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

class LargeShip(EnemyShip):
    def __init(self, x, y):
        super().__init__(x, y)
        self.size = 80
        self.health = 100

bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))
cursor = pygame.image.load('targetAim.png')
cursorImage = pygame.transform.scale(cursor, (20, 20))

def cursor(x, y):
    # puts target image over the cursor
    window.blit(cursorImage, (x, y))

def drawAll(mouseX, mouseY, angle):
    window.blit(bg, (0, 0))
    # draw the player
    player.drawPlayer(angle)
    # Draw the blasts and check if the blasts are in the boundaries
    for blast in blastList:
        if isInRange(blast.startX, blast.startY) and not blast.collided:
            blast.drawBlast()
        else: blastList.remove(blast)
    # draw the asteroids and check if they are in the bounds
    # Also check for asteroid and player collision
    for asteroid in asteroidList:
        asteroid.drawAsteroid()
        if isCollision(asteroid.centerX, asteroid.centerY, asteroid.size, \
            player.centerX, player.centerY, player.size):
            player.health -= 20
            asteroid.gotHit += 0.5
        if not isInRange(asteroid.startX,asteroid.startY)\
            and not isInRange(asteroid.startX + asteroid.size, \
                 asteroid.startY + asteroid.size):
            asteroidList.remove(asteroid)
        elif asteroid.gotHit >= 2:
            asteroidList.remove(asteroid)
    # draw ships
    # check for blasts and asteroid collision
    for asteroid in asteroidList:
        for blast in blastList:
            if isCollision(asteroid.centerX, asteroid.centerY, asteroid.size, \
                blast.centerX, blast.centerY, blast.size):
                blast.collided = True
                asteroid.gotHit += 1
    for enemy in shipList:
        enemy.drawShip()
        if enemy.health <= 0:
            shipList.remove(enemy)
    for blast in enemyBlastList:
        if isInRange(blast.startX, blast.startY) and not blast.collided:
            blast.drawBlast()
        else: enemyBlastList.remove(blast)
    for enemy in shipList:
        for blast in blastList:
            if isCollision(enemy.centerX, enemy.centerY, enemy.size, \
                blast.centerX, blast.centerY, blast.size):
                enemy.health -= 10
                blast.collided = True
    for blast in enemyBlastList:
        if isCollision(player.centerX, player.centerY, player.size, \
            blast.centerX, blast.centerY, blast.size):
            player.health -= 10
            blast.collided = True
    # draw the cursor with a helper function
    cursor(mouseX - 10, mouseY - 10)
    pygame.display.update()

# main loop
player = Player(screenWidth / 2 - 25, screenHeight / 2 - 25, 50)
blastList = []
asteroidList = []
shipList = []
enemyBlastList = []

running = True
clock = pygame.time.Clock()
while running:
    # pygame.time.delay(25)
    clock.tick(30)
    # check the events
    # code from https://www.pygame.org/docs/ref/key.html
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
            if (event.key == pygame.K_UP):
                player.yChange = 0
            if event.key == pygame.K_DOWN:
                player.yChange = 0
            if event.key == pygame.K_RIGHT:
                player.xChange = 0
            if event.key == pygame.K_LEFT:
                player.xChange = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            blastList.append(Blast(player.centerX + 10, \
                player.centerY + 10, mouseX + 10, mouseY + 10))    
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
    # generate Asteroid at random time
    # replace later with the beat of the song
    randomNum = random.randint(1, 1000)
    if randomNum > 995:
        asteroidList.append(Asteroid(player.x, player.y))
    # generate small ship
    if randomNum < 4: 
        randTypeShip= random.randint(1, 100)
        if randTypeShip < 75:
            shipList.append(SmallShip(player.centerX, player.centerY))
        else:
            shipList.append(MediumShip(player.x, player.y))
    # check the mouse position for player rotation
    mouseX, mouseY = pygame.mouse.get_pos()
    playerAngle = player.rotationAngle(mouseX, mouseY)
    drawAll(mouseX, mouseY, playerAngle)

pygame.quit()
