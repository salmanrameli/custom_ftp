import socket
import threading
import select
import sys
import os


class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 51000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
        except socket.error, (value, message):
            if self.server_socket:
                self.server_socket.close()
            print "error: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input_client = [self.server_socket]

        try:
            while True:
                read_ready, write_ready, exception = select.select(input_client, [], [])

                for ready in read_ready:
                    if ready == self.server_socket:
                        client_service = Client(self.server_socket.accept())
                        client_service.start()
                        self.threads.append(client_service)
                        print "Menerima %d koneksi" %len(self.threads)

        except KeyboardInterrupt:
            self.server_socket.close()
            sys.exit(0)


class Client(threading.Thread):
    def __init__(self,(client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def stop(self):
        self.running = False
        self.client.close()
        server_socket.threads.pop()

    def run(self):
        self.client.send('220 Welcome!\r\n')
        while True:
            data = self.client.recv(self.size)
            if 'status' in data:
                self.client.send("status ok")
            if data == 'QUIT':
                self.client.send("221 Goodbye.\r\n")
                self.stop()
                print "Menerima %d koneksi" %len(server_socket.threads)
                break
            if data == 'PWD':
                pwd = os.getcwd()
                self.client.send(pwd)
            if 'DELE' in data:
                message = data.strip().split()
                os.remove(message[1])
                self.client.send("File " + message[1] + " berhasil dihapus")
            print data.strip()
        pass


if __name__ == "__main__":
    server_socket = Server()
    server_socket.run()
