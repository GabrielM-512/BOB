import sys
from enum import Enum
import math
import random

import pygame

import src.objects.bob as bob
import src.objects.red_enemies as reds

import src.globals.globalVariables as global_variables
import src.globals.time as time

import src.system.render as render
import src.system.sound as sound

import src.data.score as score


class BackgroundStates(Enum):
    BLACK = 1
    ABILITY = 2
    CONTROL_GUIDE = 3
    CREDITS = 4


version = "v.1.3.1"

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
dash_available_image = pygame.image.load('assets/graphics/BobDash.png').convert_alpha()
dash_unavailable_image = pygame.image.load('assets/graphics/BobDashEmpty.png').convert_alpha()

background_state = BackgroundStates.BLACK

# variables setup
showFPS = False
fpsUpdater = 0

uwu_counter = 0
play_uwu = True
uwu_score = 0
uwu_score_display = None
uwu_init = True

max_score = score.get_max_score()

ability_power = 200
ability_max = 1080

# font and text setup

standard_font = pygame.font.SysFont('Arial', 50)
game_over_font = pygame.font.SysFont('Arial', 100)
max_score_font = pygame.font.SysFont('Arial', 35)
version_font = pygame.font.SysFont('Arial', 15)
control_credit_font = pygame.font.SysFont('Arial', 30)

version_text_display = version_font.render(version, True, (255, 255, 255))
display_game_over = game_over_font.render('Game Over!', True, (255, 100, 100))
reset_text_display = standard_font.render("Press 'ENTER' to reset!", True, (255, 255, 255))
start_text_display = standard_font.render("Press 'ENTER' to start!", True, (100, 255, 100))
control_guide_start = max_score_font.render("Press 'TAB' to view controls", True, (255, 255, 255))
credit_display = max_score_font.render("Press 'C' to view credits", True, (255, 255, 255))
max_score_display = max_score_font.render(f'Lifetime highscore: {max_score}', True, (100, 255, 100))
fps_display = version_font.render('180', True, (255, 255, 255))

move_text_guide_display = control_credit_font.render("A, D / LEFT, RIGHT         Move Left and Right", True, (255, 255, 255))
jump_text_guide_display = control_credit_font.render("SPACE / UP                    JUMP", True, (255, 255, 255))
ability_text_guide_display = control_credit_font.render("LSHIFT / RCONTROL    Slowdown ability", True, (255, 255, 255))
close_text_guide_display = control_credit_font.render("ESC                                Close game", True, (255, 255, 255))
dash_text_guide_display = control_credit_font.render("Q, E                                Dash Left/Right", True, (255, 255, 255))

groot_credit_display = control_credit_font.render("Main developer: Grootmaster47", True, (255, 255, 255))
jacek_credit_display = control_credit_font.render("Idea and Intro to Python: Jacek from Poland", True, (255, 255, 255))
yanic_credit_display = control_credit_font.render("Help with GitHub and refactor: Yanic from Magdeburg", True, (255, 255, 255))


def close():
    # updates the max score in the .json file
    if score.get_max_score() < max_score:
        score.set_max_score(max_score)

    # quit the game
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
                global_variables.gamestate = global_variables.GameStates.DEAD
                bob_object.visual_state = bob.States.DEAD

                pygame.mixer.music.load('assets/sounds/Bob_Death.mp3')
                pygame.mixer.music.play()

                pygame.mixer.music.unload()

                if global_variables.score > max_score:
                    max_score = global_variables.score
                    max_score_display = max_score_font.render(f'Lifetime highscore: {max_score}', True, (100, 255, 100))

                break


def reset():
    global ability_power
    if global_variables.gamestate == global_variables.GameStates.DEAD:
        global_variables.gamestate = global_variables.GameStates.PLAYING
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

        global_variables.score = 0


def uwu_sound_effect():
    global uwu_counter, play_uwu, uwu_score_display, uwu_init
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

    match global_variables.gamestate:
        case global_variables.GameStates.PLAYING:
            match background_state:
                case BackgroundStates.BLACK:
                    screen.fill((0, 0, 0))
                case BackgroundStates.ABILITY:
                    screen.blit(background_image, (0, 0))

        case global_variables.GameStates.MAIN_MENU:
            match background_state:
                case BackgroundStates.BLACK:
                    screen.fill((0, 0, 0))
                    screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 50))
                    screen.blit(control_guide_start, (SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 + 50))
                    screen.blit(credit_display, (SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2 + 100))
                case BackgroundStates.CONTROL_GUIDE:
                    screen.fill((0, 0, 0))
                    screen.blit(move_text_guide_display, (50, 40))
                    screen.blit(jump_text_guide_display, (50, 80))
                    screen.blit(ability_text_guide_display, (50, 120))
                    screen.blit(close_text_guide_display, (50, 160))
                    screen.blit(dash_text_guide_display, (50, 200))

                    screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT - 100))
                case BackgroundStates.CREDITS:
                    screen.fill((0, 0, 0))
                    screen.blit(groot_credit_display, (SCREEN_WIDTH / 2 - 150, 50))
                    screen.blit(jacek_credit_display, (SCREEN_WIDTH / 2 - 220, 100))
                    screen.blit(yanic_credit_display, (SCREEN_WIDTH / 2 - 280, 150))

                    screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT - 100))

        case global_variables.GameStates.DEAD:
            screen.fill((0, 0, 0))
            # draw bob here to get him behind the text
            bob_object.draw(screen)
            screen.blit(display_game_over, ((SCREEN_WIDTH / 2 - 50) - 150, SCREEN_HEIGHT / 2 - 50))
            screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT - 80))
            screen.blit(max_score_display, (20, 20))
            screen.blit(reset_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 100))


def draw_main_window():
    global fpsUpdater, uwu_counter

    if global_variables.gamestate == global_variables.GameStates.PLAYING:
        for game_object in global_variables.objects:
            game_object.draw(screen)

        if uwu_counter == 0:
            screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT / 8))
        elif uwu_counter <= 80:
            # noinspection PyTypeChecker
            screen.blit(uwu_score_display, (560, 90))

        if bob_object.ability_points >= bob_object.ABILITY_USAGE_REQUIREMENT:
            screen.blit(dash_available_image, (20, 0))
        else:
            screen.blit(dash_unavailable_image, (20, 0))

    if showFPS:
        if fpsUpdater >= 20:
            global_variables.fps = 1000 / time.deltaTime

            if global_variables.fps > 180:
                global_variables.fps = 180
            global_variables.fps = round(global_variables.fps)

            fpsUpdater = 0
        else:
            fpsUpdater += 1

        screen.blit(fps_display, (20, SCREEN_HEIGHT - 40))

    screen.blit(version_text_display, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20))


while True:

    score_display = standard_font.render(f'score: {global_variables.score}', True, (255, 255, 255))
    fps_display = version_font.render(f'{global_variables.fps}', True, (255, 255, 255))

    # event checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN:
            if __name__ == '__main__':
                match event.key:
                    case pygame.K_ESCAPE:  # close the game
                        close()
                    case pygame.K_b:  # switch Bob's visual to the smiley face
                        if global_variables.gamestate == global_variables.GameStates.PLAYING:
                            bob_object.visual_state = bob.States.SMILEY_FACE
                    case pygame.K_n:  # switch Bob's visual to the normal
                        if global_variables.gamestate == global_variables.GameStates.PLAYING:
                            bob_object.visual_state = bob.States.STANDARD
                    case pygame.K_RETURN:  # start the game
                        if global_variables.gamestate == global_variables.GameStates.DEAD:
                            reset()
                        else:
                            global_variables.gamestate = global_variables.GameStates.PLAYING
                    case pygame.K_TAB:  # display the control guide
                        if global_variables.gamestate == global_variables.GameStates.MAIN_MENU:
                            background_state = BackgroundStates.CONTROL_GUIDE
                    case pygame.K_c:
                        if global_variables.gamestate == global_variables.GameStates.MAIN_MENU:
                            background_state = BackgroundStates.CREDITS
                    case pygame.K_p:  # switch displaying fps counter on/off
                        showFPS = not showFPS

    keys_held = pygame.key.get_pressed()

    match global_variables.gamestate:
        case global_variables.GameStates.PLAYING:

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

        case global_variables.GameStates.DEAD:
            background_state = BackgroundStates.BLACK

    draw_background()
    draw_main_window()

    pygame.display.update()
