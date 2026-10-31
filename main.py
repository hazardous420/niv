## PYGAME
import pygame
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

## STD
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

grid_data: list = level_parser.load_grid_from_file(os.path.join("levels", "CityCenter.txt"))
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
player = Player(200,200, player_frames, player_group)

player_health = 100
player_sanity = 85
current_location = "City Center"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)
    player_group.draw(screen)


    ## LIGHTS
    light_manager.light_mask.fill(light_manager.current_time.value)
    
    for light in light_manager.light_surfaces: #side effect: all lights are at player
        light_x = player.rect.centerx - light[1]
        light_y = player.rect.centery - light[1]

        light_manager.light_mask.blit(light[0], (light_x, light_y), special_flags=pygame.BLEND_RGBA_ADD)
    screen.blit(light_manager.light_mask, (0, 0), special_flags=pygame.BLEND_RGB_MULT)


    health_text = hud_font.render(f"Health: {player_health}", True, (255, 100, 100))
    sanity_text = hud_font.render(f"Sanity: {player_sanity}", True, (150, 150, 255))
    location_text = hud_font.render(f"Location: {current_location}", True, (255, 255, 255))

    screen.blit(health_text, (50, 1080 - 70))
    screen.blit(sanity_text, (350, 1080 - 70))
    screen.blit(location_text, (1500, 1080 - 70))

    player_group.update(wall_sprites)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
