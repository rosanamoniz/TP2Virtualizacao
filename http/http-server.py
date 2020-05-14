import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

PORT = 8001


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        query_parameters = parse_qs(urlparse(self.path).query)
        if('token' not in query_parameters):
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = f"<html><head></head><body><h1>No token available</h1></body></html>"

            self.wfile.write(bytes(html, "utf8"))
            return
        else:
            token = query_parameters["token"][0]
            # check to see if the token is valid with the authentication server

            # fake flag just to test the server
            authentication = True

            # if valid
            if (authentication == True):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = "<html><head></head><body><h1>{}</h1></body></html>".format(token)

                self.wfile.write(bytes(html, "utf8"))

                return
                # return super().do_GET()
            # if not valid
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = f"<html><head></head><body><h1>Invalid token</h1></body></html>"
                self.wfile.write(bytes(html, "utf8"))


handler = HttpRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()
