import pygame

import codebase.objects.bob.bobSETTINGS as bobSETTINGS
from codebase.settings import SCREEN_WIDTH, SCREEN_HEIGHT
import codebase.globals.time as time

bob = pygame.Surface((100, 100))
bob.fill((0, 255, 0))
bob_rect = bob.get_rect()
bob_rect.center = (640, 669)
bob_state = "standard"

can_jump = True
y_vel = 0


def update():
    move()


def move():
    global can_jump, y_vel

    keys = pygame.key.get_pressed()
    # horizontal movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        bob_rect.x -= bobSETTINGS.MOVEMENT_SPEED * time.deltaTime
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        bob_rect.x += bobSETTINGS.MOVEMENT_SPEED * time.deltaTime

    # vertical movement
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and bob_rect.bottom == SCREEN_HEIGHT:
        y_vel = 0
        y_vel -= bobSETTINGS.JUMP_HEIGHT
        can_jump = False

    bob_rect.y += y_vel/2
    if bob_rect.bottom != SCREEN_HEIGHT:
        y_vel += bobSETTINGS.GRAVITY_STRENGTH
    elif bob_rect.bottom == SCREEN_HEIGHT:
        can_jump = True
    bob_rect.y += y_vel/2

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        bobSETTINGS.GRAVITY_STRENGTH = 0.2
    elif bobSETTINGS.GRAVITY_STRENGTH != 0.1:
        bobSETTINGS.GRAVITY_STRENGTH = 0.1

    # border collision
    if bob_rect.right >= SCREEN_WIDTH:
        bob_rect.right = SCREEN_WIDTH
    if bob_rect.left <= 0:
        bob_rect.left = 0
    if bob_rect.bottom >= SCREEN_HEIGHT:
        bob_rect.bottom = SCREEN_HEIGHT
    if bob_rect.top <= 0:
        bob_rect.top = 0
