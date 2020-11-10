import socket
import threading

SIZE = 16
FORMAT = 'utf-8'
EXIT_MESSAGE = '!EXIT'
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(message, client):
    message = message.encode(FORMAT)
    size = len(message)
    stringSize = str(size).encode(FORMAT)
    stringSize += b' ' * (SIZE - len(stringSize))
    client.send(stringSize)
    client.send(message)


def sendArray(array, client):
    send(str(len(array)), client)
    for i in array:
        send(str(i), client)


def worker(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    msg_length = conn.recv(SIZE).decode(FORMAT)
    nr = 0
    elements1 = []
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        nr = int(msg)
    for i in range(nr):
        msg_length = conn.recv(SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            elements1.append(int(msg))
    msg_length = conn.recv(SIZE).decode(FORMAT)
    nr = 0
    elements2 = []
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        nr = int(msg)
    for i in range(nr):
        msg_length = conn.recv(SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            elements2.append(int(msg))
    elements = []
    print(elements1, elements2)
    for x in elements1:
        if x in elements2:
            elements.append(x)
    sendArray(elements, conn)


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=worker, args=(conn, addr))
        thread.start()

start()