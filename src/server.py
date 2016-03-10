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


def parse_request(request):
    """A."""
    replaced_n = request.replace('\n', ' ')
    parsed_request = replaced_n.split('')
    while True:
        try:
            parsed_request[0] == 'GET'
        except IndexError:
            print("Index Error, method must be 'GET'")
            # continue

        try:
            parsed_request[2] == 'HTTP/1.1'
        except IndexError:
            print("Index Error, protocol must be 'HTTP/1.1'")
            # continue
        try:
            parsed_request[3] == 'Host:'
        except IndexError:
            print("Index Error, header must be 'Host:'")
            # continue
        finally:
            print(parsed_request[4])
            return parsed_request[4]


if __name__ == '__main__':
        server()
