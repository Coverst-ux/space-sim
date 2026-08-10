import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
import threading
import math
import random
import time
from src.core.spawn import generate_binary_white_dwarfs
from src.rendering.camera import Camera
from src.rendering.glow import create_glow_texture, draw_star
import space_sim_cpp
from src.rendering.visual_particle import VisualParticle, spawn_particle

pygame.init()
SCREEN_W, SCREEN_H = 800, 800
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# masses in kg (roughly 0.6 and 0.8 solar masses — typical WD masses)

m1 = 0.6 * 1.989e30
m2 = 0.8 * 1.989e30
position = space_sim_cpp.Vector3D(0, 0, 0)
separation = 1.25e7
dt = 0.005
STEPS_PER_FRAME = 20

physics_bodies, render_bodies = generate_binary_white_dwarfs(
    m1, m2, position, separation
)

lock = threading.Lock()

space_sim_cpp.leapfrog_step(
    physics_bodies,
    dt,
    is_first_step=True
)

camera = Camera(SCREEN_W, SCREEN_H)

base_zoom = 800 / (4 * separation)
camera.zoom = base_zoom

background_stars = [
    (
        random.uniform(-5e12, 5e12),
        random.uniform(-5e12, 5e12),
        random.uniform(-5e12, 5e12)
    )
    for _ in range(150)
]

running = True
paused = False
frame_count = 0
steps_taken = 0
active_particles = []
PARTICLE_LIFETIME = 700          
PARTICLE_SPAWN_INTERVAL = 5      # spawn a new particle every N physics substeps


def physics_loop():
    global running, paused, steps_taken

    while True:
        with lock:
            if not running:
                break

            should_step = not paused

        if should_step:
            with lock:
                for _ in range(STEPS_PER_FRAME):
                    space_sim_cpp.leapfrog_step(physics_bodies, dt)
                    space_sim_cpp.update_binaries(physics_bodies, dt)
                    steps_taken += 1
                    if steps_taken % PARTICLE_SPAWN_INTERVAL == 0:
                        active_indices = [i for i in range(len(physics_bodies)) if physics_bodies[i].active]
                        
                        if active_indices:
                            chosen_index = random.choice(active_indices)
                            chosen_body = physics_bodies[chosen_index]
                            chosen_render_body = render_bodies[chosen_index]
                            star_position = (chosen_body.position.x, chosen_body.position.y, chosen_body.position.z)
                            star_velocity = (chosen_body.velocity.x, chosen_body.velocity.y, chosen_body.velocity.z)
                            star_radius = chosen_body.radius
                            
                            result = spawn_particle(star_position, star_velocity, star_radius, chosen_render_body.color, PARTICLE_LIFETIME)
                            active_particles.append(result)


                for rb in render_bodies:
                    rb.record_trail()
            time.sleep(1 / 60)
        else:
            time.sleep(0.001)


t = threading.Thread(target=physics_loop)
t.daemon = True

font = pygame.font.SysFont("monospace", 20)
pygame.display.flip()
t.start()


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

    screen.fill((0, 0, 0))

    for star in background_stars:

        star_pos = camera.world_to_screen(
            star[0],
            star[1],
            star[2]
        )

        if star_pos is None:
            continue

        try:
            pygame.draw.circle(
                screen,
                (70, 75, 90),
                (int(star_pos[0]), int(star_pos[1])),
                1
            )
        except (IndexError, TypeError):
            continue


    render_snapshot = []
    trail_snapshot = []

    with lock:
        for i, rb in enumerate(render_bodies):
            physics_body = physics_bodies[i]
            if not physics_body.active:
                continue
            if physics_body.just_merged:
                physics_body.just_merged = False
            render_snapshot.append((    
                physics_body.position.x,
                physics_body.position.y,
                physics_body.position.z,
                rb.color,
                rb.glow_texture,
                physics_body.radius
            ))
            
            trail_snapshot.append((rb.color, list(rb.trail)))
        elapsed_time = steps_taken * dt
        
    attractors = [(x, y, z) for x, y, z, color, glow_texture, radius in render_snapshot]

    for particle in active_particles:
        particle.update(dt, attractors)

    active_particles = [p for p in active_particles if p.is_alive()]

        
    for color, trail in trail_snapshot:
        n = len(trail)
        if n == 0:
            continue
        for i, (tx, ty, tz) in enumerate(trail):
            screen_pos = camera.world_to_screen(tx, ty, tz)
            if screen_pos is None:
                continue
            age = i / (n - 1) if n > 1 else 1.0
            faded_color = tuple(int(c * age) for c in color)
            pygame.draw.circle(screen, faded_color, (int(screen_pos[0]), int(screen_pos[1])), 1)
            
            
    for particle in active_particles:
        screen_pos = camera.world_to_screen(*particle.position)
        if screen_pos is None:
            continue
        age_fraction = particle.age / particle.lifetime
        faded_color = tuple(int(c * (1 - age_fraction)) for c in particle.color)
        pygame.draw.circle(screen, faded_color, (int(screen_pos[0]), int(screen_pos[1])), 1)
        


    for x, y, z, color, glow_texture, radius in render_snapshot:

        screen_pos = camera.world_to_screen(x, y, z)

        if screen_pos is None:
            continue

        try:
            GLOW_RADIUS_MULTIPLIER = 1.5
            glow_radius = radius * GLOW_RADIUS_MULTIPLIER
            draw_star(screen, glow_texture, (int(screen_pos[0]), int(screen_pos[1])), color, camera.zoom,
                    base_radius=glow_radius, core_radius = radius * 0.3 )
        except Exception:
            continue


    fps = clock.get_fps()
    
    fps_text = font.render(
        f"FPS: {fps:.0f} | t={elapsed_time:.0f}s",
        True,
        (180, 180, 180)
    )

    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()