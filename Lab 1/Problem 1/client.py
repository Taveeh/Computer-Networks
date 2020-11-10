import socket

SIZE = 16
FORMAT = 'utf-8'
EXIT_MESSAGE = '!EXIT'
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


def sendArray(array):
    send(str(len(array)))
    for i in array:
        send(str(i))


arr = [1, 2, 3, 4]
sendArray(arr)
input()

print(client.recv(1024).decode(FORMAT))
