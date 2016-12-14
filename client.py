import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 51000))

try:
    while True:
        message = raw_input('> ')
        if message == 'exit':
            client_socket.send(message)
            break
        client_socket.send(message)

except KeyboardInterrupt:
    client_socket.close()
