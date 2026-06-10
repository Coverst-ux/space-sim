import pygame
from src.io.loader import config_loader
from src.core.integrator import leapfrog_step
from src.rendering.renderer import world_to_screen

pygame.init()
SCREEN_W, SCREEN_H = 800, 800
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

bodies = config_loader()
SCALE = 800 / (4 * 1.496e11)
OFFSET = (SCREEN_W // 2, SCREEN_H // 2)

running = True
STEPS_PER_FRAME = 100

while running:
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Clear Screen
    screen.fill((0, 0, 0))

    # 3. Physics Updates
    for _ in range(STEPS_PER_FRAME):
        leapfrog_step(bodies, 3600)
    
    # 4. Rendering (With the White Line Trail Engine)
    for body in bodies:
        screen_pos = world_to_screen(body.position, SCALE, OFFSET)
        
        # Initialize the trail list dynamically if it doesn't exist yet
        if not hasattr(body, 'trail'):
            body.trail = []
            
        # Append current position to history
        body.trail.append(screen_pos)
        
        # Limit history size to protect memory
        if len(body.trail) > 85:
            body.trail.pop(0)

        # Draw the continuous white trail line
        if len(body.trail) > 1:
            pygame.draw.lines(screen, (255, 255, 255), False, body.trail, 2)

        # Draw the physical body on top of its trail
        # Making the Sun stand out visually from the planets
        radius = 15 if body.name.lower() == "sun" else 6
        pygame.draw.circle(screen, body.color, screen_pos, radius)

    # 5. Flip Display
    pygame.display.flip()
    clock.tick(60)  # 60 fps

pygame.quit()