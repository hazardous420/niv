## PYGAME
import pygame
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

## STD
import os
from enum import Enum

## SELF
import systems.world.level_parser as level_parser
from systems.entity.classes import Player, Tile
from systems.globals.constants import BACKGROUND_COLOR
from systems.assets.asset_manager import AssetManager
from systems.assets.sprite import Sprite
from systems.assets.assets import sprites, load_assetmanager

pygame.font.init()
hud_font = pygame.font.Font("assets/fonts/alagard.ttf", 30)

clock: pygame.time.Clock = pygame.time.Clock()
running: bool = True

class AmbientLight(Enum):
    DAY = (255, 255, 255)
    OVERCAST = (180, 180, 190)
    DUSK = (100, 70, 70)
    NIGHT = (30, 30, 50)
    PITCH_BLACK = (5, 5, 5)

def create_light_surf(radius, color=(255, 255, 255)):
    light_surf = pygame.Surface((radius * 2, radius * 2))
    light_surf.fill((0, 0, 0)) 
    for i in range(radius, 0, -1):
        distance_ratio = i / radius
        intensity = (1 - distance_ratio) ** 1.5
        
        r = int(color[0] * intensity)
        g = int(color[1] * intensity)
        b = int(color[2] * intensity)
        
        pygame.draw.circle(light_surf, (r, g, b), (radius, radius), i)
        
    return light_surf

#light vars
current_time = AmbientLight.NIGHT
light_mask = pygame.Surface((1920, 1080))
player_light_radius = 200
player_light_surf = create_light_surf(player_light_radius)

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

    light_mask.fill(current_time.value)
    light_x = player.rect.centerx - player_light_radius
    light_y = player.rect.centery - player_light_radius

    light_mask.blit(player_light_surf, (light_x, light_y), special_flags=pygame.BLEND_RGBA_ADD)
    screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

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
