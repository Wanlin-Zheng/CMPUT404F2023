import socket
from threading import Thread

#define address & buffer size
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080
BYTES_TO_READ = 4096


def send_request(host, port, request):

    # Create a new socket in with block to ensure it's closed once we're done
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect the socket to host:port
        client_socket.connect((host,port))
        # send the request through the connected socket.
        client_socket.send(request)
        # shut the socket to further wrties. Tells server we're done sending.
        client_socket.shutdown(socket.SHUT_WR)
        # assemble response, be careful here, recall that recv(bytes) blocks until it recieves data
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: #keep reading data until connection terminates
             data = client_socket.recv(BYTES_TO_READ)
             result += data
        # return response
        return result


def handle_connection(conn, addr):
    with conn:
        print(f"CONNECTED BY {addr}")

        request = b''
        while True: # While the client is keeping the socket open
            data = conn.recv(BYTES_TO_READ) # read some data from the socket
            if not data: # if socket has been closed to further writes , break
                break
            print(data) # otherwise print the data to the screen
            request += data
        response = send_request("www.google.com", 80, request) # and snd it as a requst to google
        conn.sendall(response)

# start single threaded echo server
def start_server():
    # create the coket in "with" block to ensure it gets auto-closed once done. 
    # initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #bind socket to address (ip and port)
        s.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #set to listening mode
        s.listen()
        conn, addr = s.accept() # accepting client connection # conn = client socket, addre = IP, port of client
        handle_connection(conn,addr) # sent a response

# start multithreadd echo server
def start_threaded_server():
    #initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #bind socket to address (ip and port)
        s.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #set to listening mode
        s.listen(2) # allow backlog of up to 2 connections 

        while True:

            conn, addr = s.accept() # accepting client connection # conn = client socket, addre = IP, port of client
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

start_server()