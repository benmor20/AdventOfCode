import numpy as np


def parse_binary(vals):
    res = 0
    for v in vals:
        res *= 2
        res += v
    return res


def puzzle1():
    with open('data/day3data.txt', 'r') as file:
        lst = [[int(v) for v in row[:-1]] for row in file.readlines()]
        data = np.array(lst)
    totals = data.sum(0)
    gamma, epsilon = 0, 0
    for total in totals:
        gamma *= 2
        epsilon *= 2
        if total > data.shape[0] / 2:
            gamma += 1
        else:
            epsilon += 1
    print(gamma, epsilon, gamma * epsilon, gamma & epsilon)


def filter_data(data, reverse, index = 0):
    if data.shape[0] == 1:
        return data[0]
    totals = data.sum(0)
    most_common = 1 if totals[index] >= len(data) / 2 else 0
    filtered = data[(data[:, index] == most_common) ^ reverse, :]
    # print(f'Most common is {most_common}, keeping {[parse_binary(row) for row in filtered]}')
    return filter_data(filtered, reverse, index + 1)


def puzzle2():
    with open('data/day3data.txt', 'r') as file:
        lst = [[int(v) for v in row[:-1]] for row in file.readlines()]
        data = np.array(lst)
    o2_list = filter_data(data, False)
    co2_list = filter_data(data, True)
    o2, co2 = 0, 0
    for i in range(data.shape[1]):
        o2 *= 2
        co2 *= 2
        o2 += o2_list[i]
        co2 += co2_list[i]
    print(o2, co2, o2 * co2)
