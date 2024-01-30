import socketserver
from dotenv import load_dotenv
import os
from request_handler import CustomHttpRequestHandler

load_dotenv()

server_address = (os.environ['HTTP_SERVER_ADDRESS'],
                  int(os.environ['HTTP_SERVER_PORT']))

handler = CustomHttpRequestHandler
with socketserver.TCPServer(server_address, handler) as httpd:
    httpd.serve_forever()
