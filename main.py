import pygame

# pygame setup
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bob')

import sys
import math
import random

import src.objects.bob as bob
import src.objects.red_enemies as reds

import src.globals.globalVariables as global_variables
import src.globals.time as time

import src.system.render as render
import src.system.sound as sound

import src.data.score as score


version = "v.1.3.1"

# object setup
bob_object = bob.Bob()

# create 5 red enemies
for i in range(5):
    reds.RedEnemy()

# set images
background_image = pygame.image.load('assets/graphics/sprint_background.png').convert_alpha()
dash_available_image = pygame.image.load('assets/graphics/BobDash.png').convert_alpha()
dash_unavailable_image = pygame.image.load('assets/graphics/BobDashEmpty.png').convert_alpha()

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


def close():
    # update the max score in the .json file
    if score.get_max_score() < max_score:
        score.set_max_score(max_score)

    # quit the game
    pygame.quit()
    sys.exit()


def ability():
    global ability_power, keys_held
    if (keys_held[pygame.K_LSHIFT] or keys_held[pygame.K_RCTRL]) and ability_power > 0:
        ability_power -= 6
        render.background_state = render.BackgroundStates.ABILITY
        global_variables.ball_movement_mult = 0.7

    elif ability_power < ability_max:
        ability_power += 1
        render.background_state = render.BackgroundStates.BLACK
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
                    render.max_score_display = render.max_score_font.render(f'Lifetime highscore: {max_score}', True, (100, 255, 100))

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
    global play_uwu, uwu_score_display, uwu_init

    if 0 <= (global_variables.score % 100) <= 5 and global_variables.score > 99 and uwu_init:
        render.uwu_score_display = render.standard_font.render(f'score: {global_variables.score}', True, (255, 0, 255))
        global_variables.uwu_counter = 1
        uwu_init = False
        bob_object.temp_visual_state = bob_object.visual_state
        bob_object.visual_state = bob.States.UWU_FACE

    elif global_variables.score % 100 >= 10:
        uwu_init = True

    if 80 >= global_variables.uwu_counter > 0:
        global_variables.uwu_counter += 1
        if play_uwu:
            pygame.mixer.music.load('assets/sounds/BOB-UwU.mp3')
            pygame.mixer.music.play()
            play_uwu = False

    elif global_variables.uwu_counter > 80:
        global_variables.uwu_counter = 0
        play_uwu = True
        bob_object.visual_state = bob_object.temp_visual_state
        pygame.mixer.music.unload()


# Game Loop
while True:

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
                            render.background_state = render.BackgroundStates.CONTROL_GUIDE
                    case pygame.K_c:
                        if global_variables.gamestate == global_variables.GameStates.MAIN_MENU:
                            render.background_state = render.BackgroundStates.CREDITS
                    case pygame.K_p:  # switch displaying fps counter on/off
                        render.showFPS = not render.showFPS

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
            render.background_state = render.BackgroundStates.BLACK

    render.draw_screen(screen)

    pygame.display.update()
