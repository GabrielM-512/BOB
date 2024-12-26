import pygame

clock = pygame.time.Clock()

deltaTime = 1.1


def time_tick():
    global deltaTime
    deltaTime = clock.tick(180)
