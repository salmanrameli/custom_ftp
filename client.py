import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 51000))
recv_message = client_socket.recv(1024).strip()
print recv_message

try:
    while True:
            message = raw_input('> ')
            if message:
                if message == 'QUIT':
                    client_socket.send(message)
                    recv_message = client_socket.recv(1024)
                    print recv_message
                    break

                if 'STOR' in message:
                    client_socket.send(message)
                    filename = message.split()
                    data_file = open(filename[1], 'rb')

                    send_data = data_file.read(1024)
                    while send_data:
                        client_socket.send(send_data)
                        send_data = data_file.read(1024)

                    if not send_data:
                        client_socket.send(send_data)
                        message = client_socket.recv(1024)
                        print message.strip()
                        data_file.close()

                else:
                    client_socket.send(message)
                    recv_message = client_socket.recv(1024)
                    print recv_message.strip()

                    # while(recv_message):
                    #     if '226' in recv_message:
                    #         print recv_message.strip()
                    #         break
                    #     print recv_message.strip()
                    #     recv_message = client_socket.recv(1024)

except KeyboardInterrupt:
    client_socket.close()
