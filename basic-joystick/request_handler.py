import http.server
import os


class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        with open('index.html', 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(
            'SOCKET_SERVER_PROTOCOL', os.environ['SOCKET_SERVER_PROTOCOL'])
        filedata = filedata.replace(
            'SOCKET_SERVER_ADDRESS_CLIENT', os.environ['SOCKET_SERVER_ADDRESS_CLIENT'])
        filedata = filedata.replace(
            'SOCKET_SERVER_PORT', os.environ['SOCKET_SERVER_PORT'])

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(filedata, "utf8"))

        return
