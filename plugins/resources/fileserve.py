import http.server
import socketserver


def fserve():
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 124), Handler)
    httpd.serve_forever()


if __name__ == '__main__':
    fserve()
