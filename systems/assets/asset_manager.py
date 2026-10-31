import pygame
from systems.assets.sprite import Sprite

class AssetManager:
    def __init__(self):
        self.sprites: dict[str, Sprite] = {}

    def add_sprite(self, sprite: Sprite) -> None:
        """Adds a pre-existing sprite to the list of available assets. Must be called for each sprite before it is usable."""
        if sprite == None: return

        # Add the sprite to the dictionary
        self.sprites[sprite.sprite_name] = sprite


    def get_sprite_from_name(self, sprite_name: str) -> Sprite:
        if self.sprites.get(sprite_name) == None: return Sprite() # TODO: add fallback sprite path for this case

        return self.sprites.get(sprite_name)