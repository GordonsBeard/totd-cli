"""It's a game? Dunno. Typing thing that makes noises."""

import glob
import random

import pygame
from pynput import keyboard

pygame.init()
# pygame.mixer.init()

shots = 12

gunshots = glob.glob("sounds/p1_shoot.wav")
ricochets = glob.glob("sounds/riccochet*.wav")
hits = glob.glob("sounds/*_shot.wav")

target_words = ["baseball", "monday", "skunk", "rabbit", "bird", "toast"]

word = random.choice(target_words)


def lose_bullet():
    global shots
    shots -= 1


def reload_gun():
    global shots
    shots = 12
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/gun_cock.wav"))


def update_word(new_word):
    global word
    word = new_word


def kill_zombie():
    print("\033[2J\033[H", end="", flush=True)
    print("Zombie killed!")
    global word
    word = random.choice(target_words)
    print()
    print()

    print(f"Your next word: {word}")


def check_input(word, input):
    lose_bullet()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(random.choice(gunshots)))
    if input == word[0]:
        # if that's the last one, kill the zombo
        if len(word) == 1:
            kill_zombie()
            pygame.mixer.Channel(2).play(pygame.mixer.Sound(random.choice(hits)))
            return True
        # else, iterate
        else:
            new_word = word[1:]
            print(f"Correct! New word: {new_word}")
            update_word(new_word)
            return True
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(random.choice(ricochets)))
    return False


def on_press(key):
    if key == "tab":
        reload_gun()
        return
    if shots == 0:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/reload_prompt.wav"))
        return

    key_pressed = key
    check_input(word, key_pressed)


def on_release(key):
    if key == "escape":
        return False


# print("Welcome to zombie shooter typer! ESC to quit, R to reload!")
# print()
# print(f"Your word: {word}")


# def start_listening_for_keys():
#     with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#         listener.join()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

start_x = 250.0
start_y = 250.0

SPEED_CHANGE = 0.5


def draw_clip():
    clip_start_x = 350
    clip_start_y = 50

    bullet_color = WHITE

    if shots < 3:
        bullet_color = RED

    """Draws the bullets left"""
    pygame.draw.rect(screen, bullet_color, [clip_start_x, clip_start_y, 285, 60], 2)

    for bullet in range(shots):
        pygame.draw.rect(
            screen, bullet_color, [clip_start_x + 5, clip_start_y + 5, 12, 50]
        )
        clip_start_x += 24


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print(f"Keydown: {pygame.key.name(event.key)}")
            on_press(pygame.key.name(event.key))
        elif event.type == pygame.KEYUP:
            on_release(pygame.key.name(event.key))

    screen.fill(BLACK)
    # pygame.draw.rect(screen, WHITE, [start_x, start_y, 250, 100])
    font = pygame.font.SysFont("Consolas", 25, True, False)
    text = font.render(word, True, WHITE)
    screen.blit(text, [50, 50])

    # start_y += SPEED_CHANGE
    # start_x += SPEED_CHANGE
    draw_clip()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
