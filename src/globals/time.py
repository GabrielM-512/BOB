import pygame

clock = pygame.time.Clock()

deltaTime = 0


def time_tick():  # advances the game by one tick
    global deltaTime
    deltaTime = clock.tick(180)  # the argument provided here sets the FPS
