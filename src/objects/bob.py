import pygame
import math
from enum import Enum
import src.globals.time as time
import src.globals.globalVariables as global_variables


class States(Enum):  # visual states for bob
    STANDARD = 1
    SMILEY_FACE = 2
    DEAD = 3
    UWU_FACE = 4


class Bob:

    MOVEMENT_SPEED = 0.8

    JUMP_HEIGHT = 4
    GRAVITY_STRENGTH = 0.02
    JUMP_MODIFIER = 1

    # variables for dash ability
    ABILITY_REGEN_SPEED = 0.18
    ABILITY_USAGE_REQUIREMENT = 1200

    def __init__(self):
        self.type = "BOB"

        self.surface = pygame.Surface((100, 100))
        self.surface.fill((0, 255, 0))
        self.hitbox = self.surface.get_rect()
        self.hitbox.center = (640, 669)
        self.visual_state = States.STANDARD
        self.temp_visual_state = States.STANDARD

        # whether Bob can jump
        self.can_jump = False
        self.y_vel = 0

        self.ability_points = self.ABILITY_USAGE_REQUIREMENT

        self.col = (0, 255, 0)
        self.bob_smile = pygame.image.load("assets/graphics/BOB.png").convert_alpha()
        self.bob_dead = pygame.image.load("assets/graphics/BOBDeath.png").convert_alpha()
        self.bob_uwu = pygame.image.load("assets/graphics/BWOB-UwU.png").convert_alpha()

        global_variables.objects.append(self)

    def move(self):
        # get pressed keys
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.hitbox.x -= self.MOVEMENT_SPEED * time.deltaTime
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.hitbox.x += self.MOVEMENT_SPEED * time.deltaTime

        # vertical movement

        # check if Bob can jump again
        if self.hitbox.bottom == 720:
            self.can_jump = True
            self.y_vel = 0

        # check if player wants to jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.can_jump:
            self.y_vel += self.JUMP_HEIGHT * self.JUMP_MODIFIER
            self.can_jump = False

        # decrease y_vel if not on floor
        if self.hitbox.bottom != 720:
            self.y_vel -= self.GRAVITY_STRENGTH * time.deltaTime

        # move vertically
        self.hitbox.y -= math.floor(self.y_vel * time.deltaTime)

        # dash ability
        if self.ability_points >= self.ABILITY_USAGE_REQUIREMENT:
            if keys[pygame.K_q]:
                self.hitbox.x -= 300
                self.ability_points = 0
            if keys[pygame.K_e]:
                self.hitbox.x += 300
                self.ability_points = 0

        # check if Bob is out of bounds, if so, snap him back
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        elif self.hitbox.right > 1280:
            self.hitbox.right = 1280

        if self.hitbox.bottom >= 720:
            self.hitbox.bottom = 720
        elif self.hitbox.top < 0:
            self.hitbox.top = 0

    def update(self):
        if self.ability_points <= self.ABILITY_USAGE_REQUIREMENT:
            self.ability_points += 0.18 * time.deltaTime
        self.move()

    def draw(self, canvas):
        match self.visual_state:
            case States.STANDARD:
                canvas.blit(self.surface, self.hitbox)
            case States.SMILEY_FACE:
                canvas.blit(self.bob_smile, self.hitbox)
            case States.DEAD:
                canvas.blit(self.bob_dead, self.hitbox)
            case States.UWU_FACE:
                canvas.blit(self.bob_uwu, self.hitbox)
