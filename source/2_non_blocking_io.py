import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket

selector = DefaultSelector()

number_of_tasks = 0


def on_readable(sock, chunks):
    global number_of_tasks
    selector.unregister(sock.fileno())
    chunk = sock.recv(4096)
    if chunk:
        chunks.append(chunk)
        callback = lambda: on_readable(sock, chunks)
        selector.register(sock.fileno(), EVENT_READ, data=callback)
    else:
        # print(b''.join(chunks).decode().split('\n')[0])
        number_of_tasks -= 1
        return


def on_connected(sock, path):
    selector.unregister(sock.fileno())
    request = 'GET {} HTTP/1.1\r\nHost: lurkmore.to\r\n\r\n'.format(path)
    sock.send(bytes(request, encoding='utf-8'))

    chunks = []
    callback = lambda: on_readable(sock, chunks)
    selector.register(sock.fileno(), EVENT_READ, data=callback)


def get(path):
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('lurkmore.to', 80))
    except BlockingIOError:
        pass

    # Замыкание
    callback = lambda: on_connected(sock, path)
    selector.register(sock.fileno(), EVENT_WRITE, data=callback)


start = time.time()


tasks = [get('/') for i in range(3)]
number_of_tasks = len(tasks)

while number_of_tasks > 0:
    events = selector.select()

    for key, mask in events:
        callback = key.data
        callback()


print(f'Completed in {time.time() - start}')
