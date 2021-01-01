import json
import socketserver
import time

import psutil

stats = {}
step = 1
time_ = 0
period = 5


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global time_
        global step
        global stats

        if time.time() - time_ > period:
            print('Monitoring..')
            stats = monitor()
            time_ = time.time()

            step += 1
            if step % 2 == 0:
                self.request.sendall(stats.encode(encoding='utf-8'))
                print('Sent', stats, f'at {time.strftime("%H:%M:%S")}')


def monitor():
    cpu = psutil.cpu_percent(0.1)
    r = psutil.virtual_memory()
    data = {'cpu': cpu, 'ram': [r.percent, r.used / (1024**3)]}
    return json.dumps(data)


def main():
    HOST, PORT = '0.0.0.0', 55555
    global period
    global stats

    period = int(input('Enter the monitoring period in seconds: '))

    stats = monitor()
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
