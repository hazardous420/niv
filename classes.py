import pygame
import assets
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, image):
        super().__init__()
        self.tile_type = tile_type

        angle = random.choice([0, 90, 180, 270])
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect(topleft=(x * assets.SCALE[0], y * assets.SCALE[1]))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet_dict, *groups):
        super().__init__(*groups)
        self.animations = sprite_sheet_dict
        
        self.direction = 'down'
        self.frame_index = 0
        self.is_moving = False
        
        self.animation_speed = 0.15 

        self.image = pygame.transform.scale(self.animations[self.direction][self.frame_index], assets.SCALE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def handle_input(self, wall_sprites):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        dx, dy = 0, 0

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

    def update_animation(self):
        if self.is_moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0
            
        current_frame = self.animations[self.direction][int(self.frame_index)]
        self.image = pygame.transform.scale(current_frame, assets.SCALE)

    def update(self, wall_sprites):
        self.handle_input(wall_sprites)
        self.update_animation()