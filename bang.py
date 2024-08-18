from pynput import keyboard
import pygame
import glob
import random
import os

pygame.mixer.init()

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
    #print(f"Word to check: {word}. Letter to check: {word[0]}. Key input: {input}")
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
    try:
        if shots == 0 and key.char == ('r'):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/gun_cock.wav"))
            reload_gun()
            return
        elif shots == 0:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/reload_prompt.wav"))
            return
        key_pressed = key.char
        check_input(word, key_pressed)
    except AttributeError:
        pass
    

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    
print("Welcome to zombie shooter typer!")

print()

print(f"Your word: {word}")

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

