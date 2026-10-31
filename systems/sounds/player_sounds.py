import pygame

pygame.init()
pygame.mixer.init()

footstep_sound = pygame.mixer.Sound("assets/sounds/footstep.wav")
footstep_sound.set_volume(0.5)