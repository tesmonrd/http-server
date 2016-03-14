# _*_utf8_*_
import socket
import sys


def client(message):# where is argument being passed in the func?
    """Client sends encoded bytes msg."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    http_message = "GET 127.0.0.1:5000 HTTP/1.1 \nHost: 127.0.0.1\r\nHello"
    client.sendall(http_message.encode('utf8'))
    # http_message[1]should be {}.format(client(input)).input can be directory or file or error.

    buffer_length = 50
    reply_complete = False
    while not reply_complete:
        part = client.recv(buffer_length)
        echo = part.decode('utf8')
        print(echo)
        if len(part) < buffer_length:
            break


if __name__ == '__main__':
    client(sys.argv[1])#input
