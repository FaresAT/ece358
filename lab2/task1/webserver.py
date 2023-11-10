import socket
from datetime import datetime
import os

# Configuration
HOST, PORT = '127.0.0.1', 10000  # Loopback address and port number > 1023
BUFFER_SIZE = 1024
SERVER_NAME = 'Python Simple Server'
CONTENT_TYPE_MAPPING = {
    '.html': 'text/html',
    '.txt': 'text/plain',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    # Add more mappings if needed.
}

# Function to generate HTTP response headers
def generate_headers(code, filepath):
    header = ''
    if code == 200:
        header += 'HTTP/1.1 200 OK\n'
    elif code == 404:
        header += 'HTTP/1.1 404 Not Found\n'

    date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    header += f'Date: {date}\n'
    header += f'Server: {SERVER_NAME}\n'
    header += 'Connection: close\n'  # For simplicity, we'll close the connection after completing the request

    if code == 200:
        file_size = os.path.getsize(filepath)
        header += f'Content-Length: {file_size}\n'
        _, file_extension = os.path.splitext(filepath)
        header += f'Content-Type: {CONTENT_TYPE_MAPPING.get(file_extension, "application/octet-stream")}\n'
        last_modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        header += f'Last-Modified: {last_modified}\n'

    header += '\n'  # Blank line between headers and content
    return header

# Function to handle the request
def handle_request(client_socket):
    request = client_socket.recv(BUFFER_SIZE).decode()
    request_method = request.split(' ')[0]
    if request_method in ['GET', 'HEAD']:
        filename = request.split(' ')[1]
        filename = filename.split('?')[0]  # Ignore query parameters
        if filename == '/':
            filename = '/index.html'  # Default file
        filepath = '.' + filename  # Current directory

        if os.path.isfile(filepath):
            response_header = generate_headers(200, filepath)
            if request_method == 'GET':
                with open(filepath, 'rb') as file:
                    response_data = file.read()
                response = response_header.encode() + response_data
            else:  # HEAD request
                response = response_header.encode()
        else:
            response_header = generate_headers(404, None)
            response_data = '<html><body><h1>404 Not Found</h1></body></html>'.encode()
            response = response_header.encode() + response_data

        client_socket.sendall(response)
    else:
        print(f"Unhandled HTTP method: {request_method}")

# Create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening on {HOST}:{PORT}...")

    while True:
        client_socket, _ = server_socket.accept()
        handle_request(client_socket)
        client_socket.close()
