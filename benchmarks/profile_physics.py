# profile_physics.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cProfile
from src.core.spawn import generate_random_bodies_python
from src.core.integrator import leapfrog_step
num_bodies = 500
dt = 3600.0

def run_heavy_simulation():
    bodies = generate_random_bodies_python(num_bodies)
    
    for _ in range(50):
        leapfrog_step(bodies, dt)

if __name__ == "__main__":
    print(f"Running profile on {num_bodies}  bodies...")
    # Run the profiler and sort results by total time spent inside functions
    cProfile.run("run_heavy_simulation()", sort="tottime")