

def puzzle1():
    with open('data/day2data.txt', 'r') as file:
        data = []
        for line in file.readlines():
            split = line.split(' ')
            data.append((split[0], int(split[1])))

    horz, depth = 0, 0
    for dir, amt in data:
        if dir == 'forward':
            horz += amt
        elif dir == 'down':
            depth += amt
        elif dir == 'up':
            depth -= amt
        else:
            raise ValueError(f'Unknown direction: {dir}')
    print(horz, depth, (horz * depth))


def puzzle2():
    with open('data/day2data.txt', 'r') as file:
        data = []
        for line in file.readlines():
            split = line.split(' ')
            data.append((split[0], int(split[1])))

    aim, horz, depth = 0, 0, 0
    for dir, amt in data:
        if dir == 'forward':
            horz += amt
            depth += amt * aim
        elif dir == 'down':
            aim += amt
        elif dir == 'up':
            aim -= amt
        else:
            raise ValueError(f'Unknown direction: {dir}')
    print(aim, horz, depth, (horz * depth))
