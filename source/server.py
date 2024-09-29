import socket
import sys
import argparse
import threading

# Global variables
SOCKET_PATH = '/tmp/socket'
LINE_LEN = 4096
HOST = "0.0.0.0"

def parse_args():
    parser = argparse.ArgumentParser(description="Client-server application using TCP sockets over the network")
    parser.add_argument('-p', '--port', required=True, help="Accepts the port to listen on")
    return parser.parse_args()  

def setup_server(port):
    try:        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.bind((HOST, port))
            server_sock.listen()
            print(f"Server listening on port {port}")
            return server_sock
    except Exception as e:
        print(f"Error: Unable to create server socket: {e}")
        sys.exit(1)

def handle_client(client_socket):
    try:
        file_data = b""
        while True:
            chunk = client_socket.recv(LINE_LEN)
            if not chunk:
                break
            file_data += chunk
        count = sum(c.isalpha() for c in file_data.decode('utf-8', errors='ignore'))
        client_socket.send(str(count).encode('utf-8'))
    finally:
        client_socket.close()

def wait_for_connection(server_sock):
    try:
        while True:
            conn, client_addr = server_sock.accept()
            print(f"Server is listening on {client_addr}")
            client_handler = threading.Thread(target=handle_client, args=(conn,))
            client_handler.start()
    except Exception as e:
        print(f"Error: Unable to accept connection: {e}")


def main():
    args = parse_args()
    server_sock = setup_server(args.port)
    wait_for_connection(server_sock)
    

if __name__=="__main__":
    main()
