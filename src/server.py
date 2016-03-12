# -*-coding: utf8-*-

import socket
import os
import mimetypes


root = "../webroot/"


def server():
    """Server responds with decoded bytes msg."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()
    buffer_length = 16
    message_complete = False

    try:
        while True:
            try:
                import pdb; pdb.set_trace()
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
                try:
                    uri_message = parse_request(incoming_message)
                    print("WERE IN OUT OF THE LOOP")
                    resolve_uri(uri)

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
    reply_ok = 'HTTP/1.1 200 OK\nContent-Type: text/plain\r\nYou Made It!'
    return reply_ok.encode('utf8')


def response_error():
    reply_error = 'HTTP/1.1 500 Internal Server Error\nContent-Type: text/plain\r\n\Something bad happened!'
    return reply_error.encode('utf8')


def parse_request(request):
    """A."""
    uri = ''
    header_body_split = request.split('\r\n')
    headers = header_body_split[0]
    headers_n = headers.replace('\n', '')
    headers_nc = headers_n.replace(':', ' ')
    parsed_request = headers_nc.split(' ')
    uri += parsed_request[1:]
    if 'GET' not in parsed_request[0]:
        print("405 error: Method must be 'GET'")
        raise RuntimeError
    elif 'HTTP/1.1' not in parsed_request[3]:
        print("505 error: Protocol must be 'HTTP/1.1'")
        raise RuntimeError
    elif 'Host' not in parsed_request[4]:
        print("404 error")
        raise RuntimeError
    else:
        response_ok()
        rejoined = " ".join(str(i) for i in parsed_request)
    return rejoined


def directory_response(path):
    path = os.path.join(root, uri)
    body = "<html><ul>"
    for item in os.lisdir(path):
        body += "<li>{}</li>".format(item)
    body += "</ul></html>"
    response_ok()
    return(body, "content is directory")


def file_response(path):
    if mimetypes.guess_type(path)[0].startswith('text'):
        with io.open(path) as f:
            content = f.read()
        response_ok()
        return (content, "text")
    elif mimetypes.guess_type(path)[0].startswith('image'):
        body = "<html><ul>"
        for item in os.lisdir(path):
            body += "<a><img src={}></a>".format(item)
        body += "</ul></html>"
        response_ok()
        return (body, "image")
    else:
        response_error()
        return("404 Error")


def resolve_uri(uri):
    """resolve uri."""
    path = os.path.join(root, uri)
    print(path)
    if os.path.isdir(path):
        return directory_response(path)
    elif os.path.isfile(path):
        return file_response(path)
    else:
        return("404 NOT FOUND")


if __name__ == '__main__':
        server()
