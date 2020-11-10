import socket
import threading
import sys
import time
import random

FORMAT = 'ASCII'
TEACHER_PORT = 1234


def worker_leader(leader_socket, group):
    while True:
        leader_socket.sendto('leader'.encode(FORMAT), ('<broadcast>', group))
        time.sleep(5)


def handle_leader(group):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    t = threading.Thread(target=worker_leader, args=(sock, group))
    t.start()

    teacher = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teacher.connect(("localhost", TEACHER_PORT))

    while True:
        msg, addr = sock.recvfrom(1024)
        # msg = msg.decode(FORMAT)
        teacher.send(msg)
        answer = teacher.recv(1024).decode(FORMAT)
        print(answer)
        sock.sendto(f"{msg} -> {answer}".encode(FORMAT), ('<broadcast>', group))


def worker_student(student_socket):
    while True:
        msg, addr = student_socket.recvfrom(1024)
        msg = msg.decode(FORMAT)
        if msg != "leader":
            print(f"{msg} got from {addr}")


def handle_student(group):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", group))

    msg = None
    addr = None
    while msg != 'leader':
        msg, addr = sock.recvfrom(1024)
        msg = msg.decode(FORMAT)

    thread = threading.Thread(target=worker_student, args=(sock, ))
    thread.start()

    while True:
        if random.randint(1, 2) == 1:
            msg = "question"
            sock.sendto(msg.encode(FORMAT), addr)
        time.sleep(3)


if __name__ == '__main__':
    group_port = int(sys.argv[1])
    isLeader = int(sys.argv[2])
    if isLeader == 1:
        handle_leader(group_port)
    else:
        handle_student(group_port)



