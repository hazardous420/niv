import pygame

pygame.init()
pygame.mixer.init()

footstep_sound = pygame.mixer.Sound("assets/sounds/footstep.wav")
footstep_sound.set_volume(0.5)

pickup_item_sound = pygame.mixer.Sound("assets/sounds/pickup.wav")
pickup_gold_sound = pygame.mixer.Sound("assets/sounds/relic_pickup.wav")
