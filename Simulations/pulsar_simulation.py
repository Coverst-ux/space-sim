import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import space_sim_cpp as sim
pygame.init()

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")

config = sim.PulsarConfig(
    1.0, # stellar radius
    1.0, # speed of light 
    1.0, # polar field strength
    0.1, # omega
    sim.Vector3D(0.0,0.0,1.0)
)
position = sim.Vector3D(0.0, 0.0, 1.5)
visual_length = config.stellar_radius * 0.75
scale = 60

clock = pygame.time.Clock()

running = True

while running:
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
    pygame.draw.circle(screen, (0,0,255), visualization_area.center, config.stellar_radius * scale )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
    B = sim.get_magnetic_field(config, position)
    direction = B.normalized()
    visual_direction = direction.mult(visual_length)
    endpoint = visual_direction + position
    screenx = visualization_area.centerx + position.x * scale
    screeny = visualization_area.centery - position.z * scale
    endscreenx = visualization_area.centerx + endpoint.x * scale
    end_screeny = visualization_area.centery - endpoint.z * scale
    start_screen = (screenx, screeny)
    end_screen = (endscreenx, end_screeny)
    pygame.draw.line(screen, (255, 0, 0), start_screen, end_screen)

    
    clock.tick(60)
    pygame.display.update()