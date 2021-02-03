import socket
import threading
import random
import Shared as Shared

MAX_CLIENTS = 5

sockets_client = []
addresses_client = []
sockets_closed = []


def Update_Clients(new_client, new_address):
    new_client = Shared.Client(new_client, new_address)
    for client in sockets_client:
        try:
            Shared.send_address_list_tcp(client.socket, [new_address])
        except socket.timeout:
            sockets_closed.append(client)
            sockets_client.remove(client)
            addresses_client.remove(client.address)

    Shared.send_address_list_tcp(new_client.socket, addresses_client)

    sockets_client.append(new_client)
    addresses_client.append(new_address)


if __name__ == '__main__':
    # do stuff

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_socket.bind((Shared.ADDRESS_MASK, Shared.PORT))
    tcp_socket.listen(MAX_CLIENTS)

    print('Starting server')

    while True:
        client_socket, address = tcp_socket.accept()
        Shared.log_new_client(address)
        Update_Clients(client_socket, address)
