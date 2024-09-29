import socket
import sys
import argparse
import threading

LINE_LEN = 4096
HOST = "0.0.0.0"

def parse_args():
    parser = argparse.ArgumentParser(description="Client-server application using TCP sockets over the network")
    parser.add_argument('-p', '--port', type=int, required=True, help="Accepts the port to listen on")
    return parser.parse_args()  

def setup_server_socket(PORT):
    connection = (HOST, PORT)
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(connection)
        server_sock.listen(5)
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
        count = sum(c.isalpha() for c in file_data.decode('utf-8'))
        client_socket.send(str(count).encode('utf-8', errors='ignore'))
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
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_sock.close()


def main():
    args = parse_args()
    PORT = args.port
    server_sock = setup_server_socket(PORT)
    wait_for_connection(server_sock)
    

if __name__=="__main__":
    main()
