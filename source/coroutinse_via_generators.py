def gen1():
    while True:
        msg = yield 'OK'
        print(f"gen1 got msg '{msg}'")


g = gen1()
# Ициализация потребляющего генератора
res = g.send(None)
print(f'g.send(None) returned {res}')
g.send('test')
print(f"g.send('test') returned {res}")
g.close()


def gen2():
    msg = yield
    print(f"gen2 got {msg}")
    msg = yield
    print(f"gen2 got again {msg}")
    return 'success'


g2 = gen2()
g2.send(None)
g2.send('test')
try:
    g.send('test')
except StopIteration as e:
    print('closed')
    print(e.value)


def gen3():
    yield from gen2()
    yield from gen1()


