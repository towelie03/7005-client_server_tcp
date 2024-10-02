import socket
import sys
import argparse
from ipaddress import ip_address
import os

LINE_LEN = 4096

def parse_args():
    parser = argparse.ArgumentParser(description="Client-server application using TCP sockets over the network")
    parser.add_argument('-i', '--ip', type=ip_address, required=True, help="Accepts the IP address to send on")
    parser.add_argument('-p', '--port', type=int, required=True, help="Accepts the port to send on")
    parser.add_argument('-f', '--file', type=str, required=True, help="Path of the file to send")
    return parser.parse_args()  # Return the parsed arguments

def connect_to_server(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(ip), port))
        print(f"Socket created and connected to {ip}:{port}")
        return sock
    except Exception as e:
        print(f"Error: Unable to connect to server socket: {e}")
        sys.exit(1)

def send_file(sock, file_path):
    try:
        if not os.path.isfile(file_path):
            print(f"Error: The file '{file_path}' does not exist.")
            return
        
        # Send the file path first
        print(f"Sending file path: {file_path}")
        sock.sendall(file_path.encode('utf-8'))
        sock.sendall(b'\0')  # Null byte as delimiter to indicate end of the file path
        
        # Send the file content
        print(f"Sending file content of: {file_path}")
        with open(file_path, 'rb') as file:
            while True:
                file_data = file.read(LINE_LEN)
                if not file_data:
                    break
                sock.sendall(file_data)
        print("File sent successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
    except Exception as e:
        print(f"Error: Unable to send file: {e}")

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
    
    try:
        send_file(sock, args.file)
        response = receive_response(sock)  # Ensure this is called after sending the file
        print(f"Number of alphabetic letters: {response}")
    finally:
        if sock:
            sock.close()  # Close the socket only after receiving the response

if __name__ == "__main__":
    main()

