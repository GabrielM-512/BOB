import pygame

import random
import math

from src.globals.time import deltaTime


class RedEnemy:
    def __init__(self):
        self.hitbox = pygame.Rect((0, 0), (40, 40))
        self.hitbox.y = -100
        self.hitbox.x = random.randint(40, 1240)

        self.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5)

    def move(self):
        self.hitbox.y += self.falling_speed * deltaTime

        # delete the enemy if it is below the screen
        if self.hitbox.top > 720:
            del self

    def draw(self, canvas):
        pygame.draw.circle(canvas, (255, 0, 0), self.hitbox.center, 40, 0)
