import pygame
from pygame import mixer
import math, random, time


# set up the window sizes
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

pygame.display.set_caption('Beat Hazard')

# colors of the objects
PLAYER = (96, 96, 96)
ENEMY = (255, 0, 0)
POWERUP = (0, 255, 0)

class Game(object):
    # initialize the game
    def __init__(self):
        pygame.init()
        mainClock = pygame.time.Clock()
        pygame.display.set_caption("Beat Hazard")


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class EnemyShip(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def shoot(self, direction):
        pass

class SmallEnemyShip(EnemyShip):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 20
        self.health = 20
        self.image = pygame.image.load('smallShip.png')

class MediumEnemyShip(EnemyShip):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 50
        self.health = 100

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


