# profile_physics.py
import cProfile
from src.core.spawn import generate_random_bodies
from src.core.integrator import leapfrog_step

def run_heavy_simulation():
    # 1. Setup a heavy load (e.g., 300 bodies)
    bodies = generate_random_bodies(300)
    dt = 3600.0
    
    # 2. Run the physics loop for 50 steps to collect plenty of data
    for _ in range(50):
        leapfrog_step(bodies, dt)

if __name__ == "__main__":
    print("Running profile on 300 bodies...")
    
    # Run the profiler and sort results by total time spent inside functions
    cProfile.run("run_heavy_simulation()", sort="tottime")