import pygame
from src.io.loader import config_loader
from src.core.integrator import euler_step
from src.rendering.renderer import world_to_screen

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
bodies = config_loader()
SCREEN_W, SCREEN_H = 800, 800
SCALE = 800 / (4 * 1.496e11)
OFFSET = (SCREEN_W // 2, SCREEN_H // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #screen.fill((0,0,0))
    STEPS_PER_FRAME = 100

# inside the loop, replace euler_step(bodies, 3600) with:
    for _ in range(STEPS_PER_FRAME):
        euler_step(bodies, 3600)
    
    for body in bodies:
        screen_pos = world_to_screen(body.position, SCALE, OFFSET)
        pygame.draw.circle(screen, body.color, screen_pos, 10)

    pygame.display.flip()
    clock.tick(60)  # 60 fps

pygame.quit()