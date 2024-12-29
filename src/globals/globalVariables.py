from enum import Enum

objects = []
ball_movement_mult = 1
score = 0
fps = 180


class GameStates(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    DEAD = 3


gamestate = GameStates.MAIN_MENU
