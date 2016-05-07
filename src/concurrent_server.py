# -*-coding: utf8-*-

from gevent.server import StreamServer
from gevent.monkey import patch_all
from server import server

ADDRESS = ('127.0.0.1', 5000)


if __name__ == "__main__":
    patch_all()
    server = StreamServer(ADDRESS, server)
    print("Gevent Server on ", ADDRESS)
    try:
        server.serve_forever
    except KeyboardInterrupt:
        print("Connection Out :( ")
        server.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# import socket
# import os
# import io
# import mimetypes


# def response_ok():
#     reply_ok = 'HTTP/1.1 200 OK\nContent-Type: text/plain\r\nYou Made It!'
#     return reply_ok.encode('utf8')


# def response_error():
#     reply_error = 'HTTP/1.1 500 Internal Server Error\nContent-Type: text/plain\r\n\Something bad happened!'
#     return reply_error.encode('utf8')


# def parse_request(request):
#     """A."""
#     main_split = request.split('\r\n')
#     request_headers = main_split[0].split(' ')
#     if 'GET' not in request_headers[0]:
#         print("405 error: Method must be 'GET'")
#         raise NameError
#     elif 'HTTP/1.1' not in request_headers[2]:
#         print("505 error: Protocol must be 'HTTP/1.1'")
#         raise TypeError
#     elif 'Host: localhost' not in request_headers[1]:
#         print("400 error")
#         raise ValueError
#     else:
#         raise AttributeError


# def server_listen(conn):
#     incoming_message = ''
#     incoming_byte = b''
#     buffer_length = 500
#     while True:
#         part = conn.recv(buffer_length)
#         incoming_byte += part
#         incoming_message += part.decode('utf8')
#         if len(part) < buffer_length:
#             break
#     return incoming_message


# def directory_response(direc):
#     print(dir)
#     content = "<!DOCTYPE html>\r\n<html>\r\n<ul>\r\n<body>\r\n\r\n"
#     for i in os.listdir(direc):
#         print(i)
#         if os.path.isdir(os.path.join(direc, i)):
#             content += "<li>{}</li>".format(i)
#         else:
#             content += "<li>{}</li>".format(i)
#     content += "</ul>\r\n</body>\r\n</html>"
#     return content


# def file_response(path):
#     if mimetypes.guess_type(path)[0].startswith('text'):
#         with io.open(path) as f:
#             content = f.read()
#         return (content, "text")
#     elif mimetypes.guess_type(path)[0].startswith('image'):
#         body = "<html><ul>"
#         for item in os.lisdir(path):
#             body += "<a><img src={}></a>".format(item)
#         body += "</ul></html>"
#         return (body, "image")
#     else:
#         return("404 Error")


# def resolve_uri(uri, path='..'):
#     """Resolve uri."""
#     file_type = ""
#     path_root = os.path.join(path, 'webroot', uri[1:])
#     print(path_root)
#     if os.path.isdir(path_root):
#         print("directory", path_root)
#         return directory_response(path_root)
#     elif os.path.isfile(path_root):
#         print("file")
#         file_path = io.open(path_root, 'rb')
#         print("filepath:", file_path)
#         content = file_path.read()
#         print("content:", content)
#         file_type = mimetypes.guess_type(uri)
#         print("type: ", file_type[0])
#         file_path.close()
#         return content, file_type[0]
#     else:
#         return("404 NOT FOUND")


# def server():
#     """Server responds with decoded bytes msg."""
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     address = ('127.0.0.1', 5000)
#     server.bind(address)
#     server.listen(1)
#     conn, addr = server.accept()

#     try:
#         while True:
#             try:
#                 client_conn = server_listen(conn)
#                 print(client_conn)
#                 try:
#                     uri_message = parse_request(client_conn)
#                     print(uri_message)
#                 except ValueError:
#                     response = print("HTTP/1.1 400 Bad Request\r\n")
#                 except TypeError:
#                     response = print("HTTP/1.1 505 HTTP Version Not Supported\r\n")
#                 except NameError:
#                     response = print("HTTP/1.1 405 Method Not Allowed\r\n")
#                 try:
#                     content, file_type = resolve_uri(uri_message)
#                     print("file", file_type)
#                     print("content", content)
#                     response_ok()
#                 except OSError:
#                     response_error()
#                 conn.sendall(conn, response)
#                 break
#             finally:
#                 conn.close
#     except KeyboardInterrupt:
#         print('KeyboardInterrupted')
#         server.close()
#     finally:
#         server.close()


# if __name__ == '__main__':
#         from gevent.server import StreamServer
#         from gevent.monkey import patch_all
#         patch_all()
#         server = StreamServer(('127.0.0.1', 5000), server)
#         server.serve_forever()
#         print("Server starting...")
