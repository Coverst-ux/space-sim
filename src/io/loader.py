import json
import space_sim_cpp
from src.utils.vector import Vector3D
from src.core.body import Body
from src.rendering.render_body import RenderBody


def config_loader_python(path: str = "configs/solar_system.json"):
    with open(path, "r") as file:
        data = json.load(file)
        bodies = []

        for body_data in data["bodies"]:
            position = Vector3D(body_data["position"][0], body_data["position"][1], body_data["position"][2])   # same 3 indices as the C++ version
            velocity = Vector3D(body_data["velocity"][0], body_data["velocity"][1], body_data["velocity"][2])
            body = Body(
                name=body_data["name"],
                mass=body_data["mass"],
                position=position,
                velocity=velocity,
                radius=body_data["radius"],
                color=tuple(body_data["color"])
            )
            bodies.append(body)

        return bodies

def config_loader(path: str = "configs/solar_system.json"):
    with open(path, "r") as file:
        data = json.load(file)
        physics_bodies = space_sim_cpp.BodyVector()
        colors = []

        for body_data in data["bodies"]:
            position = space_sim_cpp.Vector3D(body_data["position"][0], body_data["position"][1], body_data["position"][2])
            velocity = space_sim_cpp.Vector3D(body_data["velocity"][0], body_data["velocity"][1], body_data["velocity"][2])
            cpp_body = space_sim_cpp.Body(
                body_data["name"], body_data["mass"], position, velocity, body_data["radius"]
            )
            physics_bodies.append(cpp_body)
            colors.append(tuple(body_data["color"]))

        render_bodies = [RenderBody(physics_bodies[i], color=colors[i]) for i in range(len(physics_bodies))]

        return physics_bodies, render_bodies
    
    
    