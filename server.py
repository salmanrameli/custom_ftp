import socket
import threading
import select
import sys
import os
import time

default_commands = ["USER", "PASS", "ACCT", "CWD", "CDUP", "SMNT", "QUIT", "REIN",
"PORT", "PASV", "TYPE", "STRU", "MODE", "RETR", "STOR", "STOU", "APPE", "ALLO",
"REST", "RNFR", "RNTO", "ABOR", "DELE", "RMD", "MKD", "PWD", "LIST", "NLST", "SITE",
"SYST", "STAT", "HELP", "NOOP"]

user_name = ["a", "b"]
user_pass = ["a", "b"]
user_auth = [0, 0]
user_add = [0, 0]


class Server:
    def __init__(self):
        self.host = '10.181.1.246'
        self.port = 51000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        self.basedir = os.path.abspath('.')
        self.commands = ["USER", "PASS", "CWD", "QUIT", "RETR", "STOR", "RNTO", "DELE",
                        "MKD", "PWD", "LIST", "HELP", "RMD"]


    def open_socket(self):
        try:
            print "Starting server"
            print "Path: " + os.path.abspath('.')
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print "Server started succesfully"
        except socket.error, (value, message):
            if self.server_socket:
                self.server_socket.close()
            print "Failed to start. Error: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input_client = [self.server_socket]

        try:
            while True:
                read_ready, write_ready, exception = select.select(input_client, [], [])

                for ready in read_ready:
                    if ready == self.server_socket:
                        client_service = Client(self.server_socket.accept(), initpath=os.path.abspath('.'))
                        client_service.start()
                        print client_service
                        self.threads.append(client_service)
                        print "Got %d connection" % len(self.threads)

        except KeyboardInterrupt:
            self.server_socket.close()
            sys.exit(0)


class Client(threading.Thread):
    def __init__(self, (client, address), initpath):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.basedir = server_socket.basedir
        os.chdir(initpath)

    def stop(self):
        self.running = False
        self.client.close()
        server_socket.threads.pop()

    def run(self):
        os.chdir(self.basedir)
        #print self.basedir
        self.client.send('220 Welcome!\r\n')
        while True:
            data = self.client.recv(self.size)
            print data.strip()
            datacommand = data.split()[0]

            if datacommand in server_socket.commands:
                if 'USER' in data:
                    message = data.strip().split()
                    name = message[1]
                    if name in user_name:
                        self.client.send("331 User %s OK. Password required.\r\n" % name)
                    else:
                        self.client.send("530 User cannot log in. \r\n Login failed.")

                if 'PASS' in data:
                    message = data.strip().split()
                    password = message[1]
                    if password in user_pass:
                        #print name + "????"
                        self.client.send("230 User %s logged in, proceed. \r\n" % password)
                        # index = user_name.index(name)
                        # user_auth[index] = 1
                        data = self.client.recv(self.size)
                        print data.strip()
                        datacommand = data.split()[0]

                    for i in user_auth:
                        print i
                    else:
                        self.client.send("530 User cannot log in. \r\n Login failed.")

                if data == 'QUIT':
                    self.client.send("221 Goodbye.\r\n")
                    # index = user_name.index(name)
                    # user_auth[index] = 0
                    # for i in user_auth:
                    #     print i
                    self.stop()
                    print "Got %d connection " % len(server_socket.threads)
                    break

                if data == 'PWD':
                    pwd = os.getcwd()
                    self.client.send(pwd)

                if data == 'HELP':
                    self.client.send("214 The following commands are recognized:\r\n")
                    i = 1
                    commands = ''
                    for command in server_socket.commands:
                        commands += command.strip() + '\t'
                        if i % 5 == 0:
                            commands += ('\n')
                        i+=1
                    self.client.send(commands + '\r\n')

                if 'DELE' in data:
                    message = data.strip().split()
                    os.remove(message[1])
                    self.client.send("250 File " + message[1] + " successfully deleted")

                if data == 'LIST':
                    self.client.send("150 Here comes the directory listing. \r\n")
                    print 'list', os.getcwd()
                    mypath = os.getcwd()
                    for filename in os.listdir(mypath):
                        st = os.stat(filename)
                        fullmode = 'rwxrwxrwx'
                        permission = ''
                        for i in range(9):
                            permission += ((st.st_mode)>>(8-i)&1) and fullmode[i] or '-'
                        d = (os.path.isdir(filename)) and 'd' or '-'
                        ftime = time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
                        listing = d + permission + '\t' + str(st.st_size) + '\t' + ftime + '\t' + os.path.basename(filename)
                        self.client.send(listing + '\r\n')
                    self.client.send('226 Directory send OK.\r\n')

                if 'MKD' in data:
                    path = os.getcwd()
                    message = data.strip().split()
                    os.mkdir(path + '/' + message[1])
                    self.client.send("257 Directory " + message[1] + " successfully created")

                if 'RMD' in data:
                    path = os.getcwd()
                    message = data.strip().split()
                    os.rmdir(path + '/' + message[1])
                    self.client.send("250 Directory " + message[1] + " successfully removed")

                if 'CWD' in data: #masih ngebug kalau >1 client
                    message = data.strip().split()
                    chdir = message[1]
                    if(chdir == '/'):
                        os.chdir("..")
                        print self.basedir
                        path = os.getcwd()
                        print path
                    else:
                        chdir = chdir.strip('/')
                        #self.basedir = os.path.join('/', os.getcwd(), chdir)
                        self.basedir = os.chdir(chdir)
                        print self.basedir
                        #os.chdir(os.path.join(self.basedir, chdir).strip('/'))
                        #print os.getcwd()
                    self.client.send("250 Ok.")

                if 'RNTO' in data:
                    message = data.strip().split()
                    os.rename(message[1], message[2])
                    self.client.send("250 Renamed " + message[1] + " to " + message[2])

                if 'RETR' in data:
                    message = data.strip().split()
                    filesize = os.path.getsize(message[1])
                    print filesize
                    self.client.send("150 Sending " + message[1] + " filesize " + str(filesize) + "\r\n")
                    self.client.send("250 Completed\r\n")
                    open_file = open(message[1], 'rb')

                    while filesize > 0:
                        if filesize <= 0:
                            open_file.close()
                            break
                        else:
                            data_file = open_file.read(1024)
                            self.client.send(data_file)
                            filesize -= len(data_file)

                if 'STOR' in data:
                    message = data.strip().split()
                    filesize = int(message[2])
                    name = message[1].split(".")

                    received_file = name[0] + "_uploaded." + name[1]
                    self.client.send("150 Opening data connection for " + message[1] + " filesize " + str(filesize) + "\r\n")
                    self.client.send("250 Completed\r\n")
                    f = ""
                    retrieve = open(received_file, 'wb')
                    received = 0
                    while received < filesize:
                        recv_data = self.client.recv(1024)
                        f += recv_data
                        received += len(recv_data)
                        if received == (filesize-1024):
                            for data in recv_data:
                                received += len(data)
                                if received < filesize:
                                    print received
                                    f += data
                                #else:
                                    #recv_message += data
                            break
                    retrieve.write(f)
                    retrieve.close()

            else:
                if datacommand in default_commands:
                    self.client.send("202 Command not implemented, superfluous at this site.")
                else:
                    self.client.send("500 Syntax error, command unrecognized.")

if __name__ == "__main__":
    server_socket = Server()
    server_socket.run()
