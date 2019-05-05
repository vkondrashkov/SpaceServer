import socket as Socket
from threading import Thread

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
client_socket.settimeout(0.1)

def receive():
    """Handles receiving of messages."""
    global THREAD_IS_RUNNING
    while THREAD_IS_RUNNING:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            print(msg)
        except OSError:  # Possibly client has left the chat.
            client_socket.close()
            break

if __name__ == "__main__":
    #global THREAD_IS_RUNNING
    receive_thread = Thread(target=receive)
    receive_thread.start()

    while True:
        try:
            key = input()
            if key == "exit":
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            THREAD_IS_RUNNING = False
            exit()