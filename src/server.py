# _*_utf8_*_

import socket


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()

    try:
        while True:
            incoming_message = ''
            response = response_ok()
            buffer_length = 25
            message_complete = False
            while not message_complete:
                part = conn.recv(buffer_length)
                decoded = part.decode('utf8')
                incoming_message += decoded
                if len(part) < buffer_length:
                    break
            print(incoming_message)
            conn.sendall(response)
            conn.close()
            server.listen(1)
            conn, addr = server.accept()
    except KeyboardInterrupt:
        print('KeyboardInterrupted')
        server.close()
    except:
        response = response_error()
        conn.sendall(response)
        conn.close()
        server.listen(1)
        conn, addr = server.accept()


def response_ok():
    reply_ok = 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\r\nYou Made It!'
    return reply_ok.encode('utf8')


def response_error():
    reply_error = 'HTTP/1.1 500 Internal Server Error\nContent-Type: text/plain\n\r\nSomething bad happened!'
    return reply_error.encode('utf8')


if __name__ == '__main__':
        server()
