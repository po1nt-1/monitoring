import json
import socket

if __name__ == "__main__":
    HOST, PORT = input('HOST: '), 55555

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            stats = sock.recv(64).decode(encoding='utf-8')
            if stats:
                print(json.loads(stats))
