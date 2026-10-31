import pygame
from systems.visuals.light import AmbientLight, create_light_surf

class LightManager:
    def __init__(self, start_time: AmbientLight = AmbientLight.NIGHT):
        self.light_mask = pygame.Surface((1920, 1080))

        self.current_time = start_time

        self.light_surfaces: list[(pygame.Surface, int)] = []

    def add_light(self, light_radius: int) -> None:
        self.light_surfaces.append((create_light_surf(light_radius), light_radius))
