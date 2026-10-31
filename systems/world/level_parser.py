import pygame
from systems.entity.classes import Tile
from systems.assets.assets import sprites

def load_grid_from_file(filepath):
    grid = []
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                row = [int(num) for num in line.split()]
                grid.append(row)
    return grid

def create_tile_sprites(grid):
    IMAGE_MAP = {
        0: pygame.transform.scale(sprites["Floor"].texture, (32, 32)),
        1: pygame.transform.scale(sprites["Wall"].texture, (32, 32)),
        2: pygame.transform.scale(sprites["BrickWall"].texture, (32, 32)),
        3: pygame.transform.scale(sprites["WoodPlanks"].texture, (32, 32)),
    }

    
    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    for row_idx, row in enumerate(grid):
        for col_idx, tile_type in enumerate(row):
            image = IMAGE_MAP.get(tile_type, pygame.Surface((32, 32))) 

            tile = Tile(tile_type, col_idx, row_idx, image)
            all_sprites.add(tile)

            if tile_type == 1 or tile_type == 2:
                wall_sprites.add(tile)

    return all_sprites, wall_sprites