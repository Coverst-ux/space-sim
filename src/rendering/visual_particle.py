# src/rendering/visual_particle.py
import math
import random

PULL_STRENGTH = 1e14
SOFTENING = 1e6

class VisualParticle:
    def __init__(self, position, velocity, color, lifetime, particle_type):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.age = 0
        self.lifetime = lifetime
        self.particle_type = particle_type

    def update(self, dt, attractors):
        pull_x, pull_y, pull_z = 0, 0, 0

        for ax, ay, az in attractors:
            dx = ax - self.position[0]
            dy = ay - self.position[1]
            dz = az - self.position[2]

            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            strength = PULL_STRENGTH / (dist + SOFTENING)

            norm_x = dx / dist
            norm_y = dy / dist
            norm_z = dz / dist

            pull_x += norm_x * strength
            pull_y += norm_y * strength
            pull_z += norm_z * strength

        vx, vy, vz = self.velocity
        vx += pull_x * dt
        vy += pull_y * dt
        vz += pull_z * dt
        self.velocity = (vx, vy, vz)

        x, y, z = self.position
        x += vx * dt
        y += vy * dt
        z += vz * dt
        self.position = (x, y, z)

        self.age += 1

    def is_alive(self):
        return self.age < self.lifetime
    


def spawn_particle(star_position, star_velocity, star_radius, color, lifetime):
    spawn_radius = star_radius * random.uniform(1.5, 15.0)  # you widened this earlier

    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)

    offset_x = spawn_radius * math.sin(phi) * math.cos(theta)
    offset_y = spawn_radius * math.sin(phi) * math.sin(theta)
    offset_z = spawn_radius * math.cos(phi)

    position = (
        star_position[0] + offset_x,
        star_position[1] + offset_y,
        star_position[2] + offset_z
    )

    up_x, up_y, up_z = 0, 0, 1
    tangent_x = offset_y * up_z - offset_z * up_y
    tangent_y = offset_z * up_x - offset_x * up_z
    tangent_z = offset_x * up_y - offset_y * up_x

    tangent_mag = math.sqrt(tangent_x**2 + tangent_y**2 + tangent_z**2)
    tangent_x /= tangent_mag
    tangent_y /= tangent_mag
    tangent_z /= tangent_mag

    TANGENT_SPEED = 1e4

    velocity = (
        star_velocity[0] + tangent_x * TANGENT_SPEED,
        star_velocity[1] + tangent_y * TANGENT_SPEED,
        star_velocity[2] + tangent_z * TANGENT_SPEED
    )

    return VisualParticle(position, velocity, color, lifetime, particle_type="background")




