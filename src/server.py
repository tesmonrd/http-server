# _*_utf8_*_

import socket


def server():
    """Server responds with decoded bytes msg."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()
    buffer_length = 8
    message_complete = False

    try:
        while not message_complete:
            part = conn.recv(buffer_length)
            print(part.decode('utf8'))
            conn.sendall(part)
            if len(part) < buffer_length:
                break
        conn.close()
        server.listen(1)
        conn, addr = server.accept()
    except KeyboardInterrupt:
        print('KeyboardInterrupted')
        conn.close()
    except:
        server.listen(1)
        conn, addr = server.accept()


if __name__ == '__main__':
        server()
