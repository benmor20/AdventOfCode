from collections import deque


def puzzle1():
    with open('data/day1data.txt', 'r') as file:
        data = [int(d) for d in file.readlines()]
    increases = 0
    prev = data[0]
    for d in data[1:]:
        if d > prev:
            increases += 1
        prev = d
    print(increases)


def puzzle2():
    window_size = 3
    with open('data/day1data.txt', 'r') as file:
        data = [int(d) for d in file.readlines()]
    increases = 0
    queue = deque(data[:window_size])
    prev = sum(queue) / window_size
    for d in data[window_size:]:
        queue.popleft()
        queue.append(d)
        av = sum(queue) / window_size
        if av > prev:
            increases += 1
        prev = av
    print(increases)
