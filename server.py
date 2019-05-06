import socket as Socket
import json as JSON
from threading import Thread
from src.config import config
from src.entity import Entity
from src.entityFactory import EntityFactory

class Server:
    def __init__(self):
        self.__addresses = {}
        self.clients = []
        self.__loadConfig()
    
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
        print("Server has been stopped.")

    def __loadConfig(self):
        self.__hostname = config["hostname"]
        self.__port = config["port"]
        self.__bufferSize = config["bufferSize"]

    def __onConnection(self):
        print("Waiting for connections...")
        while self.isRunning:
            try:
                client, address = self.__socket.accept()
                print("%s:%s has connected." % address)
                self.clients.append(client)
                self.__addresses[client] = address

                self.__recieveThread = Thread(target=self.__onReceive, args=(client,))
                self.__recieveThread.start()
            except Socket.timeout:
                pass
        
    def __onReceive(self, client):
        #client.send(b"Successfully connected!")
        while self.isRunning:
            msg = client.recv(self.__bufferSize).decode("utf8")
            _address = self.__addresses[client][0] + ":" + str(self.__addresses[client][1])
            if msg != "{exit}" and msg is not "":
                _factory = EntityFactory()
                json = JSON.loads(msg)
                _entity = _factory.make(json)
                _entity.hurt(5)
                _logMessage = _address + " sent: " + msg
                for client in self.clients:
                    json = _entity.toJSON()
                    client.send(JSON.dumps(json).encode("utf8"))
                    # client.send(_logMessage.encode("utf8"))
                print(_logMessage)
            else:
                print(_address + " has left")
                self.clients.remove(client)
                client.close()
                break


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
        except KeyboardInterrupt:
            server.stop()
            exit()