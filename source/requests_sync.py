import time
from threading import Thread

import requests


def get(url):
    requests.get(url)


start = time.time()

tasks = [Thread(target=get, args=('http://localhost:8080/',)) for i in range(1000)]
for thread in tasks:
    thread.start()
for thread in tasks:
    thread.join()

print(f"It took {time.time() - start}")