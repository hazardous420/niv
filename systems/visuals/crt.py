import pygame
import random


def apply_glitch(screen, sanity):
    if sanity >= 25:
        return

    intensity = (25 - sanity) / 25

    if random.random() > intensity:
        return

    width, height = screen.get_size()

    for _ in range(int(2 + intensity * 12)):
        y = random.randint(0, height - 1)
        strip_height = random.randint(1, int(3 + intensity * 15))
        offset = random.randint(
            -int(5 + intensity * 35),
            int(5 + intensity * 35)
        )

        strip_height = min(strip_height, height - y)

        strip = screen.subsurface(
            (0, y, width, strip_height)
        ).copy()

        screen.blit(strip, (offset, y))


def apply_static(screen, sanity):
    if sanity >= 40:
        return

    intensity = (40 - sanity) / 40

    noise = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    for _ in range(int(30 + intensity * 700)):
        x = random.randrange(screen.get_width())
        y = random.randrange(screen.get_height())

        shade = random.randint(70, 170)

        noise.set_at((x, y), (shade, shade, shade, random.randint(20, 65)))

    screen.blit(noise, (0, 0))


def apply_flicker(screen, sanity):
    if sanity >= 50:
        return

    intensity = (50 - sanity) / 50

    if random.random() < intensity * 0.07:
        brightness = random.randint(180, 220)

        overlay = pygame.Surface(screen.get_size())
        overlay.fill((brightness, brightness, brightness))

        screen.blit(
            overlay,
            (0, 0),
            special_flags=pygame.BLEND_RGB_MULT
        )


def create_crt_overlay(
    width: int,
    height: int,
    line_spacing: int = 4,
    thickness: int = 1,
    opacity: int = 255
) -> pygame.Surface:

    crt_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    scanline_color = (0, 0, 0, opacity)

    for y in range(0, height, line_spacing):
        pygame.draw.rect(
            crt_surface,
            scanline_color,
            (0, y, width, thickness)
        )

    return crt_surface


def do_sanity_vfx(screen, sanity):
    apply_glitch(screen, sanity)
    apply_static(screen, sanity)
    apply_flicker(screen, sanity)