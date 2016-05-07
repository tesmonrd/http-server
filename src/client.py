# _*_utf8_*_
import socket
import sys


def client(message):
    """Client sends encoded bytes msg."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])

    client.sendall(message.encode('utf8'))
    client.shutdown(socket.SHUT_WR)

    buffer_msg = ''
    buffer_length = 50
    reply_complete = False
    while not reply_complete:
        part = client.recv(buffer_length)
        buffer_msg += part.decode('utf8')
        print(buffer_msg)
        if len(part) < buffer_length:
            break

    client.close()
    return buffer_msg

if __name__ == '__main__':
    client(sys.argv[1])
