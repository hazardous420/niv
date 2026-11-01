import pygame
from systems.globals.constants import DEFAULT_SPRITE_SCALE
import enum
import random
from systems.sounds.audio_effects import play_sound
from systems.sounds.player_sounds import footstep_sound, pickup_item_sound, pickup_gold_sound
from systems.entity.entity import Entity
from systems.visuals.crt import create_crt_overlay

class Rotation(enum.Enum):
    NONE = 0
    RANDOM = 1

unrot_table = ['6', '7', '8', '9', 'a', 'b', 'c', '2', 6, 7, 8, 9, 2]

class Item(pygame.sprite.Sprite):
    def __init__(self, item_id, col, row, image):
        super().__init__()
        self.item_id = item_id
        self.image = image
        self.rect = self.image.get_rect()
        
        self.rect.x = col * 32
        self.rect.y = row * 32

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

class Player(Entity):
    def __init__(self, x, y, sprite_sheet_dict, *groups):
        super().__init__(
            x,
            y,
            sprite_sheet_dict,
            groups=groups,
            health=20,
            speed=2,
            animation_speed=0.15
        )

        self.inventory = []
        self.gold = 0

        self.sanity = 100
        self.sanity_ratio = 0
        self.crt_thickness = 1
        self.crt_opacity = 255
        self.crt_spacing = 4

    def handle_input(self, wall_sprites, item_group):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        dx, dy = 0, 0

        if keys[pygame.K_LSHIFT]:
            self.speed = 3
            self.animation_speed = 0.25
        else:
            self.speed = 2
            self.animation_speed = 0.15

        if keys[pygame.K_g]:
            picked_up_items = pygame.sprite.spritecollide(
                self, item_group, True
            )
            for item in picked_up_items:
                print(f"{item.item_id} get")
                self.inventory.append(item.item_id)
                if item.item_id == "GoldPile":
                    self.gold += 20
                    play_sound(pickup_gold_sound, self.sanity)
                elif item.item_id == "GoldCoin":
                    self.gold += 1
                    play_sound(pickup_gold_sound, self.sanity)
                elif item.item_id == "GoldBag":
                    self.gold += 50
                    play_sound(pickup_gold_sound, self.sanity)
                else:
                    play_sound(pickup_item_sound, self.sanity)

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"
            self.is_moving = True
        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = "up"
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = "down"
            self.is_moving = True
        if self.is_moving:
            self.move(dx, dy, wall_sprites)

        if keys[pygame.K_p]:
            self.update_sanity(-1)

    def handle_sounds(self):
        if self.is_moving:
            current_int_frame = int(self.frame_index)
            if current_int_frame != self.prev_int_frame:
                if current_int_frame in (1, 3):
                    play_sound(footstep_sound, self.sanity)
                self.prev_int_frame = current_int_frame

    def update_sanity(self, amount):
        self.sanity = max(0, min(self.sanity + amount, 100))

        self.sanity_ratio = 1 - (self.sanity / 100)

        self.crt_thickness = 1 + int(self.sanity_ratio * 2)
        self.crt_opacity = 255
        self.crt_spacing = 4

    def update_crt(self):
        ratio = 1 - (self.sanity / 100)

        thickness = 1 + round(ratio * 3)
        spacing = 4 + round(ratio * 2)

        settings = (thickness, spacing)

        if settings != getattr(self, "crt_settings", None):
            self.crt_settings = settings

            self.crt_overlay = create_crt_overlay(
                1920,
                1080,
                line_spacing=spacing,
                thickness=thickness,
                opacity=255
            )

    def update(self, wall_sprites, item_group):
        self.handle_input(wall_sprites, item_group)
        self.update_animation()
        self.handle_sounds()
        self.update_crt()
        self.update_sanity(0)