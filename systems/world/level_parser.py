import pygame
from systems.entity.classes import Tile
from systems.assets.assets import sprites

def load_level_data(filepath):
    properties = {}
    grid_l1 = []
    grid_l2 = []
    
    with open(filepath, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    idx = 0
    while idx < len(lines):
        line = lines[idx]

        if line == "PROPERTIES START":
            idx += 1
            properties['name'] = lines[idx]
            
            idx += 1
            raw_conn = lines[idx].split("|")
            properties['connections'] = {
                'north': raw_conn[0].strip() if len(raw_conn) > 0 and raw_conn[0].strip() else None,
                'east':  raw_conn[1].strip() if len(raw_conn) > 1 and raw_conn[1].strip() else None,
                'south': raw_conn[2].strip() if len(raw_conn) > 2 and raw_conn[2].strip() else None,
                'west':  raw_conn[3].strip() if len(raw_conn) > 3 and raw_conn[3].strip() else None,
            }
        elif line == "TILES L1 START":
            idx += 1
            while idx < len(lines) and lines[idx] != "TILES L1 END":
                # Keep as raw strings so '0', '1', 'a', etc., match consistently
                row = lines[idx].split()
                grid_l1.append(row)
                idx += 1
        elif line == "TILES L2 START":
            idx += 1
            while idx < len(lines) and lines[idx] != "TILES L2 END":
                row = lines[idx].split()
                grid_l2.append(row)
                idx += 1

        idx += 1

    return properties.get('name', 'Unknown'), properties.get('connections', {}), grid_l1, grid_l2

def create_tile_sprites(grid_l1, grid_l2):
    IMAGE_MAP = {
        '0': pygame.transform.scale(sprites["Floor"].texture, (32, 32)),
        '1': pygame.transform.scale(sprites["Wall"].texture, (32, 32)),
        '2': pygame.transform.scale(sprites["BrickWall"].texture, (32, 32)),
        '3': pygame.transform.scale(sprites["WoodPlanks"].texture, (32, 32)),
        '4': pygame.transform.scale(sprites["Grass"].texture, (32, 32)),
        '5': pygame.transform.scale(sprites["Dirt"].texture, (32, 32)),
        '6': pygame.transform.scale(sprites["TreeTL"].texture, (32, 32)),
        '7': pygame.transform.scale(sprites["TreeTM"].texture, (32, 32)),
        '8': pygame.transform.scale(sprites["TreeTR"].texture, (32, 32)),
        '9': pygame.transform.scale(sprites["TreeBL"].texture, (32, 32)),
        'a': pygame.transform.scale(sprites["TreeBM"].texture, (32, 32)),
        'b': pygame.transform.scale(sprites["TreeBR"].texture, (32, 32)),
        'c': pygame.transform.scale(sprites["Trunk"].texture, (32, 32)),
    }

    SOLID_TILES = {'1', '2', '6', '7', '8', '9', 'a', 'b', 'c'}

    layer1_group = pygame.sprite.Group()
    layer2_group = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()

    for row_idx, row in enumerate(grid_l1):
        for col_idx, tile_type in enumerate(row):
            tile_str = str(tile_type)

            image = IMAGE_MAP.get(tile_str)
            if image:
                tile = Tile(tile_str, col_idx, row_idx, image)
                layer1_group.add(tile)

                if tile_str in SOLID_TILES:
                    wall_sprites.add(tile)

    for row_idx, row in enumerate(grid_l2):
        for col_idx, tile_type in enumerate(row):
            tile_str = str(tile_type)
            
            if tile_str != '0' and tile_str != '':
                image = IMAGE_MAP.get(tile_str)
                if image:
                    tile = Tile(tile_str, col_idx, row_idx, image)
                    layer2_group.add(tile)

                    if tile_str in SOLID_TILES:
                        wall_sprites.add(tile)

    return layer1_group, layer2_group, wall_sprites