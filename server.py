import socket
import threading
import select
import sys


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

        except KeyboardInterrupt:
            self.server_socket.close()
            sys.exit(0)


class Client(threading.Thread):
    def __init__(self,(client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        while True:
            data = self.client.recv(self.size)
            if 'exit' in data:
                break
            if 'status' in data:
                self.client.send("status ok")
            else:
                self.client.send("pesan diterima")
            print data.strip()


if __name__ == "__main__":
    server_socket = Server()
    server_socket.run()
