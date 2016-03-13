# _*_utf8_*_
import socket


def client(message):
    """client sends encoded bytes msg."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    #change to a file/directory
    http_message = "GET images/ HTTP/1.1 \nHost:127.0.0.1\r\n" + message
    client.sendall(http_message.encode('utf8'))

    buffer_length = 25
    reply_complete = False
    while not reply_complete:
        part = client.recv(buffer_length)
        echo = part.decode('utf8')
        print(echo)
        if len(part) < buffer_length:
            break


if __name__ == '__main__':
    client(input(u"what's your message:"))
