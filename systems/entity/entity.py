import pygame
from systems.globals.constants import DEFAULT_SPRITE_SCALE


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, animations, groups=(), health=20, speed=2, animation_speed=0.15):
        super().__init__(*groups)
        
        self.animations = animations

        self.direction = "down"
        self.frame_index = 0
        self.is_moving = False

        self.prev_int_frame = 0
        self.animation_speed = animation_speed
        self.speed = speed

        self.health = health
        self.max_health = health

        self.image = pygame.transform.scale(self.animations["idle_down"][0], DEFAULT_SPRITE_SCALE)
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy, wall_sprites):
        coll_rect = self.rect.inflate(-8, -12)
        if dx:
            coll_rect.x += dx

            if not any(tile.rect.colliderect(coll_rect) for tile in wall_sprites):
                self.rect.x += dx

        coll_rect = self.rect.inflate(-8, -12)
        if dy:
            coll_rect.y += dy

            if not any(tile.rect.colliderect(coll_rect) for tile in wall_sprites):
                self.rect.y += dy

    def update_animation(self):
        anim_key = self.direction if self.is_moving else f"idle_{self.direction}"
        animation = self.animations[anim_key]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        current_int_frame = int(self.frame_index)
        current_frame = animation[current_int_frame]

        old_center = self.rect.center

        self.image = pygame.transform.scale(
            current_frame,
            DEFAULT_SPRITE_SCALE
        )

        self.rect = self.image.get_rect(center=old_center)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            self.die()

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def die(self):
        self.kill() #murk le sprite

    def update(self, wall_sprites, item_group):
        self.update_animation()
    