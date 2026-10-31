import pygame
from systems.assets.sprite import Sprite
from systems.assets.asset_manager import AssetManager

# Global list of all sprites
sprites: dict[str, Sprite] = {
    # Idle
    "PlayerIdle1": Sprite("images/characters/PlayerIdle1.png", "PlayerIdle1"),
    "PlayerIdle2": Sprite("images/characters/PlayerIdle2.png", "PlayerIdle2"),
    "PlayerIdle3": Sprite("images/characters/PlayerIdle3.png", "PlayerIdle3"),
    "PlayerIdle4": Sprite("images/characters/PlayerIdle4.png", "PlayerIdle4"),
    
    # Walk Up
    "PlayerWalkUp1": Sprite("images/characters/PlayerWalkUp1.png", "PlayerWalkUp1"),
    "PlayerWalkUp2": Sprite("images/characters/PlayerWalkUp2.png", "PlayerWalkUp2"),
    "PlayerWalkUp3": Sprite("images/characters/PlayerWalkUp3.png", "PlayerWalkUp3"),
    "PlayerWalkUp4": Sprite("images/characters/PlayerWalkUp4.png", "PlayerWalkUp4"),

    # Walk Down
    "PlayerWalkDown0": Sprite("images/characters/PlayerWalkDown0.png", "PlayerWalkDown0"),
    "PlayerWalkDown1": Sprite("images/characters/PlayerWalkDown1.png", "PlayerWalkDown1"),
    "PlayerWalkDown2": Sprite("images/characters/PlayerWalkDown2.png", "PlayerWalkDown2"),
    "PlayerWalkDown3": Sprite("images/characters/PlayerWalkDown3.png", "PlayerWalkDown3"),

    # Walk Left
    "PlayerWalkLeft0": Sprite("images/characters/PlayerWalkLeft0.png", "PlayerWalkLeft0"),
    "PlayerWalkLeft1": Sprite("images/characters/PlayerWalkLeft1.png", "PlayerWalkLeft1"),
    "PlayerWalkLeft2": Sprite("images/characters/PlayerWalkLeft2.png", "PlayerWalkLeft2"),
    "PlayerWalkLeft3": Sprite("images/characters/PlayerWalkLeft3.png", "PlayerWalkLeft3"),

    # Walk Right
    "PlayerWalkRight1": Sprite("images/characters/PlayerWalkRight1.png", "PlayerWalkRight1"),
    "PlayerWalkRight2": Sprite("images/characters/PlayerWalkRight2.png", "PlayerWalkRight2"),
    "PlayerWalkRight3": Sprite("images/characters/PlayerWalkRight3.png", "PlayerWalkRight3"),
    "PlayerWalkRight4": Sprite("images/characters/PlayerWalkRight4.png", "PlayerWalkRight4"),

    # Tiles
    "Wall": Sprite("images/tiles/Wall.png", "Wall"),
    "Floor": Sprite("images/tiles/Floor.png", "Floor"),

    "BrickWall": Sprite("images/tiles/BrickWall.png", "BrickWall"),
    "WoodPlanks": Sprite("images/tiles/WoodPlanks.png", "WoodPlanks"),

    "Dirt": Sprite("images/tiles/Dirt.png", "Dirt"),
    "Grass": Sprite("images/tiles/Grass.png", "Grass"),

    "TreeBL": Sprite("images/tiles/TreeBL.png", "TreeBL"),
    "TreeBR": Sprite("images/tiles/TreeBR.png", "TreeBR"),
    "TreeBM": Sprite("images/tiles/TreeBM.png", "TreeBM"),

    "TreeTL": Sprite("images/tiles/TreeTL.png", "TreeTL"),
    "TreeTR": Sprite("images/tiles/TreeTR.png", "TreeTR"),
    "TreeTM": Sprite("images/tiles/TreeTM.png", "TreeTM"),

    "Trunk": Sprite("images/tiles/Trunk.png", "Trunk"),

    # Items
    "RelicaBelt": Sprite("images/items/BeltOfRelica.png", "RelicaBelt"),
}

def load_assetmanager(assetmanager: AssetManager) -> None:
    for sprite_name, sprite in sprites.items():
        assetmanager.add_sprite(sprite)
        print(f"Loaded sprite: {sprite_name}")