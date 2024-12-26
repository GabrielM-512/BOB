import random
import sys

import pygame

from codebase.objects.bob import bob
import codebase.globals.time as time

version = "v.1.2"

pygame.init()

printCounter = 0

while printCounter < 50:
    print()
    printCounter += 1

# pygame setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bob')

# object setup
old_bob = pygame.Surface((100, 100))
old_bob.fill((0, 255, 0))
old_bob_rect = old_bob.get_rect()
old_bob_rect.center = (640, 669)
old_bob_state = "standard"

ball_surf = pygame.Surface((80, 80))
ball_surf.fill((255, 0, 0))
ball = ball_surf.get_rect(center=(random.randint(80, 1200), 50))

ball2_surf = pygame.Surface((80, 80))
ball2_surf.fill((255, 0, 0))
ball2 = ball2_surf.get_rect(center=(random.randint(80, 1200), -100))

ball3_surf = pygame.Surface((80, 80))
ball3_surf.fill((255, 0, 0))
ball3 = ball3_surf.get_rect(center=(random.randint(80, 1200), -250))

ball4_surf = pygame.Surface((80, 80))
ball4_surf.fill((255, 0, 0))
ball4 = ball4_surf.get_rect(center=(random.randint(80, 1200), -400))

ball5_surf = pygame.Surface((80, 80))
ball5_surf.fill((255, 0, 0))
ball5 = ball5_surf.get_rect(center=(random.randint(80, 1200), -400))

ball6_surf = pygame.Surface((80, 80))
ball6_surf.fill((255, 0, 0))
ball6 = ball6_surf.get_rect(center=(random.randint(80, 1200), -400))

background_image = pygame.image.load('./graphics/sprint_background.png').convert_alpha()
old_bobDash_image = pygame.image.load('./graphics/BobDash.png').convert_alpha()
old_bobDashEmpty_image = pygame.image.load('./graphics/BobDashEmpty.png').convert_alpha()

# variables setup
old_bob_movement_speed = 0.54

jump_height = 20
gravity_strength = 0
y_vel = 0
can_jump = False

fps = 180
showFPS = False
fpsUpdater = 0

ballMovementMult = 1

uwu_counter = 0
play_uwu = True
uwu_score = 0
uwu_score_display = None
uwu_init = True

timer = 0
score = 0
max_score = 0
game_start = False
game_over = False

background_state = "black"

ability_power = 200
ability_max = 1080
dash_timer = 1800

# font and text setup

font = pygame.font.SysFont('Arial', 50)
game_over_font = pygame.font.SysFont('Arial', 100)
max_score_font = pygame.font.SysFont('Arial', 35)
version_font = pygame.font.SysFont('Arial', 15)
control_guide_font = pygame.font.SysFont('Arial', 30)

version_text_display = version_font.render(version, True, (255, 255, 255))
display_game_over = game_over_font.render('Game Over!', True, (255, 100, 100))
reset_text_display = font.render("Press 'R' to reset!", True, (255, 255, 255))
start_text_display = font.render("Press 'ENTER' to start!", True, (100, 255, 100))
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


def move():
    global y_vel, can_jump, jump_height, dash_timer, gravity_strength

    keys = pygame.key.get_pressed()
    # horizontal movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        old_bob_rect.x -= old_bob_movement_speed * time.deltaTime
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        old_bob_rect.x += old_bob_movement_speed * time.deltaTime

    # vertical movement
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and old_bob_rect.bottom == SCREEN_HEIGHT:
        y_vel = 0
        y_vel -= jump_height
        can_jump = False

    old_bob_rect.y += y_vel/2
    if old_bob_rect.bottom != SCREEN_HEIGHT:
        y_vel += gravity_strength
    elif old_bob_rect.bottom == SCREEN_HEIGHT:
        can_jump = True
    old_bob_rect.y += y_vel/2

    if keys_held[pygame.K_s] or keys_held[pygame.K_DOWN]:
        gravity_strength = 0.2
    elif gravity_strength != 0.1:
        gravity_strength = 0.1

    # dash ability
    if keys[pygame.K_q] and dash_timer >= 1800:
        old_bob_rect.x -= 300
        dash_timer = 0
    if keys[pygame.K_e] and dash_timer >= 1800:
        old_bob_rect.x += 300
        dash_timer = 0

    # increment dash points
    if dash_timer <= 1800:
        dash_timer += 0.18 * time.deltaTime

    # border collision
    if old_bob_rect.right >= SCREEN_WIDTH:
        old_bob_rect.right = SCREEN_WIDTH
    if old_bob_rect.left <= 0:
        old_bob_rect.left = 0
    if old_bob_rect.bottom >= SCREEN_HEIGHT:
        old_bob_rect.bottom = SCREEN_HEIGHT
    if old_bob_rect.top <= 0:
        old_bob_rect.top = 0


def ability():
    global ability_power, jump_height, background_state, gravity_strength, ballMovementMult, dash_timer, keys_held
    if (keys_held[pygame.K_LSHIFT] or keys_held[pygame.K_RCTRL]) and ability_power > 0:
        jump_height = 10
        ability_power -= 6
        background_state = "sprint"
        ballMovementMult = 0.7

    elif ability_power < ability_max:
        ability_power += 1
        background_state = "black"
        jump_height = 8
        ballMovementMult = 1

    # dash ability
    if keys_held[pygame.K_q] and dash_timer >= 1800:
        old_bob_rect.x -= 300
        dash_timer = 0
    if keys_held[pygame.K_e] and dash_timer >= 1800:
        old_bob_rect.x += 300
        dash_timer = 0

    # increment dash points
    if dash_timer <= 1800:
        dash_timer += 0.18 * time.deltaTime


def ball_collisions():
    # noinspection PyGlobalUndefined
    global game_over, score, max_score, max_score_display, old_bob, old_bob_state
    if old_bob_rect.colliderect(ball) or old_bob_rect.colliderect(ball2) or old_bob_rect.colliderect(ball3) \
            or old_bob_rect.colliderect(ball4) or old_bob_rect.colliderect(ball5) or old_bob_rect.colliderect(ball6):
        game_over = True
        old_bob = pygame.image.load('./graphics/BobDeath.png').convert_alpha()

        pygame.mixer.music.load('./sounds/Bob_Death.mp3')
        pygame.mixer.music.play()

        old_bob_state = "dead"

        pygame.mixer.music.unload()
        if score > max_score:
            max_score = score
            max_score_display = max_score_font.render(f'Max score this session: {max_score}', True, (100, 255, 100))


def reset():
    global game_over, ball, ball2, ball3, ball4, ball5, ball6, timer, score, ability_power, jump_height, dash_timer, old_bob_state
    if game_over:
        game_over = False
        timer = 0
        ability_power = 200
        dash_timer = 1800
        jump_height = 4

        ball = ball_surf.get_rect(center=(random.randint(80, 1200), 50))
        ball2 = ball2_surf.get_rect(center=(random.randint(80, 1200), -100))
        ball3 = ball3_surf.get_rect(center=(random.randint(80, 1200), -250))
        ball4 = ball4_surf.get_rect(center=(random.randint(80, 1200), -400))
        ball5 = ball5_surf.get_rect(center=(random.randint(80, 1200), -400))
        ball6 = ball6_surf.get_rect(center=(random.randint(80, 1200), -400))

        old_bob_rect.center = (640, 670)
        old_bob.fill((0, 255, 0))
        old_bob_state = "standard"

        score = 0


def ball_movement():
    global score
    if ball.y >= SCREEN_HEIGHT:
        ball.center = (random.randint(40, 1240), -650 + random.randint(-50, 50))
        score += 1
    ball.y += 0.5234 * time.deltaTime * ballMovementMult

    if ball2.y >= SCREEN_HEIGHT:
        ball2.center = (random.randint(40, 1240), -100 + random.randint(-50, 50))
        score += 1
    ball2.y += 0.872 * time.deltaTime * ballMovementMult

    if ball3.y >= SCREEN_HEIGHT:
        ball3.center = (random.randint(40, 1240), -250 + random.randint(-50, 50))
        score += 1
    ball3.y += 0.3275 * time.deltaTime * ballMovementMult

    if ball4.y >= SCREEN_HEIGHT:
        ball4.center = (random.randint(40, 1240), -400 + random.randint(-50, 50))
        score += 1
    ball4.y += 0.348 * time.deltaTime * ballMovementMult

    if timer >= 500:
        if ball5.y >= SCREEN_HEIGHT:
            ball5.center = (random.randint(40, 1240), random.randint(-650, -350))
            score += 1
        ball5.y += 0.6942076 * time.deltaTime * ballMovementMult

    if score >= 150:
        if ball6.y >= SCREEN_HEIGHT:
            ball6.center = (random.randint(40, 1240), random.randint(-650, -350))
            score += 1
        ball6.y += 0.8523 * time.deltaTime * ballMovementMult


def uwu_sound_effect():
    global score, uwu_counter, play_uwu, uwu_score_display, uwu_init, old_bob
    if score % 100 == 0 and score > 0 and uwu_init:
        uwu_score_display = font.render(f'score: {score}', True, (255, 0, 255))
        uwu_counter = 1
        uwu_init = False
        old_bob = pygame.image.load('./graphics/BWOB-UwU.png').convert_alpha()
    elif score % 100 != 0:
        uwu_init = True

    if 80 >= uwu_counter > 0:
        uwu_counter += 1
        if play_uwu:
            pygame.mixer.music.load('./sounds/BOB-UwU.mp3')
            pygame.mixer.music.play()
            play_uwu = False
    elif uwu_counter > 80:
        uwu_counter = 0
        play_uwu = True
        if old_bob_state == "standard":
            old_bob.fill((0, 255, 0))
        elif old_bob_state == "smile":
            old_bob = pygame.image.load('./graphics/BOB.png').convert_alpha()
        elif old_bob_state == "dead":
            old_bob = pygame.image.load('./graphics/BobDeath.png').convert_alpha()
        pygame.mixer.music.unload()


def draw_background():
    global background_state, background_image
    if background_state == "black":
        screen.fill((0, 0, 0))
    elif background_state == "sprint":
        screen.blit(background_image, (0, 0))

    if not game_start:

        if background_state == "black":
            screen.fill((0, 0, 0))
            screen.blit(start_text_display, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 50))
            screen.blit(control_guide_start, (SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 + 50))

        if background_state == "control_guide":
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
        screen.blit(old_bob, old_bob_rect)

        if uwu_counter == 0:
            screen.blit(score_display, ((SCREEN_WIDTH / 2) - 80, SCREEN_HEIGHT / 8))
        elif uwu_counter <= 80:
            # noinspection PyTypeChecker
            screen.blit(uwu_score_display, (560, 90))

        pygame.draw.circle(screen, (255, 0, 0), ball.center, 40, 0)
        pygame.draw.circle(screen, (255, 0, 0), ball2.center, 40, 0)
        pygame.draw.circle(screen, (255, 0, 0), ball3.center, 40, 0)
        pygame.draw.circle(screen, (255, 0, 0), ball4.center, 40, 0)

        if timer >= 500:
            pygame.draw.circle(screen, (255, 0, 0), ball5.center, 40, 0)

        if score >= 150:
            pygame.draw.circle(screen, (255, 0, 0), ball6.center, 40, 0)

        if dash_timer >= 1800:
            screen.blit(old_bobDash_image, (20, 0))
        else:
            screen.blit(old_bobDashEmpty_image, (20, 0))

    elif game_over:
        screen.blit(old_bob, old_bob_rect)

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

    score_display = font.render(f'score: {score}', True, (255, 255, 255))
    fps_display = version_font.render(f'{fps}', True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                close()
            if event.key == pygame.K_b and game_start and not game_over:
                old_bob = pygame.image.load('./graphics/BOB.png').convert_alpha()
                old_bob_state = "smile"
            if event.key == pygame.K_n and game_start and not game_over:
                old_bob.fill((0, 255, 0))
                old_bob_state = "standard"
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_RETURN:
                game_start = True
            if event.key == pygame.K_TAB:
                if not game_start:
                    background_state = "control_guide"
            if event.key == pygame.K_p:
                if showFPS:
                    showFPS = False
                else:
                    showFPS = True

    keys_held = pygame.key.get_pressed()

    if not game_over and game_start:

        time.time_tick()
        # movement

        ability()
        bob.update()

        if timer <= 550:
            timer += 0.018 * time.deltaTime

        # Ball movement
        ball_movement()
        ball_collisions()

        uwu_sound_effect()

    elif game_over:
        background_state = 'black'

    draw_background()
    draw_main_window()

    pygame.display.update()
