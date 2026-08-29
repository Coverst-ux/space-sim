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
seed_position = sim.Vector3D(1.5 * config.stellar_radius, 0, 0)
step_length = 0.02 * config.stellar_radius  
scale = 60
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
        field_line_points.append(position)
        distance = position.magnitude()
        if distance <= config.stellar_radius or distance >= outer_boundary:
            break
    return field_line_points


seed_distances = [1.3, 1.7, 2.2]
field_lines =[]

for distance in seed_distances:
    for side in (1, -1):
        seed_position= sim.Vector3D(
            side * distance * config.stellar_radius,
            0.0,
            0.0
        )
        positive_half = trace_field_line(seed_position, 1)
        negative_half = trace_field_line(seed_position, -1)
        complete_line = (
                list(reversed(negative_half))
                + positive_half[1:]
            )
        field_lines.append(complete_line)
        

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
    pygame.draw.circle(screen, (0,0,255), visualization_area.center, int(config.stellar_radius * scale ))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
    # rendering
    for field_line in field_lines:
        screen_points = []
        for point in field_line:
            screen_x = visualization_area.centerx + point.x * scale
            screen_y = visualization_area.centery - point.z * scale
            screen_points.append((screen_x, screen_y))
            
        if len(screen_points) >= 2:
            pygame.draw.lines(
                screen,
                (255, 0, 0),
                False,
                screen_points,
                2
            )

        
    
    clock.tick(60)
    pygame.display.update()