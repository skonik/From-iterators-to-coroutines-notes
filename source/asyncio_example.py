import asyncio


@asyncio.coroutine
def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    yield from asyncio.sleep(1.0)
    return x + y

@asyncio.coroutine
def print_sum(x, y):
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))


loop = asyncio.get_event_loop()
#task = loop.create_task(print_sum(1, 2))
# loop.run_until_complete(task)
loop.run_until_complete(print_sum(1, 2))
loop.close()