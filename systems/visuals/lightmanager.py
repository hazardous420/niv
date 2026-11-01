import pygame
from systems.visuals.light import AmbientLight, create_light_surf

class LightManager:
    def __init__(self, start_time: AmbientLight = AmbientLight.PITCH_BLACK):
        self.light_mask = pygame.Surface((1920, 1080))

        self.current_time = start_time

        self.light_surfaces: list[(pygame.Surface, int)] = []

    def add_light(self, light_radius: int) -> None:
        self.light_surfaces.append((create_light_surf(light_radius), light_radius))

    def update_sanity(self, sanity: int) -> None:
        if sanity <= 10:
            self.current_time = AmbientLight.PITCH_BLACK
        elif sanity <= 30:
            self.current_time = AmbientLight.NIGHT
        else:
            self.current_time = AmbientLight.DUSK
