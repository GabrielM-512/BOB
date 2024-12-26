import pygame

from src.globals.time import deltaTime


class Bob:
    # visual states for Bob
    state = {
        "STANDARD": 1,
        "SMILEYFACE": 2,
        "DEAD": 3,
        "UWUFACE": 4
    }

    MOVEMENT_SPEED = 0.54

    JUMP_HEIGHT = 20
    GRAVITY_STRENGTH = 0.1

    ABILITY_REGEN_SPEED = 0.18

    def __init__(self):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill((0, 255, 0))
        self.hitbox = self.surface.get_rect()
        self.hitbox.center = (640, 669)
        self.visual_state = self.state["STANDARD"]

        # whether Bob can jump
        self.can_jump = False

        self.y_vel = 0

        self.ability_points = 0

    def move(self):
        # get pressed keys
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.hitbox -= self.MOVEMENT_SPEED * deltaTime
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.hitbox += self.MOVEMENT_SPEED * deltaTime

        # vertical movement

        # check if Bob can jump again
        if self.hitbox.bottom == 720:
            self.can_jump = True

        # check if player wants to jump
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.y_vel += self.JUMP_HEIGHT
            self.can_jump = False

        # decrease y_vel if not on floor
        if self.hitbox.y != 720:
            self.y_vel -= self.GRAVITY_STRENGTH

        # move vertically
        self.hitbox.y -= self.y_vel

        # dash ability
        if self.ability_points <= 1800:
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
        if self.ability_points < 1800:
            self.ability_points += 0.18 * deltaTime
        self.move()

    def draw(self, canvas):
        canvas.blit(self.surface, self.hitbox)
