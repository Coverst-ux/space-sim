import json
from src.utils.vector import Vector2D
from src.core.body import Body
def config_loader(path: str = "configs/solar_system.json"):
    with open(path, "r") as file:
        data = json.load(file)
        bodies = []
        for body_data in data["bodies"]:
            position = Vector2D(body_data["position"][0], body_data["position"][1])
            velocity = Vector2D(body_data["velocity"][0], body_data["velocity"][1])
            
            bodies.append(Body(
                name=body_data["name"],
                mass=body_data["mass"],
                position=position,
                velocity=velocity,
                color=tuple(body_data["color"]),
                radius=body_data["radius"]
            ))
            
        return bodies