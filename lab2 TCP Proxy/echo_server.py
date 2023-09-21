import socket
from threading import Thread

#define address & buffer size
HOST = "127.0.0.1"
PORT = 8080
BYTES_TO_READ = 4096

def handle_connection(conn, addr):
    with conn:
        print(f"CONNECTED BY {addr}")
        while True:
            # wait for a request
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            conn.sendall(data)

# start single threaded echo server
def start_server():
    #initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #bind socket to address (ip and port)
        s.bind((HOST, PORT))
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
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #set to listening mode
        s.listen(2) # allow backlog of up to 2 connections 

        while True:

            conn, addr = s.accept() # accepting client connection # conn = client socket, addre = IP, port of client
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

start_server()
#start_threaded_server()