import json
import socket
import time

if __name__ == "__main__":
    HOST, PORT = input('HOST: '), 55555

    while True:
        try:
            test_val = 5
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            while True:
                stats = sock.recv(64).decode(encoding='utf-8')
                if stats:
                    print(json.loads(stats))
        except ConnectionResetError:
            sock.close()
            print('Connection Reset Error')
            continue
        except ConnectionRefusedError:
            sock.close()
            print('Connection Refused Error')
            continue
        finally:
            time.sleep(1)
