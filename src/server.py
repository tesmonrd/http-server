# # -*-coding: utf8-*-
import socket
import os
import io
import sys
import mimetypes

buffer_length = 1024
PORT = 5000
IP = "127.0.0.1"

ROOT = "../webroot/"


def setup_server():
    """Setup on localhost."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind((IP, PORT))
    server.listen(5)
    return server


def server_listen(server):
    """Accept connections from the client."""
    conn, addr = server.accept()
    return (conn, addr)


def server_read(connection):
    """Read parse message."""
    string = ''.encode('utf-8')
    while True:
        part = connection.recv(buffer_length)
        string += part
        if len(part) < buffer_length or len(part) == 0:
            break
    return string.decode('utf-8')


def parse_request(request):
    """Parse HTTP request."""
    print([request])
    request_line = request.split('\n')[0]
    request_line = request_line.strip()
    try:
        method, uri, version = request_line.split()
    except ValueError:
        raise SyntaxError('400: Bad Request (6)')
    if method.upper() != 'GET':
        raise TypeError('405: Method Not Allowed')
    if version.upper().split('/')[0] != 'HTTP':
        raise TypeError('400: Bad Request (5)')
    if version.upper().split('/')[1] != '1.1':
        raise ValueError('505: Invalid HTTP Version')
    headers = parse_headers(request)
    content, mime = resolve_uri(uri)
    return (content, mime)


def parse_headers(request):
    """Validate and parse headers."""
    parsed_headers = {}
    http_header = request.replace('\r', '').split('\n')[1:]
    if not http_header:
        raise KeyError("400: Bad Request (3)")
    idx = http_header.index('')
    http_header = http_header[:idx]
    for header in http_header:
        if not len(header.split(': ')) == 2:
            raise SyntaxError('400: Bad Request (2)')
        header_key, header_value = header.split(': ')
        parsed_headers[header_key.lower()] = header_value
    if not parsed_headers.get('host'):
        raise KeyError("400: Bad Request (1)")
    return parsed_headers


def server_response(string, connection):
    """Send back string to connection."""
    if isinstance(string, bytes):
        connection.send(string)
    else:
        connection.send(string.encode('utf-8'))


def response_ok(content, tag):
    """Send back ok HTTP."""
    if isinstance(content, bytes):
        to_return = b"HTTP/1.1 200 OK\r\nContent-type: " + bytes(tag.encode()) + b"\r\n" + b"Content-length: " + bytes(str(len(content)).encode()) + b"\r\n\r\n" + content
        return to_return
    else:
        return ("HTTP/1.1 200 OK\r\nContent-type: {}\r\nContent-length: {}\r\n\r\n{}".format(tag, len(content), content))


def response_error(code, message="ERROR"):
    """Send back error."""
    return "HTTP/1.1 {} nContent-type: text/html\r\n\r\n{}".format(code, message)


def directory_response(path):
    """Return listing of directory."""
    html_return = "<ul>"
    for node in os.listdir(path):
        print(path)
        if os.path.isdir(os.path.join(path, node)):
            html_return += "<a href=\"{}/\"><li>{}</li></a>".format(node, node)
        else:
            html_return += "<a href=\"{}\"><li>{}</li></a>".format(node, node)
    html_return += "</ul>"
    return (html_return, "text/html")


def file_response(path):
    """Return file."""
    try:
        if mimetypes.guess_type(path)[0].startswith('text'):
            with io.open(path, 'rb') as f:
                content = f.read()
            return (content, mimetypes.guess_type(path)[0])
        else:
            assert os.path.isfile(path)
            with io.open(path, 'rb') as f:
                content = f.read()
            return (content, mimetypes.guess_type(path)[0])
    except Exception as e:
        sys.exit(e)
        raise IOError("404: Not Found")


def resolve_uri(uri):
    """Resolve uri."""
    path = os.path.join(ROOT, uri[1:])
    if os.path.isdir(path):
        return directory_response(path)
    elif os.path.isfile(path):
        return file_response(path)
    else:
        print("404: Not Found", path)
        raise IOError("404: Not Found")


def server():
    """Main server."""
    try:
        socket = setup_server()
        while True:
            connection, address = socket.accept()
            try:
                result, mime = parse_request(server_read(connection))
                print("log:", result)
                to_send = response_ok(result, mime)
                server_response(to_send, connection)
            except Exception as error:
                try:
                    error = error.args[0]
                    code = int(error.split(':')[0])
                    error = error.split(':')[1].strip()
                except:
                    code = 500
                    error = "Server Error"
                server_response(response_error(code, error), connection)
            finally:
                connection.close()
    except KeyboardInterrupt:
        print("Server closed :( ")
        try:
            connection.close()
        except NameError:
            pass
    finally:
        socket.close()

if __name__ == "__main__":
    server()
