import http.server
import socketserver

if __name__ == '__main__':
    PORT = 124

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    httpd.serve_forever()
