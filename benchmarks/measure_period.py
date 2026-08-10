import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
import space_sim_cpp
from src.core.integrator import leapfrog_step as py_leapfrog_step
from src.io.loader import config_loader_python


def measure_all_periods_python():
    # Load a fresh batch of bodies from your config
    bodies = config_loader_python()
    sun = bodies[0]
    
    # Loop through every planet starting from index 1 to the end
    for i in range(1, len(bodies)):
        planet = bodies[i]
        
        # Reload bodies every time so each planet starts fresh from Day 0
        current_bodies = config_loader_python()
        current_sun = current_bodies[0]
        current_planet = current_bodies[i]
        
        dx = current_planet.position.x - current_sun.position.x
        dy = current_planet.position.y - current_sun.position.y
        theta_initial = math.atan2(dy, dx)
        
        dt = 3600  # 1 hour steps
        step = 0
        theta_prev = theta_initial
        total_angle = 0.0
        
        # Run your exact math loop for this specific planet
        while abs(total_angle) < (2 * math.pi):
            py_leapfrog_step(current_bodies, dt)
            step += 1
            
            dx = current_planet.position.x - current_sun.position.x
            dy = current_planet.position.y - current_sun.position.y
            theta_current = math.atan2(dy, dx) 
            
            delta_theta = theta_current - theta_prev

            if delta_theta < -math.pi:
                delta_theta += (2 * math.pi)
            elif delta_theta > math.pi:
                delta_theta -= (2 * math.pi)
                
            total_angle += delta_theta
            theta_prev = theta_current
            
        days = step * dt / 86400  # convert seconds to days
        print(f"{current_planet.name} orbital period: {days:.2f} days")

measure_all_periods_python()