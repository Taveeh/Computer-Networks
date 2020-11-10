import socket
import select
FORMAT = 'ascii'


if __name__ == '__main__':
    TEACHER_PORT = 1234
    sock = socket.create_server(("0.0.0.0", TEACHER_PORT), family=socket.AF_INET, reuse_port=True)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    array_for_select = [sock]

    while True:
        readable, writable, error = select.select(array_for_select, [], [])
        for file_descriptor in readable:
            if file_descriptor == sock:
                student_socket, addr = sock.accept()
                array_for_select.append(student_socket)
            else:
                msg = file_descriptor.recv(1024)
                msg = msg.decode(FORMAT)
                print(f"Teacher received {msg}")
                file_descriptor.send("answer".encode(FORMAT))

