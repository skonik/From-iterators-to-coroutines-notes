import socket
import time
from threading import Thread


def get(url):
    sock = socket.socket()
    sock.connect(('localhost', 8080))
    request = 'GET {} HTTP/1.1\r\nHost: 0.0.0.0:8080\r\n\r\n'.format(url)
    sock.sendall(bytes(request, encoding='utf-8'))
    chunk = sock.recv(4026)
    response = b''
    while chunk:
        response += chunk
        chunk = sock.recv(4026)
    sock.close()
    return ' '.join(response.decode('utf-8').split()[:3])


start = time.time()

tasks = [Thread(target=get, args=('/',)) for i in range(10000)]
for thread in tasks:
    thread.start()
for thread in tasks:
    thread.join()

print(f"It took {time.time() - start}")