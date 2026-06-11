import math
from src.core.integrator import leapfrog_step
from src.io.loader import config_loader
def measure_period():
    bodies = config_loader()
    sun = bodies[0]
    earth = bodies[1]
    earth = bodies[1]
    dx = earth.position.x - sun.position.x
    dy = earth.position.y - sun.position.y
    theta_initial = math.atan2(dy,dx)
    dt = 3600
    steps = 8766
    step = 0
    threshold = 0.01
    theta_current = theta_initial
    while abs(theta_current - theta_initial) > threshold or step  <100:
        leapfrog_step(bodies, dt)
        step +=1
        dx = earth.position.x - sun.position.x
        dy = earth.position.y - sun.position.y
        theta_current = math.atan2(dy,dx) 
        
    days = step * dt / 86400  # convert seconds to days
    print(f"Earth orbital period: {days:.2f} days")

measure_period()