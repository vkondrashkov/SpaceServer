import socket as Socket
import json as JSON
from threading import Thread
from src.entity import Entity
from src.entityFactory import EntityFactory

HOST = input('Enter host: ')
PORT = input('Enter port: ')

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
uuid = client_socket.recv(BUFFER_SIZE).decode("utf8")

def receive():
    """Handles receiving of messages."""
    global THREAD_IS_RUNNING
    while THREAD_IS_RUNNING:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            if not msg:
                raise OSError
            json = JSON.loads(msg)
            # print(msg)
        except OSError:  # Possibly client has left.
            client_socket.close()
            break

if __name__ == "__main__":
    print("UUID: " + uuid)
    receive_thread = Thread(target=receive)
    receive_thread.start()

    while True:
        try:
            key = input()
            if key == "exit":
                raise KeyboardInterrupt
            request = {}
            request["event"] = key
            request["id"] = uuid
            json = JSON.dumps(request)
            client_socket.send(json.encode("utf8"))
            print(json)
        except KeyboardInterrupt:
            request = {}
            request["event"] = "exit"
            request["id"] = uuid
            json = JSON.dumps(request)
            client_socket.send(json.encode("utf8"))
            THREAD_IS_RUNNING = False
            receive_thread.join()
            client_socket.close()
            exit()