import socket, threading

SIZE = 16
FORMAT = 'utf-8'
EXIT_MESSAGE = '!EXIT'
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def worker(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    sum_elements = 0
    msg_length = conn.recv(SIZE).decode(FORMAT)
    nr = 0
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        nr = int(msg)
    for i in range(nr):
        msg_length = conn.recv(SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            sum_elements += int(msg)
            print(f"[{addr}] The sum is now {sum_elements}")
    conn.send(str(sum_elements).encode(FORMAT))
    msg_length = conn.recv(SIZE).decode(FORMAT)
    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=worker, args=(conn, addr))
        thread.start()


print("Starting server...")
start()
