from src.entity import Entity

class EntityFactory:
    def make(self, json):
        id = json["id"]
        entityType = json["entityType"]
        health = json["health"]
        x = json["position"]["x"]
        y = json["position"]["y"]

        return Entity(id, entityType, health, x, y)