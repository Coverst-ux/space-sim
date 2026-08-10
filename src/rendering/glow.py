# src/rendering/glow.py

import pygame


def create_glow_texture(radius, color):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    for x in range(radius * 2):
        for y in range(radius * 2):
            dx = x - radius
            dy = y - radius
            distance = (dx * dx + dy * dy) ** 0.5

            if distance <= radius:
                t = distance / radius
                alpha = int((1 - t) ** 2 * 255)
                surface.set_at((x, y), (*color, alpha))

    return surface

def draw_star(screen, glow_texture, screen_pos, core_color, zoom, base_radius, core_radius):
    scaled_size = max(int(base_radius * zoom * 2), 1)
    scaled_glow = pygame.transform.smoothscale(glow_texture, (scaled_size, scaled_size))

    glow_pos = (
        screen_pos[0] - scaled_size // 2,
        screen_pos[1] - scaled_size // 2
    )
    screen.blit(scaled_glow, glow_pos)
    
    scaled_core_radius = max(int(core_radius * zoom), 1)
    pygame.draw.circle(screen, core_color, screen_pos, scaled_core_radius)


