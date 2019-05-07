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
                _entity = self.__entityFactory.makeUUID(_uuid)
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
            request = JSON.loads(msg)
            if request["event"] != "exit" and msg is not "":
                _entity = self.__entities[request["id"]]
                
                if request["event"] == "move_up":
                    _entity.move(0, 1)
                if request["event"] == "move_down":
                    _entity.move(0, -1)
                if request["event"] == "move_left":
                    _entity.move(-1, 0)
                if request["event"] == "move_right":
                    _entity.move(1, 0)

                self.__entities[request["id"]] = _entity

                self.__updateGameLoop()
                print(msg)
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
        print("Game is " + str(self.gameIsRunning))

    def __gameLoop(self):
        while self.gameIsRunning:
            time.sleep(0.1)
            for _, entity in self.__entities.items():
                entity.update()
            self.__updateClients()
        
    
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