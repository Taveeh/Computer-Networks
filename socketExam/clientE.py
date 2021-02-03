import socket
import threading
import Shared

addresses_client = []


def Tcp_Listener_Thread(socket_tcp):
    while True:
        Updated_Addresses = Shared.receive_address_list_tcp(socket_tcp)
        # Update(Updated_Addresses)


def Udp_Listener_Thread(receiver_socket, bound_address):
    while True:
        Message = Shared.receive_message(receiver_socket, bound_address)
        print('Received: %s' % Message)


def Update(Updated_Addresses):
    Address = Updated_Addresses[0]

    try:
        addresses_client.index(Address)
        print('Disconnected client: %s:%s' % (Address[0], Address[1]))
        addresses_client.remove(Address)

    except ValueError:
        print('New client: %s:%s' % (Address[0], Address[1]))
        addresses_client.append(Address)


def SendToAll(udp_socket, Message):
    for address in addresses_client:
        udp_socket.sendto(Message.encode(Shared.ENCODING), ('<broadcast>', Shared.UDP_PORT))

if __name__ == '__main__':

    tcp_socket = socket.create_connection((Shared.LOCALHOST, Shared.PORT))

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    addresses_client = Shared.receive_address_list_tcp(tcp_socket)

    t = threading.Thread(target=Tcp_Listener_Thread, args=(tcp_socket,))
    t.start()

    for address in addresses_client:
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener_socket.bind((address[0], Shared.UDP_PORT))
        listener = threading.Thread(target=Udp_Listener_Thread, args=(listener_socket, (address[0], Shared.UDP_PORT)))
        listener.start()

    while True:
        line = input("Input:")
        print('Sending: %s' % line)
        SendToAll(udp_socket, line)
