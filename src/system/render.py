import pygame
from enum import Enum

import src.data.score as score
import src.globals.globalVariables as global_variables
import src.globals.time as time


class BackgroundStates(Enum):
    BLACK = 1
    ABILITY = 2
    CONTROL_GUIDE = 3
    CREDITS = 4


background_state = BackgroundStates.BLACK

version = "v.1.3.1"

showFPS = False

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# image setup
background_image = pygame.image.load('assets/graphics/sprint_background.png').convert_alpha()
dash_available_image = pygame.image.load('assets/graphics/BobDash.png').convert_alpha()
dash_unavailable_image = pygame.image.load('assets/graphics/BobDashEmpty.png').convert_alpha()

# font and text setup

standard_font = pygame.font.SysFont('Arial', 50)
game_over_font = pygame.font.SysFont('Arial', 100)
max_score_font = pygame.font.SysFont('Arial', 35)
version_font = pygame.font.SysFont('Arial', 15)
control_credit_font = pygame.font.SysFont('Arial', 30)
uwu_score_display = standard_font.render(f'score: {global_variables.score}', True, (255, 0, 255))

version_text_display = version_font.render(version, True, (255, 255, 255))
display_game_over = game_over_font.render('Game Over!', True, (255, 100, 100))
reset_text_display = standard_font.render("Press 'ENTER' to reset!", True, (255, 255, 255))
start_text_display = standard_font.render("Press 'ENTER' to start!", True, (100, 255, 100))
control_guide_start = max_score_font.render("Press 'TAB' to view controls", True, (255, 255, 255))
credit_display = max_score_font.render("Press 'C' to view credits", True, (255, 255, 255))
max_score_display = max_score_font.render(f'Lifetime highscore: {score.get_max_score()}', True, (100, 255, 100))
fps_display = version_font.render('180', True, (255, 255, 255))
score_display = standard_font.render(f'score: {global_variables.score}', True, (255, 255, 255))

move_text_guide_display = control_credit_font.render("A, D / LEFT, RIGHT         Move Left and Right", True, (255, 255, 255))
jump_text_guide_display = control_credit_font.render("SPACE / UP                    JUMP", True, (255, 255, 255))
ability_text_guide_display = control_credit_font.render("LSHIFT / RCONTROL    Slowdown ability", True, (255, 255, 255))
close_text_guide_display = control_credit_font.render("ESC                                Close game", True, (255, 255, 255))
dash_text_guide_display = control_credit_font.render("Q, E                                Dash Left/Right", True, (255, 255, 255))

groot_credit_display = control_credit_font.render("Main developer: Grootmaster47", True, (255, 255, 255))
jacek_credit_display = control_credit_font.render("Idea and Intro to Python: Jacek from Poland", True, (255, 255, 255))
yanic_credit_display = control_credit_font.render("Help with GitHub and refactor: Yanic from Magdeburg", True, (255, 255, 255))


def draw_background(screen):
    global fps_display, score_display, background_state, background_image

    score_display = standard_font.render(f'score: {global_variables.score}', True, (255, 255, 255))
    fps_display = version_font.render(f'{global_variables.fps}', True, (255, 255, 255))

    match global_variables.gamestate:
        case global_variables.GameStates.PLAYING:  # only displays the very background
            match background_state:
                case BackgroundStates.BLACK:
                    screen.fill((0, 0, 0))

                case BackgroundStates.ABILITY:
                    screen.blit(background_image, (0, 0))

        case global_variables.GameStates.MAIN_MENU:
            match background_state:
                case BackgroundStates.BLACK:  # displays the start screen
                    screen.fill((0, 0, 0))
                    screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 50))
                    screen.blit(control_guide_start, (SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 + 50))
                    screen.blit(credit_display, (SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2 + 100))

                case BackgroundStates.CONTROL_GUIDE:  # displays the control info
                    screen.fill((0, 0, 0))
                    screen.blit(move_text_guide_display, (50, 40))
                    screen.blit(jump_text_guide_display, (50, 80))
                    screen.blit(ability_text_guide_display, (50, 120))
                    screen.blit(close_text_guide_display, (50, 160))
                    screen.blit(dash_text_guide_display, (50, 200))

                    screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT - 100))

                case BackgroundStates.CREDITS:  # displays the credits
                    screen.fill((0, 0, 0))
                    screen.blit(groot_credit_display, (SCREEN_WIDTH / 2 - 150, 50))
                    screen.blit(jacek_credit_display, (SCREEN_WIDTH / 2 - 220, 100))
                    screen.blit(yanic_credit_display, (SCREEN_WIDTH / 2 - 280, 150))

                    screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT - 100))

        case global_variables.GameStates.DEAD:
            screen.fill((0, 0, 0))
            # draw bob here to get him behind the text
            global_variables.objects[0].draw(screen)
            screen.blit(display_game_over, ((SCREEN_WIDTH / 2 - 50) - 150, SCREEN_HEIGHT / 2 - 50))
            screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT - 80))
            screen.blit(max_score_display, (20, 20))
            screen.blit(reset_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 100))


def draw_main_window(screen):

    if global_variables.gamestate == global_variables.GameStates.PLAYING:
        for game_object in global_variables.objects:  # draw all game objects
            game_object.draw(screen)

        if global_variables.uwu_counter == 0:  # determine whether to display normal or pink score counter. Put here so Bob and balls can disappear behind it.
            screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT / 8))
        elif global_variables.uwu_counter <= 80:
            # noinspection PyTypeChecker
            screen.blit(uwu_score_display, (560, 90))

        if global_variables.objects[0].ability_points >= global_variables.objects[0].ABILITY_USAGE_REQUIREMENT:  # display the icon showing if dash is available
            screen.blit(dash_available_image, (20, 0))
        else:
            screen.blit(dash_unavailable_image, (20, 0))

    if showFPS:
        # recalculate the FPS
        global_variables.fps = 1000 / time.deltaTime

        if global_variables.fps > 180:
            global_variables.fps = 180
        global_variables.fps = round(global_variables.fps)

        # display the FPS
        screen.blit(fps_display, (20, SCREEN_HEIGHT - 40))

    screen.blit(version_text_display, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20))


def draw_screen(screen):
    draw_background(screen)
    draw_main_window(screen)
