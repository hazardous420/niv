import pygame
import os
from assets import SPRITES
import level_parser
from classes import Player, Tile

#pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 800))
clock = pygame.time.Clock()
running = True

BACKGROUND_COLOR = (0, 0, 0)

grid_data = level_parser.load_grid_from_file(os.path.join("levels", "Ruins.txt"))
all_sprites, wall_sprites = level_parser.create_tile_sprites(grid_data)

player_frames = {
    'up':    [pygame.image.load(os.path.join("images", "characters", f"PlayerWalkUp{i+1}.png")).convert_alpha() for i in range(4)],#bru i forgot to end this one with 0 and 2 lazy 2 change
    'down':  [pygame.image.load(os.path.join("images", "characters", f"PlayerWalkDown{i}.png")).convert_alpha() for i in range(4)],
    'left':  [pygame.image.load(os.path.join("images", "characters", f"PlayerWalkLeft{i}.png")).convert_alpha() for i in range(4)],
    'right': [pygame.image.load(os.path.join("images", "characters", f"PlayerWalkRight{i+1}.png")).convert_alpha() for i in range(4)],

    'idle_down':  [pygame.image.load(os.path.join("images", "characters", f"PlayerIdle1.png")).convert_alpha() for i in range(1)],
    'idle_up':    [pygame.image.load(os.path.join("images", "characters", f"PlayerIdle2.png")).convert_alpha() for i in range(1)],
    'idle_left':  [pygame.image.load(os.path.join("images", "characters", f"PlayerIdle4.png")).convert_alpha() for i in range(1)],
    'idle_right': [pygame.image.load(os.path.join("images", "characters", f"PlayerIdle3.png")).convert_alpha() for i in range(1)],
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
