# Proxy Downloader

This project provides a Python-based HTTP proxy downloader. It accepts client requests, parses the request to extract the URL, sends an HTTP GET request to the remote server, receives the HTTP response, and finally downloads the file if the request is successful.

## File Structure

The project is comprised of a single Python file:

1. **ProxyDownloader.py**

This script is the main body of the proxy downloader. It includes various functions to handle client requests, send HTTP GET requests, receive and interpret HTTP responses, and save the requested file to disk if the request is successful.

## Code Explanation

The `ProxyDownloader.py` script defines several functions for handling HTTP requests and responses:

- `get_request()`: This function accepts the client socket as an argument and reads the client's request from this socket.
- `get_parsed_url()`: This function parses the client's HTTP GET request to extract the URL of the requested file.
- `send_http_request()`: This function sends an HTTP GET request to the remote server specified by the URL.
- `get_http_response()`: This function reads the HTTP response from the remote server.
- `status_code_ops()`: This function interprets the HTTP response code from the remote server. If the response code is 200 (OK), the function saves the requested file to disk.

The script also defines the `ProxyDownloader` class, which encapsulates the functionality of the proxy downloader:

- `start()`: This function is the main function of the `ProxyDownloader` class. It sets up the server socket, enters an infinite loop to listen for client connections, and handles each client connection by processing the HTTP GET request and downloading the requested file (if the request is successful).

Finally, the script defines a `main()` function, which parses command line arguments to get the port number, creates an instance of the `ProxyDownloader` class, and starts the proxy downloader.

## Running the Project

To run this project, you need Python 3.x and a command-line interface.

Here is the syntax to run the script:

