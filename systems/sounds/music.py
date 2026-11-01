import pygame
import os

pygame.init()
pygame.mixer.init()

def start_bg_music():
    pygame.mixer.music.load(os.path.join("assets/music", "Distopia.wav"))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)