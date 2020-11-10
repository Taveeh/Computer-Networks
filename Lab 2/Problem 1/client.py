import socket
import sys

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


def getStringFromCommand():
    arr = sys.argv[1:]
    string = ""
    for i in arr:
        string += i + " "
    string = string[:-1]
    send(string)


getStringFromCommand()
size = int(client.recv(SIZE))
print(client.recv(size).decode(FORMAT))
