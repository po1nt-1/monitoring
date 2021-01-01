import json
import socketserver

import psutil


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        stats = monitor()
        self.request.sendall(stats.encode(encoding='utf-8'))
        print('Sended:', stats)


def monitor():
    cpu = psutil.cpu_percent(1)
    r = psutil.virtual_memory()
    data = {'cpu': cpu, 'ram': [r.percent, r.used]}
    return json.dumps(data)


if __name__ == "__main__":
    HOST, PORT = '', 55555

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
