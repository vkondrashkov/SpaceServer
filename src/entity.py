class Entity:
    def __init__(self, 
                id, 
                entityType, 
                health, 
                x, 
                y,
                width,
                height,
                damage):
        self.__id = id
        self.__entityType = entityType
        self.__health = health
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__damage = damage
    
    def hurt(self, damage):
        self.__health -= damage

    def toJSON(self):
        json = {}
        json["id"] = self.__id
        json["entityType"] = self.__entityType
        json["health"] = self.__health
        json["x"] = self.__x
        json["y"] = self.__y
        json["width"] = self.__width
        json["height"] = self.__height
        json["damage"] = self.__damage
        return json