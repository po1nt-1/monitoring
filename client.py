import json
import socket
import time

if __name__ == "__main__":
    HOST, PORT = input('HOST: '), 55555
    TIMEOUT = 9

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            time_ = time.time()
            while True:
                stats = sock.recv(64).decode(encoding='utf-8')
                if stats:

                    print(json.loads(stats))

                    time_ = time.time()
                if time.time() - time_ > TIMEOUT:
                    break
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
