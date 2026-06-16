import pygame
from src.core.spawn import generate_random_bodies
from src.core.integrator import leapfrog_step
from src.rendering.camera import Camera

pygame.init()
SCREEN_W, SCREEN_H = 800, 800
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

bodies = generate_random_bodies(750)
camera = Camera(SCREEN_W, SCREEN_H)
camera.zoom = 800 / (4 * 1.496e11)
running = True
STEPS_PER_FRAME = 1

while running:
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.zoom_in()
            elif event.button == 5:
                camera.zoom_out()

    # 2. Clear Screen
    screen.fill((0, 0, 0))

    # 3. Physics Updates
    for _ in range(STEPS_PER_FRAME):
        leapfrog_step(bodies, 3600)
        # for body in bodies:
        #     # body.record_trail()
    
    # 4. Rendering (With the White Line Trail Engine)
    for body in bodies:
        screen_pos = camera.world_to_screen(body.position.x,body.position.y)
        
        # Draw the continuous white trail line
        # if len(body.trail) > 1:
        #     pixel_trail = [camera.world_to_screen(wx, wy) for wx, wy in body.trail]
        #     pygame.draw.lines(screen, (255, 255, 255), False, pixel_trail, 2)

        # Draw the physical body on top of its trail
        # Making the Sun stand out visually from the planets
        # if body.name.lower() == "sun":
        #     radius = int(25*(camera.zoom / ( 800/ (4* 1.496e11))))
        #     radius = max(4, radius)
        # else:
        #     scale_factor = camera.zoom / (800 / (4 * 1.496e11))
        #     radius = int(5 * scale_factor)
        #     radius = max(3, radius) # Force planets to stay a clear 3-pixel dot minimum
        #
        # pygame.draw.circle(screen, body.color, screen_pos, radius)
        screen.set_at(screen_pos, body.color)

    # 5. Flip Display
    fps = clock.get_fps()
    fps_text = pygame.font.SysFont("monospace", 20).render(f"FPS: {fps:.0f} | N: {len(bodies)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)  # 60 fps

pygame.quit()