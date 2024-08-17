from pynput import keyboard
import pygame
import glob
import random

pygame.mixer.init()

shots = 6

# thanks to CobalCatsup for the gunsounds
gunshots = glob.glob("sounds/p1_shoot.wav")

ricochets = glob.glob("sounds/riccochet*.wav")

hits = glob.glob("sounds/*_shot.wav")

def lose_bullet():
    global shots
    shots -= 1

def reload_gun():
    global shots
    shots = 6

def on_press(key):
    try:
        if shots == 0 and key.char == ('r'):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/gun_cock.wav"))
            reload_gun()
            return
        elif shots == 0:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/reload_prompt.wav"))
            return

        pygame.mixer.Channel(0).play(pygame.mixer.Sound(random.choice(gunshots)))
        if random.random() < 0.4:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(random.choice(ricochets)))
        else:
            if random.random() < 0.85:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(random.choice(hits)))
        lose_bullet()

    except AttributeError:
        print(f"Special key pressed: {key}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()