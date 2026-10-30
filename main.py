import pygame
import os
import level_parser

from classes import Player, Tile
from constants import BACKGROUND_COLOR
from assets import SPRITES

from asset_manager import AssetManager
from sprite import Sprite
from nassets import sprites, load_assetmanager

#pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((640, 800))
clock: pygame.time.Clock = pygame.time.Clock()
running: bool = True

grid_data: list = level_parser.load_grid_from_file(os.path.join("levels", "Ruins.txt"))
all_sprites, wall_sprites = level_parser.create_tile_sprites(grid_data)

player_frames = {
    'up':    [sprites[f"PlayerWalkUp{i+1}"].texture for i in range(4)],
    'down':  [sprites[f"PlayerWalkDown{i}"].texture for i in range(4)],
    'left':  [sprites[f"PlayerWalkLeft{i}"].texture for i in range(4)],
    'right': [sprites[f"PlayerWalkRight{i+1}"].texture for i in range(4)],

    'idle_down':  [sprites["PlayerIdle1"].texture],
    'idle_up':    [sprites["PlayerIdle2"].texture],
    'idle_left':  [sprites["PlayerIdle4"].texture],
    'idle_right': [sprites["PlayerIdle3"].texture],
}

player_group = pygame.sprite.Group()
player = Player(100, 100, player_frames, player_group)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hud_rect = pygame.Rect(0, 640, 640, 160)
    pygame.draw.rect(screen, (30, 30, 30), hud_rect)

    player_group.update(wall_sprites)
    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
