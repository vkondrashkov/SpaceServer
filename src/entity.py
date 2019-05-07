class Entity:
    def __init__(self, 
                id, 
                entityType, 
                health, 
                x, 
                y,
                width,
                height,
                damage,
                velocity,
                deltaXConstant=0,
                deltaYConstant=0):
        self.__id = id
        self.__entityType = entityType
        self.__health = health
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__damage = damage
        self.__velocity = velocity
        self.__deltaXConstant = deltaXConstant
        self.__deltaYConstant = deltaYConstant
    
    def hurt(self, damage):
        self.__health -= damage

    # DeltaX and DeltaY should be equaled 1 or -1
    # Sign means direction for each axis
    def move(self, deltaX, deltaY):
        self.__x += deltaX * self.__velocity
        self.__y += deltaY * self.__velocity

    # Update method which called every tick by server
    def update(self):
        if self.__deltaXConstant != 0 or self.__deltaYConstant != 0:
            self.move(self.__deltaXConstant, self.__deltaYConstant)

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
        json["velocity"] = self.__velocity
        return json