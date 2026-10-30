from sprite import Sprite
from asset_manager import AssetManager

# Global list of all sprites
sprites: list[Sprite] = [
    Sprite("images/characters/PlayerIdle1.png"),
    Sprite("images/tiles/Wall.png"),
    Sprite("images/tiles/Floor.png"),
]

def load_assetmanager(assetmanager: AssetManager) -> None:
    for sprite in sprites:
        assetmanager.add_sprite(sprite)
        print("Loaded sprite: " + sprite.sprite_name)