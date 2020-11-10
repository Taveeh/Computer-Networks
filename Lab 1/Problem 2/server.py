import socket
import threading

SIZE = 16
FORMAT = 'utf-8'
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def worker(conn, addr):
    cnt = 0
    size = conn.recv(SIZE).decode(FORMAT)
    if size:
        size = int(size)
    else:
        conn.close()
        exit(-1)
    string = conn.recv(size).decode(FORMAT)
    for i in string:
        if i == ' ':
            cnt += 1
    conn.send(str(cnt).encode(FORMAT))
    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=worker, args=(conn, addr))
        thread.start()


start()

