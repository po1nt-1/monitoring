import json
import socket
import sys
import threading
import time

import psutil

HOST, PORT = '0.0.0.0', 55555

stats = {}
step = 1
clients = {}


def monitor(period):
    try:
        global stats
        global step

        time_ = 0
        while True:
            if time.time() - time_ > period:
                time_ = time.time()

                print('Monitoring..')
                cpu = psutil.cpu_percent(0.1)
                r = psutil.virtual_memory()
                data = {'cpu': cpu, 'ram': [r.percent, r.used / (1024**3)]}

                stats = json.dumps(data).encode(encoding='utf-8')

                step += 1
    except KeyboardInterrupt:
        return -1


def sender():
    try:
        global stats
        global clients
        global step

        while True:
            if step % 2 == 0 and stats and clients:
                kick_list = []
                local_clients = clients.copy()
                for addr, conn in local_clients.items():
                    try:
                        conn.sendall(stats)
                    except BrokenPipeError:
                        kick_list.append(addr)
                        print(f'{addr}', 'disconnected')
                    except ConnectionResetError:
                        kick_list.append(addr)
                        print(f'{addr}', 'disconnected')

                for ip in kick_list:
                    clients.pop(ip)

                stats = {}
    except KeyboardInterrupt:
        return -1


def main():
    try:
        global clients

        arg = sys.argv[1]
        if not arg or not arg.isnumeric():
            raise IndexError
        else:
            period = int(arg)
            if not period > 0:
                raise IndexError

        thread = threading.Thread(target=monitor, args=(period,))
        thread.setDaemon(True)
        thread.start()

        thread = threading.Thread(target=sender)
        thread.setDaemon(True)
        thread.start()

        clients = {}
        server = socket.socket()
        server.bind((HOST, PORT))
        server.listen()

        while True:
            conn, addr = server.accept()
            print(f'{addr[0]}:{addr[1]}', 'connected')
            if f'{addr[0]}:{addr[1]}' not in clients.keys():
                clients.update({f'{addr[0]}:{addr[1]}': conn})

    except IndexError:
        print('Specify the period in seconds as the parameter!\n'
              'Like this: python server.py 5')
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
