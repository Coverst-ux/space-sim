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
    1.0, # omega
    sim.Vector3D(0.0,0.0,1.0)
)

alpha = math.radians(30)
simulation_time = 0.0
step_length = 0.02 * config.stellar_radius  
maximum_steps = 2000
outer_boundary = 8 * config.stellar_radius
font_path = pygame.font.match_font("Segoe UI")
font = pygame.font.Font(font_path, 20)
title_font = pygame.font.Font(font_path, 22)
label_font = pygame.font.Font(font_path, 18)

title_surface = title_font.render("Pulsar", True, (235, 240, 250))
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


def rotate_field_point(point, alpha, phase):
    tilted_x = (
        point.x * math.cos(alpha)
        + point.z * math.sin(alpha)
    )

    tilted_y = point.y

    tilted_z = (
        -point.x * math.sin(alpha)
        + point.z * math.cos(alpha)
    )

    rotated_x = (
        tilted_x * math.cos(phase)
        - tilted_y * math.sin(phase)
    )

    rotated_y = (
        tilted_x * math.sin(phase)
        + tilted_y * math.cos(phase)
    )

    rotated_z = tilted_z

    return sim.Vector3D(
        rotated_x,
        rotated_y,
        rotated_z
    )


def draw_beam(surface, camera, direction, length, width,  color):
    start = sim.Vector3D(0.0,0.0,0.0)
    end = direction.mult(length)
    
    start_screen = camera.world_to_screen(
        start.x,
        start.y,
        start.z
    )    
    
    end_screen = camera.world_to_screen(
        end.x,
        end.y,
        end.z
    )
    
    if start_screen is None or end_screen is None:
        return
    
    pygame.draw.line(surface, color, start_screen, end_screen, round(width))
    
def random_star_brightness():
    roll = random.random()

    if roll < 0.8:
        return random.randint(45, 90)
    elif roll < 0.97:
        return random.randint(100, 160)
    else:
        return random.randint(180, 240)

seed_radius = 1.3 * config.stellar_radius
theta_values = [math.radians(38), math.radians(46), math.radians(54), math.radians(62), math.radians(70)]
phi_values = [i * math.pi / 3 for i in range(6)]
field_lines = []

for theta in theta_values:
    for phi in phi_values:
        seed_position= sim.Vector3D(
            seed_radius * math.sin(theta) * math.cos(phi),
            seed_radius * math.sin(theta) * math.sin(phi),
            seed_radius * math.cos(theta)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
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
    phase = config.omega * simulation_time
    magnetic_axis = sim.Vector3D(
    math.sin(alpha) * math.cos(phase),
    math.sin(alpha) * math.sin(phase),
    math.cos(alpha)
    )
    
    beam_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    beam_width = 8
    beam_length = 30 * config.stellar_radius
    
    draw_beam(beam_surface, camera, magnetic_axis, beam_length, beam_width * 1.8, (100, 170, 255, 35))
    draw_beam(beam_surface, camera, magnetic_axis, beam_length, beam_width * 1.3, (120, 185, 255, 70))
    draw_beam(beam_surface, camera, magnetic_axis, beam_length, beam_width, (170, 220, 255, 130))

    draw_beam(beam_surface, camera, magnetic_axis.mult(-1), beam_length, beam_width * 1.8, (100, 170, 255, 35))
    draw_beam(beam_surface, camera, magnetic_axis.mult(-1), beam_length, beam_width * 1.3, (120, 185, 255, 70))
    draw_beam(beam_surface, camera, magnetic_axis.mult(-1), beam_length, beam_width, (170, 220, 255, 130))
    screen.blit(beam_surface,(0,0))
    config.magnetic_axis = magnetic_axis
    # TODO:: Improve field line depth and visualization
    field_surface = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    star_radius = config.stellar_radius
    field_line_width = 1 

    for field_line in field_lines:

        for i in range(len(field_line) - 1):
            point1 = rotate_field_point(field_line[i], alpha, phase)
            point2 = rotate_field_point(field_line[i+1], alpha, phase)

            px1, py1, depth1 = camera.world_to_camera(
                point1.x,
                point1.y,
                point1.z
            )
            
            px2, py2, depth2 = camera.world_to_camera(
                point2.x,
                point2.y,
                point2.z
            )
            
                

            screen_x1 = round(
                px1 * camera.zoom + camera.offset_x
            )
            
            screen_x2 = round(
                px2 * camera.zoom + camera.offset_x
            )

            screen_y1 = round(
                py1 * camera.zoom + camera.offset_y
            )
            screen_y2= round(
                py2 * camera.zoom + camera.offset_y
            )

            segment_depth = (depth1 + depth2) / 2
            mid_px = (px1 + px2) / 2
            mid_py = (py1 + py2) / 2
            projected_distance_squared = (mid_px * mid_px + mid_py * mid_py)
            star_radius_squared = star_radius * star_radius

            hidden_by_star = False

            if projected_distance_squared < star_radius_squared:
                star_surface_depth = math.sqrt(
                    star_radius_squared
                    - projected_distance_squared
                )

                if segment_depth < star_surface_depth:
                    hidden_by_star = True

            if hidden_by_star:
                continue
            pygame.draw.line(
                field_surface,
                (180, 210, 255, 210),
                (screen_x1, screen_y1),
                (screen_x2, screen_y2),
                field_line_width
            )

    screen.set_clip(None)
# =============================================================================
    # CONTROL PANEL 
    
    panel_x = visualization_width + 28
    panel_y = 32
    row_gap = 34


    screen.blit(title_surface, (panel_x, panel_y))

    labels = [
        f"Omega:   {config.omega}",
        f"Tilt:    {math.degrees(alpha):.0f}°",
        f"Field:   {config.polar_field_strength}",
        f"Paused:  {'Yes' if paused else 'No'}"
    ]

    for i, text in enumerate(labels):
        label_surface = label_font.render(text, True, (200, 210, 225))
        screen.blit(
            label_surface,
            (panel_x, panel_y + 48 + i * row_gap)
        )

    screen.set_clip(visualization_area)

    screen.blit(field_surface, (0, 0))
    
    screen.set_clip(None)


    dt = clock.tick(60) / 1000.0
    if not paused:
        simulation_time += dt
    pygame.display.update()