PORT = 7000
LOCALHOST = 'localhost'
ENCODING = 'ASCII'

UDP_PORT = 7001

ADDRESS_MASK = '0.0.0.0'


class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address


def send_address_list_tcp(target_socket, address_list):

    address_list_string = ''

    for address in address_list:
        address_list_string += str(address[0]) + ':' + str(address[1]) + ','

    address_list_string = address_list_string.strip(',')

    print('Sending address list: %s' % address_list_string)

    target_socket.sendall(address_list_string.encode(ENCODING))
    target_socket.send(' '.encode(ENCODING))


def receive_address_list_tcp(target_socket):
    address_list_string = ''
    while True:
        character = target_socket.recv(1).decode(ENCODING)[0]
        if character == ' ':
            break
        else:
            address_list_string += character

    if len(address_list_string) == 0:
        return []

    address_list_unparsed = address_list_string.split(',')
    address_list = []

    for address in address_list_unparsed:
        ip = address.split(':')[0]
        port = int(address.split(':')[1])
        address_list.append((ip, port))

    print('Received address list: %s' % address_list)

    return address_list


def receive_message(udp_socket, bound_address):
    string = ''
    while True:
        character = udp_socket.recvfrom(1, (bound_address[0], UDP_PORT)).decode(ENCODING)[0]
        if character == ' ':
            break
        else:
            string += character

    return string


def log_new_client(new_address):
    print("New client address: %s" % new_address[0])
