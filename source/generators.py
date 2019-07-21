def grep(data, pattern):
    for i in data:
        if pattern in i:
            yield i

    return f'end for pattern {pattern}'


g = grep(['ruby is the best', 'python is the best', '<3 python'], 'python')
next(g)
# 'python is the best'
next(g)
# '<3 python'
#next(g)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# StopIteration


def grep_from_1(pattern):
    for i in grep(['ruby', 'python', 'pythonista'], pattern):
        yield i
    for i in grep(['from C# to python', 'C++', 'pythons'], pattern):
        yield i


def grep_from_2(pattern):
    yield from grep(['ruby', 'python', 'pythonista'], pattern)
    yield from grep(['from C# to python', 'C++', 'from python to js'], pattern)


grep2 = grep_from_2('python')
for i in grep2:
    print(i)


def grep_from_3():
    first_yield_from = yield from grep(['ruby', 'python', 'pythonista'], 'python')
    print(f'first yeild from: "{first_yield_from}"')
    second_yield_from = yield from grep(['from C# to python', 'C++', 'from python to js'], 'C')
    print(f'second yeild from: "{second_yield_from}"')

grep3 = grep_from_3()
for i in grep3:
    print(f"i = {i}")