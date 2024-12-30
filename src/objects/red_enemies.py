import pygame

import random
import math

import src.globals.time as time
import src.globals.globalVariables as global_variables


class RedEnemy:
    def __init__(self, id):

        self.type = "RED_ENEMY"
        self.id = id

        self.hitbox = pygame.Rect((0, 0), (80, 80))
        self.hitbox.y = -100 + random.randint(-20, 20)
        self.hitbox.x = random.randint(40, 1240)

        self.falling_speed = math.pow(random.uniform(0.5, 1), 2)

        for game_object in global_variables.objects:
            if game_object.type == "RED_ENEMY" and game_object != self:
                while self.falling_speed == game_object.falling_speed:
                    self.falling_speed = math.pow(random.uniform(0.5, 1), 2)

        global_variables.objects.append(self)

    def reset(self):  # resets the ball if it is below the screen or the game is reset
        self.hitbox = pygame.Rect((0, 0), (80, 80))
        self.hitbox.y = -100 + random.randint(-20, 20)
        self.hitbox.x = random.randint(40, 1240)

        self.falling_speed = math.pow(random.uniform(0.5, 1), 2)

        for game_object in global_variables.objects:
            if game_object.type == "RED_ENEMY" and game_object != self:
                while self.falling_speed == game_object.falling_speed:
                    self.falling_speed = math.pow(random.uniform(0.5, 1), 2)

    def move(self):
        self.hitbox.y += max(self.falling_speed * time.deltaTime * global_variables.ball_movement_mult, 1)  # ensure the ball falls with at least 1px/frame, otherwise it won't at all

        # teleport the enemy back up if it is below the screen
        if self.hitbox.top > 720:
            global_variables.score += 1
            self.reset()

    def draw(self, canvas):
        pygame.draw.circle(canvas, (255, 0, 0), self.hitbox.center, 40, 0)
