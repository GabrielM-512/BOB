import pygame

import random
import math

from src.globals.time import deltaTime
import src.globals.globalVariables as global_variables


class RedEnemy:
    def __init__(self):
        self.hitbox = pygame.Rect((0, 0), (80, 80))
        self.hitbox.y = -100 + random.randint(-20, 20)
        self.hitbox.x = random.randint(40, 1240)

        self.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5) * 4

        for game_object in global_variables.objects:
            if game_object.type == "RED_ENEMY":
                while self.falling_speed == game_object.falling_speed:
                    self.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5) * 4

        self.type = "RED_ENEMY"

        global_variables.objects.append(self)

    def move(self):
        self.hitbox.y += self.falling_speed * deltaTime * global_variables.ball_movement_mult

        # teleport the enemy back up if it is below the screen
        if self.hitbox.top > 720:
            global_variables.score += 1

            self.hitbox.y = -100 + random.randint(-20, 20)
            self.hitbox.x = random.randint(40, 1240)
            self.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5) * 4

            for game_object in global_variables.objects:
                if game_object.type == "RED_ENEMY":
                    while self.falling_speed == game_object.falling_speed and game_object != self:
                        self.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5) * 4

    def draw(self, canvas):
        pygame.draw.circle(canvas, (255, 0, 0), self.hitbox.center, 40, 0)
