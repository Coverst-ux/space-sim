import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import random
import math
from src.rendering.camera import Camera
from src.rendering.glow import create_glow_texture, draw_star
import space_sim_cpp as sim
pygame.init()

camera = Camera(1200, 800)
screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE)
camera.zoom = 60
pygame.display.set_caption("Simulation")

pulsar_glow = create_glow_texture(
    radius = 40,
    color = (70, 120, 255)
)
config = sim.PulsarConfig(
    1.0, # stellar radius
    1.0, # speed of light 
    1.0, # polar field strength
    0.1, # omega
    sim.Vector3D(0.0,0.0,1.0)
)
step_length = 0.02 * config.stellar_radius  
maximum_steps = 2000
outer_boundary = 8 * config.stellar_radius

# calculation
def trace_field_line(seed_position, direction_sign):
    position = seed_position
    field_line_points = [position]
    
    for _ in range(maximum_steps):
        B = sim.get_magnetic_field(config, position)
        direction = B.normalized()
        displacement = direction.mult(step_length * direction_sign) 
        position = displacement + position  
        distance = position.magnitude()
        if distance <= config.stellar_radius or distance >= outer_boundary:
            break
        field_line_points.append(position)
    return field_line_points




def random_star_brightness():
    roll = random.random()

    if roll < 0.8:
        return random.randint(45, 90)
    elif roll < 0.97:
        return random.randint(100, 160)
    else:
        return random.randint(180, 240)

seed_distances = [1.2, 1.4, 1.7, 2.0, 2.4]
angles = [i * math.pi / 3 for i in range(6)]
field_lines =[]

for distance in seed_distances:
    for angle in angles:
        seed_position= sim.Vector3D(
            distance * config.stellar_radius * math.cos(angle),
            distance * config.stellar_radius * math.sin(angle),
            0.0
        )
        positive_half = trace_field_line(seed_position, 1)
        negative_half = trace_field_line(seed_position, -1)
        complete_line = (
                list(reversed(negative_half))
                + positive_half[1:]
            )
        field_lines.append(complete_line)
        
background_stars = [
    (
        random.uniform(-12, 12),
        random.uniform(-12, 12),
        random.uniform(-12, 12),
        random_star_brightness()
    )
    for _ in range(600)
]
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.zoom_in()
            elif event.button == 5:
                camera.zoom_out()
        
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        camera.rotate_azimuth(-0.03)

    if keys[pygame.K_RIGHT]:
        camera.rotate_azimuth(0.03)

    if keys[pygame.K_UP]:
        camera.rotate_elevation(-0.03)

    if keys[pygame.K_DOWN]:
        camera.rotate_elevation(0.03)
        
    window_width, window_height = screen.get_size()
    visualization_width = int(window_width * 0.75)
    panel_width = window_width - visualization_width
    visualization_area = pygame.Rect(
        0,
        0,
        visualization_width,
        window_height
    )
    
    
    control_panel = pygame.Rect(
        visualization_width,
        0,
        panel_width,
        window_height
    )
    
    panel_color = (30,35,45)
    border_color = (90,100,120)
    visualization_color = (15,18,24)

    camera.offset_x = visualization_area.centerx
    camera.offset_y = visualization_area.centery
    pygame.draw.rect(screen, visualization_color, visualization_area)
    
    pygame.draw.rect(
        screen,
        panel_color,
        control_panel,
    )
    
    pygame.draw.rect(
        screen,
        border_color,
        control_panel,
        width = 2
    )
    
    screen.set_clip(visualization_area)

    star_screen_pos = camera.world_to_screen(0,0,0)
    
    for star in background_stars:
        star_pos = camera.world_to_screen(
            star[0],
            star[1],
            star[2]
        )
        if star_pos is None:
            continue

        if visualization_area.collidepoint(star_pos):
            brightness = star[3]
            pygame.draw.circle(
                screen,
                (brightness, brightness, brightness),
                star_pos,
                1
            )
    if star_screen_pos is not None:
        draw_star(
            screen,
            pulsar_glow,
            star_screen_pos,
            core_color=(80,140,255),
            zoom= camera.zoom,
            base_radius= config.stellar_radius,
            core_radius= config.stellar_radius 
        )
    
    # rendering
    field_surface = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    star_radius = config.stellar_radius

    for field_line in field_lines:
        visible_segments = []
        current_segment = []

        for point in field_line:
            px, py, depth = camera.world_to_camera(
                point.x,
                point.y,
                point.z
            )

            screen_x = round(
                px * camera.zoom + camera.offset_x
            )

            screen_y = round(
                py * camera.zoom + camera.offset_y
            )

            projected_distance_squared = px * px + py * py
            star_radius_squared = star_radius * star_radius

            hidden_by_star = False

            if projected_distance_squared < star_radius_squared:
                star_surface_depth = math.sqrt(
                    star_radius_squared
                    - projected_distance_squared
                )

                if depth < star_surface_depth:
                    hidden_by_star = True

            if hidden_by_star:
                if len(current_segment) >= 2:
                    visible_segments.append(current_segment)

                current_segment = []
                continue

            current_segment.append(
                (screen_x, screen_y)
            )

        if len(current_segment) >= 2:
            visible_segments.append(current_segment)

        for segment in visible_segments:
            pygame.draw.lines(
                field_surface,
                (80, 110, 255, 40),
                False,
                segment,
                7
            )

            pygame.draw.lines(
                field_surface,
                (180, 205, 255, 190),
                False,
                segment,
                2
            )

    screen.blit(field_surface, (0, 0))

    screen.set_clip(None)

    clock.tick(60)
    pygame.display.update()