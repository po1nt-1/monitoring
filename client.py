import json
import socket
from time import sleep

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            stats = sock.recv(1024).decode(encoding='utf-8')
            if stats:
                print(json.loads(stats))
