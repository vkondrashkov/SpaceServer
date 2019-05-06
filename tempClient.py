import socket as Socket
import json as JSON
from threading import Thread
from src.entity import Entity
from src.entityFactory import EntityFactory

HOST = input('Enter host: ')
PORT = input('Enter port: ')

player = Entity(1, "player", 100, 50, 50)

if not HOST:
    HOST = "localhost"

if not PORT:
    PORT = 33000  # Default value.
else:
    PORT = int(PORT)

BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

THREAD_IS_RUNNING = True

client_socket = Socket.socket()
client_socket.connect(ADDRESS)

def receive():
    """Handles receiving of messages."""
    global THREAD_IS_RUNNING
    global player
    while THREAD_IS_RUNNING:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            if not msg:
                raise OSError
            json = JSON.loads(msg)
            entityFactory = EntityFactory()
            entity = entityFactory.make(json)
            player = entity
            print(msg)
        except OSError:  # Possibly client has left the chat.
            client_socket.close()
            break

if __name__ == "__main__":
    receive_thread = Thread(target=receive)
    receive_thread.start()

    while True:
        try:
            key = input()
            if key == "exit":
                raise KeyboardInterrupt
            json = JSON.dumps(player.toJSON())
            client_socket.send(json.encode("utf8"))
            print(json)
        except KeyboardInterrupt:
            client_socket.send(bytes("{exit}", "utf8"))
            THREAD_IS_RUNNING = False
            receive_thread.join()
            exit()