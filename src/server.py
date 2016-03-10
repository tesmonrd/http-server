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
        while True:
            try:
                incoming_message = ''
                response = response_ok()
                buffer_length = 25
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    decoded = part.decode('utf8')
                    print(decoded)
                    incoming_message += decoded
                    parse_request(decoded)
                    if len(part) < buffer_length:
                        break
                print(incoming_message)
                try:
                    conn.sendall(response(parse_request(incoming_message)))
                except:
                    pass
                conn.close()
                server.listen(1)
                conn, addr = server.accept()
            except:
                response = response_error()
                conn.sendall(response)
    except KeyboardInterrupt:
        print('KeyboardInterrupted')
        server.close()
    finally:
        conn.close()
        server.listen(1)
        conn, addr = server.accept()


def response_ok():
    reply_ok = 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\r\nYou Made It!'
    return reply_ok.encode('utf8')


def response_error():
    reply_error = 'HTTP/1.1 500 Internal Server Error\nContent-Type: text/plain\n\r\nSomething bad happened!'
    return reply_error.encode('utf8')


def parse_request(request):
    """A."""
    replaced_n = request.replace('\n', ' ')
    parsed_request = replaced_n.split('')
    try:
        parsed_request[0] == 'GET'
    except:
        raise RuntimeError
        print("405 error: Method must be 'GET'")
    try:
        parsed_request[2] == 'HTTP/1.1'
    except:
        raise RuntimeError
        print("505 error: Protocol must be 'HTTP/1.1'")
    try:
        parsed_request[3:4] == 'Host:'
    except:
        raise RuntimeError
        print("404 error")
    return parsed_request


if __name__ == '__main__':
        server()
