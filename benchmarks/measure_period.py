import math
from src.core.integrator import leapfrog_step
from src.io.loader import config_loader
def measure_period():
    bodies = config_loader()
    sun = bodies[0]
    earth = bodies[1]
    dx = earth.position.x - sun.position.x
    dy = earth.position.y - sun.position.y
    theta_initial = math.atan2(dy,dx)
    dt = 3600
    steps = 8766
    step = 0
    threshold = 0.01
    theta_current = theta_initial
    theta_prev = theta_initial
    total_angle = 0.0
    while abs(total_angle) < (2 * math.pi):
        leapfrog_step(bodies, dt)
        step +=1
        dx = earth.position.x - sun.position.x
        dy = earth.position.y - sun.position.y
        theta_current = math.atan2(dy,dx) 
        delta_theta = theta_current - theta_prev

        if delta_theta < -math.pi:
            delta_theta += (2* math.pi)
        elif delta_theta > math.pi:
            delta_theta -= (2* math.pi)
        total_angle += delta_theta
        theta_prev = theta_current
    days = step * dt / 86400  # convert seconds to days
    print(f"Earth orbital period: {days:.2f} days")

measure_period()