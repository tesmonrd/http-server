# _*_utf8_*_

import socket
import sys


def client(message):
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))

    buffer_length = 8
    reply_complete = False
    while not reply_complete:
        part = client.recv(buffer_length)
        print(part.decode('utf8'))
        if len(part) < buffer_length:
            break


if __name__ == '__main__':
    try:
        client(input(u"What is your message:"))
    except KeyboardInterrupt:
        print('KeyboardInterrupted')
        sys.exit(0)
