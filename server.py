import socket as Socket
import json as JSON
import uuid
import time
from threading import Thread
from src.config import config
from src.entity import Entity
from src.entityFactory import EntityFactory

class Server:
    def __init__(self):
        self.isRunning = False
        self.gameIsRunning = False
        self.__entities = {}
        self.clients = []
        self.__loadConfig()
        self.__entityFactory = EntityFactory()
        self.__spawnEnemyTick = 30
    
    def start(self):
        self.isRunning = True
        self.__socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
        self.__socket.bind((self.__hostname, self.__port))
        self.__socket.listen(2) # Temp value # what the duck it doing?
        self.__socket.settimeout(0.1)
        print("Server has started on " + self.__hostname + ":" + str(self.__port))

        self.__acceptThread = Thread(target=self.__onConnection)
        self.__acceptThread.start()
    
    def stop(self):
        for client in self.clients:
            client.close()
        self.__socket.close()
        self.isRunning = False
        self.__acceptThread.join()
        self.__recieveThread.join()
        print("Server has been stopped.")

    def __loadConfig(self):
        self.__hostname = config["hostname"]
        self.__port = config["port"]
        self.__bufferSize = config["bufferSize"]

    # Events
    def __onConnection(self):
        print("Waiting for connections...")
        while self.isRunning:
            try:
                client, address = self.__socket.accept()
                print("%s:%s has connected." % address)
                self.clients.append(client)
                _uuid = uuid.uuid4().hex
                _entity = self.__entityFactory.makePlayerWithUUID(_uuid)
                self.__entities[_uuid] = _entity
                client.send(_uuid.encode("utf8"))

                self.__recieveThread = Thread(target=self.__onReceive, args=(client,))
                self.__recieveThread.start()

                self.__updateGameLoop()
            except Socket.timeout:
                pass
        
    def __onReceive(self, client):
        while self.isRunning:
            msg = client.recv(self.__bufferSize).decode("utf8")
            try:
                request = JSON.loads(msg)
            except:
                continue
            if request["event"] != "exit" and msg is not "":
                _entity = self.__entities[request["id"]]
                print(msg)
                _originX, _originY = _entity.x, _entity.y
                
                if request["event"] == "move_up":
                    _entity.move(0, -1)
                if request["event"] == "move_down":
                    _entity.move(0, 1)
                if request["event"] == "move_left":
                    _entity.move(-1, 0)
                if request["event"] == "move_right":
                    _entity.move(1, 0)
                if request["event"] == "shoot":
                    if _entity.managedShot():
                        _bulletUuid = uuid.uuid4().hex
                        _bullet = self.__entityFactory.makeBulletWithUUID(_bulletUuid, _entity.x + _entity.width / 2, _entity.y, _entity.damage, deltaYConstant=-1)
                        self.__entities[_bulletUuid] = _bullet

                for collidingEntity in [entity for _, entity in self.__entities.items() if entity.id != request["id"]]:
                    if _entity.collidesWith(collidingEntity):
                        _entity.x, _entity.y = _originX, _originY

                self.__entities[request["id"]] = _entity

                self.__updateGameLoop()
            else:
                print(request["id"] + " has left")
                self.clients.remove(client)
                del self.__entities[request["id"]]
                client.close()
                self.__updateGameLoop()
                break

    # Core
    def __updateGameLoop(self):
        if not self.gameIsRunning and len(self.clients) != 0:
            self.gameIsRunning = True
            self.__gameThread = Thread(target=self.__gameLoop)
            self.__gameThread.start()
        if self.gameIsRunning and len(self.clients) == 0:
            self.gameIsRunning = False
            self.__gameThread.join()

    def __gameLoop(self):
        while self.gameIsRunning:
            # Note: couldn't send 60 requests per second due to client
            # can't parse JSON, because it receives several JSONs simultaneously
            # so serializer can't parse wrong JSON and client caught exception
            # That's why clients can't see real-time changes.
            #
            # 23 requests per second seems more convinient and stable.
            # Should be changed ASAP
            time.sleep(1 / 23)
            self.__cycleSpawnEnemy()
            entitiesCopy = self.__entities.copy()
            for _uuid, entity in entitiesCopy.items():
                entity.update()
                if entity.entityType == "enemy" and entity.managedShot():
                    _bulletUuid = uuid.uuid4().hex
                    _bullet = self.__entityFactory.makeBulletWithUUID(_bulletUuid, entity.x + entity.width / 2, entity.y, entity.damage, deltaYConstant=1)
                    self.__entities[_bulletUuid] = _bullet
                if entity.y >= 640:
                    del self.__entities[_uuid]
                    print("Deleted " + _uuid + " (" + entity.entityType + ")")
            self.__updateClients()

    def __cycleSpawnEnemy(self):
        if self.__spawnEnemyTick:
            self.__spawnEnemyTick -= 1
        else:
            # Generates random horizontal position
            # considering it's width to avoid generating
            # object beyond Screen borders.
            _uuid = uuid.uuid4().hex
            _entity = self.__entityFactory.makeEnemyWithUUID(_uuid)
            self.__entities[_uuid] = _entity
            print("Spawned " + _uuid + " (" + _entity.entityType + ")")
            self.__spawnEnemyTick = 240
        
    
    def entitiesListJSON(self):
        '''Returns JSON string that contains all the entities in game world'''
        entityList = []
        for _, entity in self.__entities.items():
            entityList.append(entity.toJSON())
        return JSON.dumps(entityList)
    
    def __updateClients(self):
        for client in self.clients:
            client.send(self.entitiesListJSON().encode("utf8"))

if __name__ == "__main__":
    server = Server()
    server.start()
    while True:
        try:
            key = input()
            if key == "exit":
                raise KeyboardInterrupt
            if key == "clients":
                for client in server.clients:
                    print(client)
            if key == "entities":
                print(server.entitiesListJSON())
        except KeyboardInterrupt:
            server.stop()
            exit()