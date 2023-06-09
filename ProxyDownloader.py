import sys
import socket
import os
import time


# Global Variables
BUFFER_SIZE = 4096
bilkent = "www.cs.bilkent.edu.tr"


# Function to get the request from the client
def get_request(socket_):
    request = socket_.recv(BUFFER_SIZE).decode('utf-8', 'ignore')
    return request


# Function to parse the URL from the request
def get_parsed_url(request):
    url = request.split(' ')[1]
    # We are dealing with http only
    if url.startswith('http://'):
        url = url[7:]
    server_name = url.split('/')[0]
    file_name = os.path.basename(url)
    parsed_url = '/' + url[len(server_name):]
    return server_name, file_name, parsed_url


# Function to send an HTTP request to the remote server
def send_http_request(url, server_name, socket_):
    http_get_request = f"GET {url} HTTP/1.0\r\nHost: {server_name}\r\n\r\n"
    socket_.sendall(http_get_request.encode())


# Function to get the HTTP response from the remote server
def get_http_response(socket_):
    response = socket_.recv(BUFFER_SIZE)
    status_code = response.split()[1].decode('utf-8', 'ignore')
    print(f"Status code: {status_code} OK") if (status_code == 200) else print(f"Status code: {status_code}")
    return status_code


# Function to handle different operations for different status codes
def status_code_ops(status_code, file_name, socket_):

    if status_code == "200":
        with open(file_name, "wb") as file:
            print(f"Downloading file `{file_name}`...")
            while True:
                incoming_data = socket_.recv(BUFFER_SIZE)
                if not incoming_data:
                    break
                file.write(incoming_data)
        print(f"Saving file {file_name}...")
        print("(Continue with next website)")
    else:
        print("################################################")
        print("Error: File not found or another error occurred.")
        print("################################################")


# Class implementation of ProxyDownloader
class ProxyDownloader:
    def __init__(self, port, host_name='localhost'):
        self.port = port
        self.host_name = host_name
        self.server = None

    # Main function to start the proxy downloader
    def start(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_name, self.port))
        self.server.listen(8)
        print(f"Proxy server listening on the port {self.port}")
        while True:
            client_socket, client_address = self.server.accept()
            request = get_request(client_socket)
            server_name, file_name, parsed_url = get_parsed_url(request)
            if server_name == bilkent:
                print(f"Client connected from the address {client_address}")
                print("Retrieved request from Firefox: \n")
                print(request)
                try:
                    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    start_time = time.time()
                    remote_socket.connect((server_name, 80))
                    end_time = time.time()
                    # Calculating and displaying round trip time
                    rtt = round((end_time - start_time) * 1000, 2)
                    print(f"Round Trip Time: {rtt} ms")
                    send_http_request(parsed_url, server_name, remote_socket)
                    status_code = get_http_response(remote_socket)
                    status_code_ops(status_code, file_name, remote_socket)
                # Throw an exception if there is
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    client_socket.close()


def main():

    arguments = sys.argv

    if len(arguments) == 2:
        port_ = int(sys.argv[1])
        p_downloader = ProxyDownloader(port_)
        p_downloader.start()
    else:
        print("Usage: python3 ProxyDownloader.py <port>")
        sys.exit(1)


if __name__ == "__main__":
    main()
