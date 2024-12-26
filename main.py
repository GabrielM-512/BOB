import sys
from enum import Enum
import math
import random

import pygame

import src.objects.bob as bob
import src.objects.red_enemies as reds

import src.globals.globalVariables as global_variables
import src.globals.time as time


class BackgroundStates(Enum):
    BLACK = 1,
    ABILITY = 2,
    CONTROL_GUIDE = 3


version = "v.1.3"

pygame.init()

# pygame setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bob')

# object setup
bob_object = bob.Bob()

# create 5 red enemies
for i in range(5):
    reds.RedEnemy()

# set images
background_image = pygame.image.load('assets/graphics/sprint_background.png').convert_alpha()
old_bobDash_image = pygame.image.load('assets/graphics/BobDash.png').convert_alpha()
old_bobDashEmpty_image = pygame.image.load('assets/graphics/BobDashEmpty.png').convert_alpha()

background_state = BackgroundStates.BLACK

# variables setup
fps = 180
showFPS = False
fpsUpdater = 0

uwu_counter = 0
play_uwu = True
uwu_score = 0
uwu_score_display = None
uwu_init = True

max_score = 0
game_start = False
game_over = False

ability_power = 200
ability_max = 1080

# font and text setup

standard_font = pygame.font.SysFont('Arial', 50)
game_over_font = pygame.font.SysFont('Arial', 100)
max_score_font = pygame.font.SysFont('Arial', 35)
version_font = pygame.font.SysFont('Arial', 15)
control_guide_font = pygame.font.SysFont('Arial', 30)

version_text_display = version_font.render(version, True, (255, 255, 255))
display_game_over = game_over_font.render('Game Over!', True, (255, 100, 100))
reset_text_display = standard_font.render("Press 'R' to reset!", True, (255, 255, 255))
start_text_display = standard_font.render("Press 'ENTER' to start!", True, (100, 255, 100))
control_guide_start = max_score_font.render("Press 'TAB' to view controls", True, (255, 255, 255))
max_score_display = max_score_font.render(f'Max score this session: 0', True, (100, 255, 100))
fps_display = version_font.render('180', True, (255, 255, 255))

move_text_guide_display = control_guide_font.render("A, D / LEFT, RIGHT:         Move Left or Right", True, (255, 255, 255))
jump_text_guide_display = control_guide_font.render("SPACE / UP:                    JUMP", True, (255, 255, 255))
ability_text_guide_display = control_guide_font.render("LSHIFT / RCONTROL:    Slowdown ability", True, (255, 255, 255))
close_text_guide_display = control_guide_font.render("ESC:                                 Close game", True, (255, 255, 255))
dash_text_guide_display = control_guide_font.render("Q, E:                                 Dash Left/Right", True, (255, 255, 255))


def close():
    pygame.quit()
    sys.exit()


def ability():
    global ability_power, background_state, keys_held
    if (keys_held[pygame.K_LSHIFT] or keys_held[pygame.K_RCTRL]) and ability_power > 0:
        ability_power -= 6
        background_state = BackgroundStates.ABILITY
        global_variables.ball_movement_mult = 0.7

    elif ability_power < ability_max:
        ability_power += 1
        background_state = BackgroundStates.BLACK
        global_variables.ball_movement_mult = 1


def ball_collisions():
    # noinspection PyGlobalUndefined
    global game_over, max_score, max_score_display
    for game_object in global_variables.objects:
        if game_object.type == "RED_ENEMY":
            if bob_object.hitbox.colliderect(game_object.hitbox):
                game_over = True
                bob_object.visual_state = bob.States.DEAD

                pygame.mixer.music.load('assets/sounds/Bob_Death.mp3')
                pygame.mixer.music.play()

                #pygame.mixer.music.unload()
                if global_variables.score > max_score:
                    max_score = global_variables.score
                    max_score_display = max_score_font.render(f'Max score this session: {max_score}', True, (100, 255, 100))

                break


def reset():
    global game_over, ability_power
    if game_over:
        game_over = False
        ability_power = 200
        bob_object.ability_points = bob_object.ABILITY_USAGE_REQUIREMENT

        for game_object in global_variables.objects:
            if game_object.type == "RED_ENEMY":
                game_object.hitbox.y = -100 + random.randint(-20, 20)
                game_object.hitbox.x = random.randint(40, 1240)
                game_object.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5) * 4

                for target in global_variables.objects:
                    if target.type == "RED_ENEMY":
                        while game_object.falling_speed == target.falling_speed and target != game_object:
                            game_object.falling_speed = math.pow(random.uniform(0.54, 0.9), 2.5) * 4

        bob_object.hitbox.center = (640, 670)
        bob_object.y_vel = 0

        bob_object.visual_state = bob.States.STANDARD

        global_variables.score = 00


def uwu_sound_effect():
    global uwu_counter, play_uwu, uwu_score_display, uwu_init, old_bob
    if 0 <= (global_variables.score % 100) <= 5 and global_variables.score > 99 and uwu_init:
        uwu_score_display = standard_font.render(f'score: {global_variables.score}', True, (255, 0, 255))
        uwu_counter = 1
        uwu_init = False
        bob_object.temp_visual_state = bob_object.visual_state
        bob_object.visual_state = bob.States.UWU_FACE

    elif global_variables.score % 100 >= 10:
        uwu_init = True

    if 80 >= uwu_counter > 0:
        uwu_counter += 1
        if play_uwu:
            pygame.mixer.music.load('assets/sounds/BOB-UwU.mp3')
            pygame.mixer.music.play()
            play_uwu = False

    elif uwu_counter > 80:
        uwu_counter = 0
        play_uwu = True
        bob_object.visual_state = bob_object.temp_visual_state
        pygame.mixer.music.unload()


def draw_background():
    global background_state, background_image
    if game_start:
        match background_state:
            case BackgroundStates.BLACK:
                screen.fill((0, 0, 0))
            case BackgroundStates.ABILITY:
                screen.blit(background_image, (0, 0))

    else:
        match background_state:
            case BackgroundStates.BLACK:
                screen.fill((0, 0, 0))
                screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 50))
                screen.blit(control_guide_start, (SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 + 50))
            case BackgroundStates.CONTROL_GUIDE:
                screen.fill((0, 0, 0))
                screen.blit(move_text_guide_display, (50, 40))
                screen.blit(jump_text_guide_display, (50, 80))
                screen.blit(ability_text_guide_display, (50, 120))
                screen.blit(close_text_guide_display, (50, 160))
                screen.blit(dash_text_guide_display, (50, 200))

                screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT - 100))


def draw_main_window():
    global fpsUpdater, fps, uwu_counter

    if not game_over and game_start:
        print(bob_object.ability_points)
        for game_object in global_variables.objects:
            game_object.draw(screen)

        if uwu_counter == 0:
            screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT / 8))
        elif uwu_counter <= 80:
            # noinspection PyTypeChecker
            screen.blit(uwu_score_display, (560, 90))

        if bob_object.ability_points >= bob_object.ABILITY_USAGE_REQUIREMENT:
            screen.blit(old_bobDash_image, (20, 0))
        else:
            screen.blit(old_bobDashEmpty_image, (20, 0))

    elif game_over:
        bob_object.draw(screen)

        screen.blit(display_game_over, ((SCREEN_WIDTH / 2 - 50) - 150, SCREEN_HEIGHT / 2 - 50))
        screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT - 80))
        screen.blit(max_score_display, (20, 20))
        screen.blit(reset_text_display, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 100))

    if showFPS:
        if fpsUpdater >= 20:
            fps = 1000 / time.deltaTime

            if fps > 180:
                fps = 180
            fps = round(fps)

            fpsUpdater = 0
        else:
            fpsUpdater += 1

        screen.blit(fps_display, (20, SCREEN_HEIGHT - 40))

    screen.blit(version_text_display, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20))


while True:

    score_display = standard_font.render(f'score: {global_variables.score}', True, (255, 255, 255))
    fps_display = version_font.render(f'{fps}', True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN:
            if __name__ == '__main__':
                match event.key:
                    case pygame.K_ESCAPE:  # close the game
                        close()
                    case pygame.K_b:  # switch Bob's visual to the smileyface
                        if game_start and not game_over:
                            bob_object.visual_state = bob.States.SMILEY_FACE
                    case pygame.K_n:  # switch Bob's visual to the normal
                        if game_start and not game_over:
                            bob_object.visual_state = bob.States.STANDARD
                    case pygame.K_r:  # reset the game
                        reset()
                    case pygame.K_RETURN:  # start the game
                        game_start = True
                    case pygame.K_TAB:  # display the control guide
                        if not game_start:
                            background_state = BackgroundStates.CONTROL_GUIDE
                    case pygame.K_p:  # switch displaying fps counter on/off
                        showFPS = not showFPS

    keys_held = pygame.key.get_pressed()

    if not game_over and game_start:

        time.time_tick()
        # movement

        ability()
        bob_object.update()

        # Ball movement
        for game_object in global_variables.objects:
            if game_object.type == "RED_ENEMY":
                game_object.move()
        # Check for collisions between Bob and enemies
        ball_collisions()

        uwu_sound_effect()

    elif game_over:
        background_state = BackgroundStates.BLACK

    draw_background()
    draw_main_window()

    pygame.display.update()
