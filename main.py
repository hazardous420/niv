## PYGAME
import pygame
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

## STD (nah diddy)
import os

## SELF
from systems.assets.asset_manager import AssetManager
from systems.assets.sprite import Sprite
from systems.assets.assets import sprites, load_assetmanager

from systems.visuals.lightmanager import LightManager
from systems.visuals.light import AmbientLight, create_light_surf

import systems.world.level_parser as level_parser
from systems.entity.classes import Player, Tile
from systems.globals.constants import BACKGROUND_COLOR

pygame.font.init()
hud_font = pygame.font.Font("assets/fonts/alagard.ttf", 30)

clock: pygame.time.Clock = pygame.time.Clock()
running: bool = True

## LIGHTS
light_manager: LightManager = LightManager()
light_manager.add_light(200)

asset_manager: AssetManager = AssetManager()
load_assetmanager(asset_manager)

current_level_file = "CITY_START.txt"
current_location = ""
level_connections = {}

current_location, level_connections, grid_l1, grid_l2 = level_parser.load_level_data(
    os.path.join("levels", current_level_file)
)

layer1_sprites = pygame.sprite.Group()
layer2_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()

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
player = Player(400, 400, player_frames, player_group)

player_health = 100
player_sanity = 85

RelicaBeltSprite = sprites["RelicaBelt"].texture
RelicaBeltSpriteRect = RelicaBeltSprite.get_rect(midbottom=(1800 /2, 990))
RelicaBeltSprite = pygame.transform.scale(RelicaBeltSprite, (RelicaBeltSprite.get_width() * 3.5, RelicaBeltSprite.get_height() * 3.5))

def create_crt_overlay(width: int, height: int, line_spacing: int = 4, opacity: int = 40) -> pygame.Surface:
    crt_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    scanline_color = (0, 0, 0, opacity)
    for y in range(0, height, line_spacing):
        pygame.draw.line(crt_surface, scanline_color, (0, y), (width, y), 1)
        
    return crt_surface
crt_overlay = create_crt_overlay(1920, 1080, line_spacing=4, opacity=255)

def load_level(filename):
    global current_location, level_connections, layer1_sprites, layer2_sprites, wall_sprites
    
    filepath = os.path.join("levels", filename)
    current_location, level_connections, grid_l1, grid_l2 = level_parser.load_level_data(filepath)
    
    layer1_sprites, layer2_sprites, wall_sprites = level_parser.create_tile_sprites(grid_l1, grid_l2)

def handle_level_swap():
    PLAYABLE_WIDTH = 1920
    PLAYABLE_HEIGHT = 935

        #west
    if player.rect.right < 0 and level_connections.get('west'):
        load_level(f"{level_connections['west']}.txt")
        player.rect.left = PLAYABLE_WIDTH - player.rect.width
        #east
    elif player.rect.left > PLAYABLE_WIDTH and level_connections.get('east'):
        load_level(f"{level_connections['east']}.txt")
        player.rect.right = 0
        #north
    elif player.rect.bottom < 0 and level_connections.get('north'):
        load_level(f"{level_connections['north']}.txt")
        player.rect.top = PLAYABLE_HEIGHT - player.rect.height
        #south
    elif player.rect.top > PLAYABLE_HEIGHT and level_connections.get('south'):
        load_level(f"{level_connections['south']}.txt")
        player.rect.bottom = 0

load_level(current_level_file)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    handle_level_swap()

    screen.fill(BACKGROUND_COLOR)
    layer1_sprites.draw(screen)  
    player_group.draw(screen)    
    layer2_sprites.draw(screen)

    ## LIGHTS
    light_manager.light_mask.fill(light_manager.current_time.value)
    
    for light in light_manager.light_surfaces: #side effect: all lights are at player
        light_x = player.rect.centerx - light[1]
        light_y = player.rect.centery - light[1]

        light_manager.light_mask.blit(light[0], (light_x, light_y), special_flags=pygame.BLEND_RGBA_ADD)
    screen.blit(light_manager.light_mask, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    health_text = hud_font.render(f"Health: {player_health}", True, (255, 100, 100))
    sanity_text = hud_font.render(f"Sanity: {player_sanity}", True, (150, 150, 255))
    location_text = hud_font.render(f"Room: {current_location}", True, (255, 255, 255))
    
    screen.blit(RelicaBeltSprite, RelicaBeltSpriteRect)
    screen.blit(health_text, (50, 1080 - 70))
    screen.blit(sanity_text, (350, 1080 - 70))
    screen.blit(location_text, (1500, 1080 - 70))
    screen.blit(crt_overlay, (0, 0))

    player_group.update(wall_sprites)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
