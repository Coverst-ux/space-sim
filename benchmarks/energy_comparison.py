import math
from src.core.integrator import leapfrog_step, euler_step
from src.io.loader import config_loader
import matplotlib.pyplot as plt
from src.utils.constants import G

bodies_euler = config_loader()
bodies_leapfrog = config_loader()
dt = 86400
steps = 365 * 20  # 20 years

def total_energy(bodies):
    earth = bodies[1]   # index 1 is Earth
    sun = bodies[0]     # index 0 is Sun
    
    # kinetic energy
    v_sq = earth.velocity.x**2 + earth.velocity.y**2
    KE = 0.5 * earth.mass * v_sq
    
    # potential energy
    dx = earth.position.x - sun.position.x
    dy = earth.position.y - sun.position.y
    r = math.sqrt(dx**2 + dy**2)
    PE = -G * sun.mass * earth.mass / r
    
    return KE + PE

# --- Keep all your original imports and functions exactly the same ---

bodies_euler = config_loader()
bodies_leapfrog = config_loader()

# --- THE SIMPLE FIXES ---
dt = 86400             # 1 day in seconds
steps = 365 * 20       # 20 years total

# Capture the starting energy of the system
initial_euler_energy = total_energy(bodies_euler)
initial_leapfrog_energy = total_energy(bodies_leapfrog)

energy_euler = []
for step in range(steps):
    euler_step(bodies_euler, dt)
    # Track the relative percentage change: (Current - Initial) / Initial
    relative_error = (total_energy(bodies_euler) - initial_euler_energy) / abs(initial_euler_energy)
    energy_euler.append(relative_error)
    
energy_leapfrog = []
for step in range(steps):
    leapfrog_step(bodies_leapfrog, dt)
    # Track the relative percentage change
    relative_error = (total_energy(bodies_leapfrog) - initial_leapfrog_energy) / abs(initial_leapfrog_energy)
    energy_leapfrog.append(relative_error)

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(energy_euler, color="blue")
ax1.set_title("Euler Integration (Relative Energy Error)")
ax1.set_ylabel("Error Ratio")

ax2.plot(energy_leapfrog, color="orange")
ax2.set_title("Leapfrog Integration (Relative Energy Error)")
ax2.set_ylabel("Error Ratio")

plt.tight_layout()
plt.savefig("benchmarks/euler_vs_leapfrog_energy.png")