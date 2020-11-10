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

arr2 = [2, 3, 5, 6]
sendArray(arr2)


def receiveArray():
    msg_length = client.recv(SIZE).decode(FORMAT)
    nr = 0
    elements1 = []
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        nr = int(msg)
    for i in range(nr):
        msg_length = client.recv(SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            elements1.append(int(msg))
    return elements1


print(receiveArray())