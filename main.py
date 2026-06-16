import pygame
import threading
from src.core.spawn import generate_spiral
from src.core.integrator import leapfrog_step
from src.rendering.camera import Camera

pygame.init()
SCREEN_W, SCREEN_H = 800, 800
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

bodies = generate_spiral(750)
lock = threading.Lock()
leapfrog_step(bodies, 3600, is_first_step=True)
camera = Camera(SCREEN_W, SCREEN_H)
camera.zoom = 800 / (4 * 1.496e11)
running = True

def physics_loop():
    while running:
        with lock:
            leapfrog_step(bodies, 3600)

t = threading.Thread(target=physics_loop)
t.daemon = True
t.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.zoom_in()
            elif event.button == 5:
                camera.zoom_out()

    blur_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    blur_surface.fill((0, 0, 0, 25))
    screen.blit(blur_surface, (0, 0))

    with lock:
        for body in bodies:
            screen_pos = camera.world_to_screen(body.position.x, body.position.y)
            screen.set_at(screen_pos, body.color)

    fps = clock.get_fps()
    fps_text = pygame.font.SysFont("monospace", 20).render(f"FPS: {fps:.0f} | N: {len(bodies)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()