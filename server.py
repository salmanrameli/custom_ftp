import socket
import threading
import select
import sys

server_address = ('127.0.0.1', 51000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for client in read_ready:
            if client == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

            else:
                data = client.recv(1024)
                print data.strip()

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
