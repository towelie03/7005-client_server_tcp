import socket
import sys
import os
import stat
import argparse
import threading

# Global variables
SOCKET_PATH = '/tmp/socket'
LINE_LEN = 4096
HOST = "0.0.0.0"

def parse_args():
    parser = argparse.ArgumentParser(description="Client-server application using TCP sockets over the network")
    parser.add_argument('-p', '--port', required=True, help="Accepts the port to listen on")
    return parser.parse_args()  # Return the parsed arguments

# def check_socket_path():
#     if os.path.exists(SOCKET_PATH):
#         # Attempt to check if it's a socket file
#         try:
#             if stat.S_ISSOCK(os.stat(SOCKET_PATH).st_mode):
#                 os.remove(SOCKET_PATH)
#                 print(f"Removed existing socket file: {SOCKET_PATH}")
#             else:
#                 print(f"Warning: '{SOCKET_PATH}' exists but is not a socket file.")
#         except Exception as e:
#             print(f"Error checking socket file: {e}")
#     else:
#         print(f"No existing socket file to remove at: {SOCKET_PATH}")
#

def setup_server_socket(PORT):
    try:        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.bind((HOST, PORT))
            server_sock.listen()
            print(f"Server listening on port {PORT}")
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
    server_sock = setup_server_socket(args.PORT)
    wait_for_connection(server_sock)
    

if __name__=="__main__":
    main()
