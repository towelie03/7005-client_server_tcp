import socket
import sys
import argparse
from ipaddress import ip_address

LINE_LEN = 4096

def parse_args():
    parser = argparse.ArgumentParser(description="Client-server application using TCP sockets over the network")
    parser.add_argument('-i', '--ip', type=ip_address, required=True, help="Accepts the ip address to send on")
    parser.add_argument('-p', '--port', type=int, required=True, help="Accepts the port to send on")
    parser.add_argument('-f', '--file', type=str, required=True, help="Path of files to send")
    return parser.parse_args()  # Return the parsed arguments

def connect_to_server(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((str(ip), port))
            return sock
    except Exception as e:
        print(f"Error: Unable to connect to server socket: {e}")
        sys.exit(1)

def send_file(sock, file_path):
    try:
        with open(file_path, 'rb') as file:
            while True:
                file_data = file.read(LINE_LEN)
                if not file_data:
                    break
                sock.sendall(file_data)
            print("File sent successfully.")
    except Exception as e:
        print(f"Error: Unable to send request: {e}")
        sock.close()
        sys.exit(1)

def receive_response(sock):
    try:
        response = sock.recv(LINE_LEN)
        return response.decode('utf-8')
    except Exception as e:
        print(f"Error: Unable to receive response: {e}")
        sys.exit(1)

def main():
    args = parse_args()
    sock = connect_to_server(args.ip, args.port)
    print(f"Connecting to {args.ip} on port {args.port} with file {args.file}")
    
    try:
        send_file(sock, args.file)
        response = receive_response(sock)
        print(f"Number of alphabetic letters: {response}")
    finally:
        sock.close()

if __name__=="__main__":
    main()
