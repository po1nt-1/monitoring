import json
import threading
import socketserver
import sys
import time

import psutil

stats = {}
step = 1


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global step
        global stats

        if step % 2 == 0:
            self.request.sendall(stats.encode(encoding='utf-8'))
            print('Sent', stats, f'at {time.strftime("%H:%M:%S")}')
            time.sleep(0.5)


def monitor(period):
    try:
        global stats
        global step

        time_ = 0
        while True:
            if time.time() - time_ > period:
                time_ = time.time()
                step += 1

                print('Monitoring..')
                cpu = psutil.cpu_percent(0.1)
                r = psutil.virtual_memory()
                data = {'cpu': cpu, 'ram': [r.percent, r.used / (1024**3)]}

                stats = json.dumps(data)
    except KeyboardInterrupt:
        return -1


def main():
    try:
        HOST, PORT = '0.0.0.0', 55555

        try:
            arg = sys.argv[1]
            if not arg or not arg.isnumeric():
                raise IndexError
            else:
                period = int(arg)
                if not period > 0:
                    raise IndexError
        except IndexError:
            print('Specify the period in seconds as the parameter!\n'
                  'Like this: python server.py 5')
            return -1

        thread = threading.Thread(target=monitor, args=(period,))
        thread.setDaemon(True)
        thread.start()

        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
