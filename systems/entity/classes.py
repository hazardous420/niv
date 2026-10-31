import pygame
import systems.assets.assets as assets
from systems.globals.constants import DEFAULT_SPRITE_SCALE
import enum
import random
from systems.sounds.player_sounds import footstep_sound

class Rotation(enum.Enum):
    NONE = 0
    RANDOM = 1

unrot_table = ['6', '7', '8', '9', 'a', 'b', 'c', '2', 6, 7, 8, 9, 2]

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, image):
        super().__init__()
        self.tile_type = tile_type
        orientation = 0
        if tile_type in unrot_table or str(tile_type) in unrot_table:
            self.rotation = Rotation.NONE
            orientation = 0
        else:
            self.rotation = Rotation.RANDOM
            orientation = random.choice([0, 90, 180, 270])   

        self.image = pygame.transform.rotate(image, orientation)
        print(f"Tile Type: {tile_type}, Orientation: {orientation}")
        
        self.rect = self.image.get_rect(topleft=(x * 32, y * 32))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet_dict, *groups):
        super().__init__(*groups)
        self.animations = sprite_sheet_dict
        
        self.direction = 'down'
        self.frame_index = 0
        self.is_moving = False

        self.prev_int_frame = 0
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
        
        current_int_frame = int(self.frame_index)
        current_frame = self.animations[anim_key][int(self.frame_index)]
        self.image = pygame.transform.scale(current_frame, DEFAULT_SPRITE_SCALE)

    def handle_sounds(self):
        if self.is_moving:
            current_int_frame = int(self.frame_index)

            if current_int_frame != self.prev_int_frame:
                if current_int_frame in (1, 3):
                    footstep_sound.play()
                self.prev_int_frame = current_int_frame

    def update(self, wall_sprites):
        self.handle_input(wall_sprites)
        self.update_animation()
        self.handle_sounds()
    