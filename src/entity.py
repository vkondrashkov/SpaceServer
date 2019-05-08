class Entity:
    @property
    def id(self):
        return self.__id

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

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
        self.x = x
        self.y = y
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
        self.x += deltaX * self.__velocity
        self.y += deltaY * self.__velocity

    # Update method which called every tick by server
    def update(self):
        if self.__deltaXConstant != 0 or self.__deltaYConstant != 0:
            self.move(self.__deltaXConstant, self.__deltaYConstant)

    def toJSON(self):
        json = {}
        json["id"] = self.__id
        json["entityType"] = self.__entityType
        json["health"] = self.__health
        json["x"] = self.x
        json["y"] = self.y
        json["width"] = self.width
        json["height"] = self.height
        json["damage"] = self.__damage
        json["velocity"] = self.__velocity
        return json
    
    def collidesWith(self, entity):
        return (self.x + self.width + self.__velocity) >= entity.x and \
            self.x - self.__velocity <= entity.x + entity.width and \
            self.y + self.height + self.__velocity >= entity.y and \
            self.y - self.__velocity <= entity.y + entity.height
        # return ((self.y - self.__velocity) >= (entity.y + entity.height) or \
        #     (self.y + self.height + self.__velocity) <= entity.y) and \
        #     ((self.x - self.__velocity) >= (entity.x + entity.width) or \
        #     (self.x + self.width + self.__velocity) <= entity.x)


#             if (r1x + r1w >= r2x &&    // r1 right edge past r2 left
#       r1x <= r2x + r2w &&    // r1 left edge past r2 right
#       r1y + r1h >= r2y &&    // r1 top edge past r2 bottom
#       r1y <= r2y + r2h) {    // r1 bottom edge past r2 top
#         return true;
#   }