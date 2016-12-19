import socket
import os

buff = 1024
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

            if 'LIST' in message:
                client_socket.send(message)
                recv_message = client_socket.recv(buff)
                while (recv_message):
                    if '226' in recv_message:
                        print recv_message.strip()
                        break
                    print recv_message.strip()
                    recv_message = client_socket.recv(buff)

            elif 'STOR' in message:
                filename = message.split()
                st = os.stat(filename[1])
                filesize = str(st.st_size)
                client_socket.send(message + " " + filesize)
                data_file = open(filename[1], 'rb')

                data_sent = 0
                send_data = data_file.read(buff)
                while send_data and data_sent < filesize:
                    client_socket.send(send_data)
                    data_sent += buff
                    send_data = data_file.read(buff)

                if not send_data:
                    client_socket.send(send_data)
                    message = client_socket.recv(buff)
                    print message.strip()
                    data_file.close()

            elif 'RETR' in message:
                size = 0.0
                client_socket.send(message)
                recv_message = client_socket.recv(buff)
                reply = recv_message.strip().split()
                size = int(reply[4])
                print size
                received = panjang = 0
                f = ""
                filename = reply[2].split(".")
                received_file = filename[0] + "_downloaded." + filename[1]

                downloaded = open(received_file, "wb")
                while received < size:
                    recv_data = client_socket.recv(buff)
                    f += recv_data
                    received += len(recv_data)
                    if received == (size-buff):
                        for data in recv_data:
                            received += len(data)
                            if received < size:
                                f += data
                            else:
                                recv_message += data
                        break

                downloaded.write(f)
                downloaded.close()
                print recv_message.strip()

            elif message == 'HELP':
                client_socket.send(message)
                recv_message = client_socket.recv(buff)
                count = 0
                while (recv_message):
                    if '\r\n' in recv_message:
                        count += 1
                        if count == 2:
                            print recv_message.strip()
                            count = 0
                            break
                    print recv_message.strip()
                    recv_message = client_socket.recv(buff)

            else:
                client_socket.send(message)
                recv_message = client_socket.recv(1024)
                print recv_message.strip()


except KeyboardInterrupt:
    client_socket.close()
