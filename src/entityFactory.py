from src.entity import Entity

class EntityFactory:
    def make(self, json):
        id = json["id"]
        entityType = json["entityType"]
        health = json["health"]
        x = json["x"]
        y = json["y"]
        width = json["width"]
        height = json["height"]
        damage = json["damage"]

        return Entity(id, entityType, health, x, y, width, height, damage)
