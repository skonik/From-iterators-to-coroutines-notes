def coroutine(func):
    def start(*args,**kwargs):
        gen = func(*args,**kwargs)
        gen.send(None)
        return gen
    return start


@coroutine
def some_generator(pattern):
    print('started')
    while True:
        string = yield
        print(pattern in string)


coro = some_generator('python')
print(f"coro len in bytes: {len(coro.gi_code.co_code)}")

coro.send('python is the best')
coro.send('test')
coro.close()