import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

#constants
SCALE = (32, 32)

#functions
def scale_image(image):
    return pygame.transform.scale(image, SCALE)

#sprites
PLAYER_SPRITE = scale_image(pygame.image.load("images/characters/PlayerIdle1.png").convert_alpha())
WALL_SPRITE = scale_image(pygame.image.load("images/tiles/Wall.png").convert_alpha())
FLOOR_SPRITE = scale_image(pygame.image.load("images/tiles/Floor.png").convert_alpha())

#pass sprites to main.py
def return_sprites():
    return FLOOR_SPRITE, WALL_SPRITE, PLAYER_SPRITE

SPRITES = return_sprites()