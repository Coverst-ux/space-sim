import pygame
import threading
import math
import random
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

base_zoom = 800 / (4 * 1.496e11)
camera.zoom = base_zoom

background_stars = [
    (random.uniform(-5e12, 5e12), random.uniform(-5e12, 5e12), random.uniform(-5e12, 5e12))
    for _ in range(150)
]

running = True
paused = False


def physics_loop():
    global running, paused
    while True:
        with lock:
            if not running:
                break
            should_step = not paused

        if should_step:
            with lock:
                leapfrog_step(bodies, 3600)


t = threading.Thread(target=physics_loop)
t.daemon = True
t.start()

font = pygame.font.SysFont("monospace", 20)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with lock:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.zoom_in()
            elif event.button == 5:
                camera.zoom_out()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                with lock:
                    paused = not paused

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera.rotate_azimuth(-0.03)
    if keys[pygame.K_RIGHT]:
        camera.rotate_azimuth(0.03)
    if keys[pygame.K_UP]:
        camera.rotate_elevation(-0.03)
    if keys[pygame.K_DOWN]:
        camera.rotate_elevation(0.03)

    blur_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    blur_surface.fill((0, 0, 0, 12))
    screen.blit(blur_surface, (0, 0))

    for star in background_stars:
        star_pos = camera.world_to_screen(star[0], star[1], star[2])
        try:
            pygame.draw.circle(screen, (70, 75, 90), (int(star_pos[0]), int(star_pos[1])), 1)
        except (IndexError, TypeError):
            continue

    render_snapshot = []
    with lock:
        for body in bodies:
            render_snapshot.append((
                body.position.x, body.position.y, body.position.z,
                body.velocity.x, body.velocity.y, body.velocity.z
            ))

    log_speeds = []
    for x, y, z, vx, vy, vz in render_snapshot:
        speed = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
        log_speeds.append(math.log10(max(1.0, speed)))

    if log_speeds:
        min_log = min(log_speeds)
        max_log = max(log_speeds)
    else:
        min_log, max_log = 2.2, 7.2

    log_range = max_log - min_log if max_log != min_log else 1.0

    for i, (x, y, z, vx, vy, vz) in enumerate(render_snapshot):
        screen_pos = camera.world_to_screen(x, y, z)
        try:
            radius = max(1, min(6, int(2 * camera.zoom / base_zoom)))
            current_log = log_speeds[i]

            factor = (current_log - min_log) / log_range
            factor = max(0.0, min(1.0, factor))

            # Mathematical cliff: Compresses low-mid speeds to keep outer arms teal
            factor = factor ** 3.8

            if factor < 0.5:
                # Stage 1 LERP: Deep Teal (20, 100, 220) -> Blazing Orange (255, 110, 0)
                val_t = factor / 0.5
                r = int(20 + (255 - 20) * val_t)
                g = int(100 + (110 - 100) * val_t)
                b = int(220 + (0 - 220) * val_t)
            else:
                # Stage 2 LERP: Blazing Orange (255, 110, 0) -> White-Hot Yellow (255, 240, 150)
                val_t = (factor - 0.5) / 0.5
                r = int(255)
                g = int(110 + (240 - 110) * val_t)
                b = int(0 + (150 - 0) * val_t)

            glow_color = (
                max(0, min(255, r)),
                max(0, min(255, g)),
                max(0, min(255, b))
            )

            pygame.draw.circle(screen, glow_color, (int(screen_pos[0]), int(screen_pos[1])), radius)

        except Exception:
            continue

    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.0f} | N: {len(bodies)}", True, (180, 180, 180))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()