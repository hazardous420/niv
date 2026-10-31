import pygame
from enum import Enum

class AmbientLight(Enum):
    DAY = (255, 255, 255)
    OVERCAST = (180, 180, 190)
    DUSK = (100, 70, 70)
    NIGHT = (30, 30, 50)
    PITCH_BLACK = (5, 5, 5)



def create_light_surf(radius, color=(255, 255, 255)):
    light_surf = pygame.Surface((radius * 2, radius * 2))
    light_surf.fill((0, 0, 0)) 
    for i in range(radius, 0, -1):
        distance_ratio = i / radius
        intensity = (1 - distance_ratio) ** 1.5
            
        r = int(color[0] * intensity)
        g = int(color[1] * intensity)
        b = int(color[2] * intensity)
          
        pygame.draw.circle(light_surf, (r, g, b), (radius, radius), i)
            
    return light_surf