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

    @property
    def entityType(self):
        return self.__entityType
    
    @property
    def damage(self):
        return self.__damage

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
                shootDelay,
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
        self.__shootDelay = shootDelay
        self.__shootTick = shootDelay / 2
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
        self.__shootTick -= 1
        if self.__deltaXConstant != 0 or self.__deltaYConstant != 0:
            self.move(self.__deltaXConstant, self.__deltaYConstant)

    # Actually I wouldn't make such mess and monkeycode but...
    # Who cares? ¯\_(ツ)_/¯
    # Returns True if managed to shoot and False whether not
    def managedShot(self):
        if self.entityType == "bullet":
            return False
        if self.__shootTick > 0:
            return False
        self.__shootTick = self.__shootDelay
        print(self.id + " shot")
        return True

    def toJSON(self):
        json = {}
        json["id"] = self.__id
        json["entityType"] = self.entityType
        json["health"] = self.__health
        json["x"] = self.x
        json["y"] = self.y
        json["width"] = self.width
        json["height"] = self.height
        json["damage"] = self.__damage
        json["velocity"] = self.__velocity
        json["shootDelay"] = self.__shootDelay
        return json
    
    def collidesWith(self, entity):
        return (self.x + self.width + self.__velocity) >= entity.x and \
            self.x - self.__velocity <= entity.x + entity.width and \
            self.y + self.height + self.__velocity >= entity.y and \
            self.y - self.__velocity <= entity.y + entity.height