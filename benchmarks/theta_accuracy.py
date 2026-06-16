# benchmarks/theta_accuracy.py
import numpy as np
from src.core.spawn import generate_random_bodies
from src.core.integrator import update_forces_bh, update_forces_np
from src.utils.vector import Vector2D
import matplotlib.pyplot as plt



def total_force_magnitude(bodies):
    """Return list of force magnitudes on each body."""
    return [body.acceleration.magnitude() for body in bodies]


def run_theta_test(theta_values, n_bodies=50):
    bodies_ref = generate_random_bodies(n_bodies)

    # Ground truth: NumPy exact forces
    update_forces_np(bodies_ref)
    ref_forces = total_force_magnitude(bodies_ref)

    results = {}
    for theta in theta_values:
        # Reset bodies to same initial state
        bodies_test = generate_random_bodies(n_bodies)
        # Copy positions from reference bodies so comparison is fair
        for i, body in enumerate(bodies_test):
            body.position = bodies_ref[i].position
            body.mass = bodies_ref[i].mass

        update_forces_bh(bodies_test, theta=theta)
        bh_forces = total_force_magnitude(bodies_test)

        # Compute mean percentage error
        errors = [abs(bh - ref) / ref * 100
                  for bh, ref in zip(bh_forces, ref_forces) if ref > 0]
        results[theta] = sum(errors) / len(errors)

    return results




if __name__ == "__main__":
    theta_values = [0.1, 0.3, 0.5, 0.7, 1.0]
    results = run_theta_test(theta_values)

    print(f"{'Theta':<10} {'Mean Error %':<15}")
    print("-" * 25)
    for theta, error in results.items():
        print(f"{theta:<10} {error:<15.4f}")
        
fig, ax = plt.subplots()

ax.plot(list(results.keys()), list(results.values()), color="orange", marker="o")
ax.set_title("Theta Accuracy")
ax.set_xlabel("Theta")
ax.set_ylabel("Error Ratio")

plt.tight_layout()
plt.savefig("theta_accuracy.png")
