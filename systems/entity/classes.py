import pygame
import systems.assets.assets as assets
from systems.globals.constants import DEFAULT_SPRITE_SCALE
import enum
import random

class Rotation(enum.Enum):
    NONE = 0
    RANDOM = 1

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, image):
        super().__init__()
        self.tile_type = tile_type
        rotation = Rotation.NONE if tile_type == 2 or tile_type == 3 else Rotation.RANDOM
  
        if rotation == Rotation.RANDOM:
            angle = random.choice([0, 90, 180, 270])
        else:
            angle = Rotation.NONE.value

        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect(topleft=(x * DEFAULT_SPRITE_SCALE[0], y * DEFAULT_SPRITE_SCALE[1]))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet_dict, *groups):
        super().__init__(*groups)
        self.animations = sprite_sheet_dict
        
        self.direction = 'down'
        self.frame_index = 0
        self.is_moving = False
        
        self.animation_speed = 0.15 

        self.image = pygame.transform.scale(self.animations[self.direction][self.frame_index], DEFAULT_SPRITE_SCALE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def handle_input(self, wall_sprites):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        dx, dy = 0, 0
        if keys[pygame.K_LSHIFT]:
            self.speed = 3
            self.animation_speed = 0.25
        else:
            self.speed = 2
            self.animation_speed = 0.15
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'
            self.is_moving = True
        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = 'up'
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = 'down'
            self.is_moving = True

        if self.is_moving:
            next_rect = self.rect.move(dx, dy)
            next_rect.inflate_ip(-8, -12)
            
            if not any(tile.rect.colliderect(next_rect) for tile in wall_sprites):
                self.rect.x += dx
                self.rect.y += dy

    def update_animation(self): #idle based on dir
        anim_key = self.direction if self.is_moving else f"idle_{self.direction}"

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[anim_key]):
            self.frame_index = 0

        current_frame = self.animations[anim_key][int(self.frame_index)]
        self.image = pygame.transform.scale(current_frame, DEFAULT_SPRITE_SCALE)
            
        current_frame = self.animations[anim_key][int(self.frame_index)]
        self.image = pygame.transform.scale(current_frame, DEFAULT_SPRITE_SCALE)

    def update(self, wall_sprites):
        self.handle_input(wall_sprites)
        self.update_animation()