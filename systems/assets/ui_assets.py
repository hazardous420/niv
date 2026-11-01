import pygame

def create_ui_sprites(sprites):
    GoldCoinSprite = sprites["GoldCoin"].texture
    GoldCoinSprite = pygame.transform.scale(GoldCoinSprite, (32, 32))
    GoldCoinSpriteRect = GoldCoinSprite.get_rect(bottomright=(1900, 1040))

    RelicaBeltSprite = sprites["RelicaBelt"].texture
    RelicaBeltSpriteRect = RelicaBeltSprite.get_rect(midbottom=(1800 /2, 990))
    RelicaBeltSprite = pygame.transform.scale(RelicaBeltSprite, (RelicaBeltSprite.get_width() * 3.5, RelicaBeltSprite.get_height() * 3.5))

    return GoldCoinSprite, GoldCoinSpriteRect, RelicaBeltSprite, RelicaBeltSpriteRect