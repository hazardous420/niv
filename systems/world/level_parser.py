import pygame
from systems.entity.classes import Item, Tile
from systems.assets.assets import sprites

def load_level_data(filepath, item_group):
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
                'north': raw_conn[0].strip() or None,
                'east': raw_conn[1].strip() or None,
                'south': raw_conn[2].strip() or None,
                'west': raw_conn[3].strip() or None,
            }

        elif line == "TILES L1 START":
            idx += 1

            while idx < len(lines) and lines[idx] != "TILES L1 END":
                grid_l1.append(lines[idx].split())
                idx += 1

        elif line == "TILES L2 START":
            idx += 1

            while idx < len(lines) and lines[idx] != "TILES L2 END":
                grid_l2.append(lines[idx].split())
                idx += 1

        elif line == "ITEMS START":
            idx += 1

            while idx < len(lines) and lines[idx] != "ITEMS END":
                item_data = lines[idx].split()

                if len(item_data) == 3:
                    item_id, col, row = item_data
                    col, row = int(col), int(row)
                    sprite_obj = sprites.get(item_id)

                    if sprite_obj and hasattr(sprite_obj, "texture"):
                        item_texture = pygame.transform.scale(sprite_obj.texture, (32, 32))
                        item_sprite = Item(item_id, col, row, item_texture)
                        item_group.add(item_sprite)
                    else:
                        print(f"Warning: Item ID '{item_id}' not found.")

                idx += 1

        idx += 1

    return (
        properties.get('name', 'Unknown'),
        properties.get('connections', {}),
        grid_l1,
        grid_l2
    )

def create_item_sprites(grid_l3):
    ITEM_MAP = {
        '1': {'name': 'TrustySword', 'image': pygame.transform.scale(sprites["TrustySword"].texture, (32, 32))},
        '2': {'name': 'GoldCoin', 'image': pygame.transform.scale(sprites["GoldCoin"].texture, (32, 32))},
        '3': {'name': 'GoldBag', 'image': pygame.transform.scale(sprites["GoldBag"].texture, (32, 32))},
        '4': {'name': 'GoldPile', 'image': pygame.transform.scale(sprites["GoldPile"].texture, (32, 32))},
    }

    item_group = pygame.sprite.Group()

    for row_idx, row in enumerate(grid_l3):
        for col_idx, tile_type in enumerate(row):
            tile_str = str(tile_type)
            
            if tile_str != '0' and tile_str != '':
                item_data = ITEM_MAP.get(tile_str)
                if item_data:
                    item = Item(item_data['name'], col_idx, row_idx, item_data['image'])
                    item_group.add(item)

    return item_group

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