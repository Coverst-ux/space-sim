import pygame
from src.io.loader import config_loader
import sys
sys.path.append(r"C:\Users\Admin\Documents\hell_in_a_folder\bindings")
import space_sim_cpp
from src.rendering.camera import Camera

pygame.init()
SCREEN_W, SCREEN_H = 800, 800
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

physics_bodies, render_bodies = config_loader()
camera = Camera(SCREEN_W, SCREEN_H)
camera.zoom = 800 / (4 * 1.496e11)
running = True
STEPS_PER_FRAME = 100
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.zoom_in()
            elif event.button == 5:
                camera.zoom_out()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera.rotate_azimuth(-0.05)
    if keys[pygame.K_RIGHT]:
        camera.rotate_azimuth(0.05)
    if keys[pygame.K_UP]:
        camera.rotate_elevation(0.05)
    if keys[pygame.K_DOWN]:
        camera.rotate_elevation(-0.05)

    screen.fill((0, 0, 0))

    if not paused:
        for _ in range(STEPS_PER_FRAME):
            space_sim_cpp.leapfrog_step(physics_bodies, 3600)
        for rb in render_bodies:
            rb.record_trail()

    for rb in render_bodies:
        screen_pos = camera.world_to_screen(rb.position.x, rb.position.y, rb.position.z)


        if len(rb.trail) > 1:
            pixel_trail = [camera.world_to_screen(wx, wy, wz) for wx, wy, wz in rb.trail]
            pygame.draw.lines(screen, (255, 255, 255), False, pixel_trail, 2)

        if rb.name.lower() == "sun":
            radius = int(25 * (camera.zoom / (800 / (4 * 1.496e11))))
            radius = max(4, radius)
        else:
            scale_factor = camera.zoom / (800 / (4 * 1.496e11))
            radius = int(5 * scale_factor)
            radius = max(3, radius)

        pygame.draw.circle(screen, rb.color, screen_pos, radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()