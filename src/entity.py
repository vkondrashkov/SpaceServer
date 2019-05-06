class Entity:
    def __init__(self, id, entityType, health, x, y):
        self.__id = id
        self.__entityType = entityType
        self.health = health
        self.__x = x
        self.__y = y
    
    def toJSON(self):
        json = {}
        json["id"] = self.__id
        json["entityType"] = self.__entityType
        json["health"] = self.health
        position = {}
        position["x"] = self.__x
        position["y"] = self.__y
        json["position"] = position
        return json