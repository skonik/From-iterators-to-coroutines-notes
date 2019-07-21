import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()


class Future:
    def __init__(self):
        self.result = None
        self.callbacks = []

    def resolve(self):
        for callback in self.callbacks:
            callback()

    def add_callback(self, fn):
        self.callbacks.append(fn)


class Task:
    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            next_future = next(self.coro)
        except StopIteration:
            return

        next_future.add_callback(self.step)


number_of_tasks = 0


def on_readable(sock, chunks):
    global number_of_tasks
    selector.unregister(sock.fileno())
    chunk = sock.recv(4096)
    if chunk:
        chunks.append(chunk)
        callback = lambda: on_readable(sock, chunks)
        future = Future()
        future.add_callback(callback)
        selector.register(sock.fileno(), EVENT_READ, data=future)
    else:
        # print(b''.join(chunks).decode().split('\n')[0])
        number_of_tasks -= 1
        return


def get(path):
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('0.0.0.0', 8080))
    except BlockingIOError:
        pass

    future = Future()
    selector.register(sock.fileno(), EVENT_WRITE, data=future)

    yield future

    selector.unregister(sock.fileno())
    request = 'GET {} HTTP/1.1\r\nHost: 0.0.0.0:8080\r\n\r\n'.format(path)
    sock.send(bytes(request, encoding='utf-8'))

    chunks = []
    callback = lambda: on_readable(sock, chunks)
    future = Future()
    future.add_callback(callback)
    selector.register(sock.fileno(), EVENT_READ, data=future)


start = time.time()


tasks = [Task(get('/')) for i in range(10000)]
number_of_tasks = len(tasks)

while number_of_tasks > 0:
    events = selector.select()

    for key, mask in events:
        future = key.data
        future.resolve()


print(f'Completed in {time.time() - start}')
