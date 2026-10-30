import pygame
import os
from assets import SPRITES
import level_parser
from classes import Player, Tile

#pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

BACKGROUND_COLOR = (230, 212, 114)

grid_data = level_parser.load_grid_from_file(os.path.join("levels", "level1.txt"))
all_sprites, wall_sprites = level_parser.create_tile_sprites(grid_data)

player_frames = {
    'up':    [pygame.image.load(os.path.join("images", "characters", f"PlayerWalkUp{i+1}.png")).convert_alpha() for i in range(4)],#bru i forgot to end this one with 0 and 2 lazy 2 change
    'down':  [pygame.image.load(os.path.join("images", "characters", f"PlayerWalkDown{i}.png")).convert_alpha() for i in range(4)],
    'left':  [pygame.image.load(os.path.join("images", "characters", f"PlayerIdle1.png")).convert_alpha() for i in range(4)],
    'right': [pygame.image.load(os.path.join("images", "characters", f"PlayerIdle1.png")).convert_alpha() for i in range(4)]
}
player_group = pygame.sprite.Group()
player = Player(100, 100, player_frames, player_group)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input(wall_sprites)
    screen.fill(BACKGROUND_COLOR)

    #rendering
    all_sprites.draw(screen)
    player_group.draw(screen)
    player.update(wall_sprites)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()