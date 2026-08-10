import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import space_sim_cpp
from src.core.spawn import generate_random_bodies, generate_random_bodies_python
from src.core.integrator import leapfrog_step  # NumPy path — confirm this is your update_forces_np-based one, not the softened pairwise version

def benchmark_numpy(n, steps, dt=3600.0):
    bodies = generate_random_bodies_python(n)
    start = time.perf_counter()
    for _ in range(steps):
        leapfrog_step(bodies, dt)
    elapsed = time.perf_counter() - start
    return elapsed

def benchmark_cpp(n, steps, dt=3600.0):
    bodies_result = generate_random_bodies(n)
    bodies = bodies_result[0]
    start = time.perf_counter()
    for _ in range(steps):
        space_sim_cpp.leapfrog_step(bodies, dt)
    elapsed = time.perf_counter() - start
    return elapsed

if __name__ == "__main__":
    for n in [750, 1300]:
        numpy_time = benchmark_numpy(n, steps=50)
        cpp_time = benchmark_cpp(n, steps=50)
        speedup = numpy_time / cpp_time
        print(f"N={n}: NumPy={numpy_time:.3f}s, C++={cpp_time:.3f}s, speedup={speedup:.1f}x")