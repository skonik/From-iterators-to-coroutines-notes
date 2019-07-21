import socket
import time


def get(url):
    sock = socket.socket()
    sock.connect(('lurkmore.to', 80))
    request = 'GET {} HTTP/1.1\r\nHost: lurkmore.to\r\n\r\n'.format(url)
    sock.sendall(bytes(request, encoding='utf-8'))
    chunk = sock.recv(4026)
    response = b''
    while chunk:
        response += chunk
        chunk = sock.recv(4026)
    sock.close()
    return ' '.join(response.decode('utf-8').split()[:3])


start = time.time()

for i in range(3):
    print(get('/'))

print(f"It took {time.time() - start}")