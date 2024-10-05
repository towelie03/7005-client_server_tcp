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

def wait_for_connection(server_sock):
    try:
        conn, client_addr = server_sock.accept()
        print(f"Server is listening on {client_addr}")
        return conn
    except Exception as e:
        print(f"Error: Unable to accept connection: {e}")
        return None

def count_alphabetical(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            alphabetic_count = sum(c.isalpha() for c in data.decode('utf-8', errors='ignore'))
            return alphabetic_count
    except Exception as e:
        print(f"Error: Unable to count alphabetic letters: {e}")
        return None  

def handle_client(conn):
    try:
        file_path_bytes = bytearray()
        while True:
            chunk = conn.recv(LINE_LEN)
            file_path_bytes.extend(chunk)
            if b'\0' in chunk: 
                break
        
        file_path = file_path_bytes[:file_path_bytes.index(0)].decode('utf-8')

        print(f"Received file request: {file_path}")

        alphabetic_count = count_alphabetical(file_path)
        if alphabetic_count is not None:
            send_reply(conn, str(alphabetic_count))
        else:
            send_reply(conn, f"Error: Unable to count characters in file '{file_path}'")

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        conn.close()


def send_reply(conn, reply):
    try:
        conn.sendall(reply.encode('utf-8'))
    except BrokenPipeError:
        print("Error: Client disconnected unexpectedly.")
    except Exception as e:
        print(f"Error: Unable to send response: {e}")

def main():
    args = parse_args()
    PORT = args.port

    server_sock = setup_server_socket(PORT)

    try:
       while True:
            conn = wait_for_connection(server_sock)
            if conn is not None:
                client_thread = threading.Thread(target=handle_client, args=(conn,))
                client_thread.start()   
    except KeyboardInterrupt:
        print("\nShutting down and closing the connection")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()

