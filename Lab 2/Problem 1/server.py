import socket
import threading
import subprocess

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


def worker(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    msg_length = conn.recv(SIZE).decode(FORMAT)
    msg = ""
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    print(msg)
    msg = msg.split(' ')
    print(msg)
    out = subprocess.Popen(msg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    to_send = out.communicate()[0].decode(FORMAT)
    send(to_send, conn)
    print(to_send)
    conn.close()



def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=worker, args=(conn, addr))
        thread.start()


print("Starting server...")
start()
