from random import randint
from src.entity import Entity

class EntityFactory:
    def makeEntityFromJSON(self, json):
        id = json["id"]
        entityType = json["entityType"]
        health = json["health"]
        x = json["x"]
        y = json["y"]
        width = json["width"]
        height = json["height"]
        damage = json["damage"]
        velocity = json["velocity"]
        shootDelay = json["shootDelay"]

        return Entity(id, entityType, health, x, y, width, height, damage, velocity, shootDelay)

    def makePlayerWithUUID(self, uuid):
        id = uuid
        entityType = "player"
        health = 10
        x = randint(0, 780)
        y = randint(320, 580)
        width = 75
        height = 55
        damage = 3
        velocity = 6
        shootDelay = 10

        return Entity(id, entityType, health, x, y, width, height, damage, velocity, shootDelay)
    
    def makeEnemyWithUUID(self, uuid):
        id = uuid
        entityType = "enemy"
        health = 10
        x = randint(0, 860)
        y = 0
        width = 75
        height = 60
        damage = 1
        velocity = 1
        shootDelay = 90

        return Entity(id, entityType, health, x, y, width, height, damage, velocity, shootDelay, deltaYConstant=1)

    def makeBulletWithUUID(self, uuid, x, y, damage, deltaYConstant, ownerUUID):
        id = uuid
        entityType = "bullet"
        health = 1
        width = 5
        height = 15
        velocity = 12
        
        return Entity(id, entityType, health, x, y, width, height, damage, velocity, 0, deltaYConstant=deltaYConstant, ownerUUID=ownerUUID)