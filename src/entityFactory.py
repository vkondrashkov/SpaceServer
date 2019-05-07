from random import randint
from src.entity import Entity

class EntityFactory:
    def makeJSON(self, json):
        id = json["id"]
        entityType = json["entityType"]
        health = json["health"]
        x = json["x"]
        y = json["y"]
        width = json["width"]
        height = json["height"]
        damage = json["damage"]
        velocity = json["velocity"]

        return Entity(id, entityType, health, x, y, width, height, damage, velocity)

    def makeUUID(self, uuid):
        id = uuid
        entityType = "player"
        health = 10
        x = randint(0, 860)
        y = randint(320, 640)
        width = 75
        height = 55
        damage = 3
        velocity = 6

        return Entity(id, entityType, health, x, y, width, height, damage, velocity)