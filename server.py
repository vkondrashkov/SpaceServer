import socket as Socket
from threading import Thread
from src.config import config

class Server:
    def __init__(self):
        self.__addresses = {}
        self.clients = []
        self.__loadConfig()
    
    def start(self):
        self.isRunning = True
        self.__socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
        self.__socket.bind((self.__hostname, self.__port))
        self.__socket.listen(5) # Temp value
        self.__socket.settimeout(0.1)
        print("Server has been started on " + self.__hostname + ":" + str(self.__port))

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

    def __onConnection(self):
        print("Waiting for connections...")
        while self.isRunning:
            try:
                client, address = self.__socket.accept()
                print("%s:%s has connected." % address)
                client.send(b"Successfully connected!") # temp message
                self.clients.append(client)
                self.__addresses[client] = address
            except Socket.timeout:
                pass
            # Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    server = Server()
    server.start()
    while True:
        try:
            key = input()
            for client in server.clients:
                print(client)
            if key == "exit":
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            server.stop()
            exit()