import socket

a = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 21))

commands = ['USER salman\r\n', 'PASS 123\r\n', 'QUIT\r\n']

i = 1

while True:
    try:
        if i > len(commands):
            msg = str(s.recv(1024))
            break
        s.send(commands[i - 1])
        msg = str(s.recv(1024))
        if "220" in msg:
            msa = msg.replace('msg ', '').replace('220 ', '')
            print msa
        i += 1

    except socket.error, exc:
        # print exc
        s.close()
        break