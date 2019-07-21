from collections import deque


def counter(start_number, max_number):
    current_number = start_number
    while current_number < max_number:
        print(current_number)
        yield
        current_number += 1


tasks = deque([counter(10, 15),
               counter(5, 10),
               counter(0, 5)
               ])

while tasks:
    task = tasks.pop()
    try:
        next(task)
        tasks.appendleft(task)
    except StopIteration:
        pass