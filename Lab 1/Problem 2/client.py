import socket


SIZE = 16
FORMAT = "utf-8"
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(message):
    message = message.encode(FORMAT)
    size = len(message)
    stringSize = str(size).encode(FORMAT)
    stringSize += b' ' * (SIZE - len(stringSize))
    client.send(stringSize)
    client.send(message)


send("Ana are mere")
print(client.recv(1024).decode(FORMAT))
