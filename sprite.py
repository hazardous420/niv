import pygame
from constants import DEFAULT_SPRITE_SCALE

class Sprite:
    def __init__(self, path: str = "", sprite_name: str = "", initial_scale: float = 1.0):
        self.path: str = path
        self.sprite_name: str = path
        self.scale: float = initial_scale

        self.texture: pygame.Surface = pygame.image.load(path).convert_alpha()

    def scale_texture(self, scale: tuple[float, float]= DEFAULT_SPRITE_SCALE) -> None:
        """Scales this sprite's texture by a value."""
        pygame.transform.scale(self.texture, scale)