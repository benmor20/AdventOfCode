from year2021.day2021 import Day2021
import numpy as np


def parse_data(lines):
    data = []
    for line in lines:
        row = []
        for c in line:
            num = -1
            if c == '.':
                num = 0
            elif c in 'ABCD':
                num = ord(c) - ord('A') + 1
            row.append(num)
        if len(data) > 0:
            row.extend([-1] * (len(data[0]) - len(row)))
        data.append(row)
    return np.array(data)[1:-1, 1:-1]


def room_index(species):
    return 2 * species


def species_index(room):
    return room // 2


def is_sorted(arr):
    return np.all(arr[1:, 2:10:2] == np.array([1, 2, 3, 4]))


def path_clear(arr, start, end):
    if start[0] == 0:
        if end[0] > 0 and not np.all(arr[0:end[0]+1, end[1]] == 0):
            return False
    else:
        if not np.all(arr[0:start[0]-1, start[1]] == 0):
            return False
    if start[1] < end[1]:
        return np.all(arr[0, start[1] + 1:end[1] + 1] == 0)
    else:
        return np.all(arr[0, end[1]:start[1]] == 0)


def can_enter(arr, species):
    room = room_index(species)
    a1 = arr[1:, room] == 0
    a2 = arr[1:, room] == species
    return np.all(a1 | a2)


def lowest_empty(arr, room):
    lst = [i for i in range(1, arr.shape[0]) if arr[i, room] == 0]
    if len(lst) == 0:
        return 0
    return max(lst)


def least_energy_after_move(arr, start, end, prev_energy=None):
    species = arr[start]
    clear = path_clear(arr, start, end)
    if start == end or species == 0 or not clear:
        # print(f'From {start} to {end}, species is {species}, path clear: {clear}')
        return None
    movement = abs(start[0] - end[0]) + abs(start[1] - end[1])
    energy = movement * 10 ** (arr[start] - 1)
    if prev_energy is not None and energy > prev_energy:
        return None
    nxt = arr.copy()
    nxt[start], nxt[end] = 0, species
    nxt_energy = least_energy(nxt, prev_energy=prev_energy)
    if nxt_energy is not None:
        return energy + nxt_energy
    return None


available_stops = (0, 1, 3, 5, 7, 9, 10)
memo = {}
def least_energy(arr, prev_energy=None):
    if is_sorted(arr):
        return 0
    tuparr = tuple(arr.reshape((-1,)))
    if tuparr in memo:
        return memo[tuparr]
    best_energy = prev_energy
    # print_array(arr)
    for space in available_stops:
        species = arr[0, space]
        if species > 0:
            room = room_index(species)
            if can_enter(arr, species):
                end_row = lowest_empty(arr, room)
                if end_row == 0:
                    continue
                energy = least_energy_after_move(arr, (0, space), (end_row, room), prev_energy=best_energy)
                if energy is not None and (best_energy is None or energy < best_energy):
                    best_energy = energy
    for room in range(2, 10, 2):
        if np.all(arr[1:, room] == 0):
            continue
        start = lowest_empty(arr, room) + 1
        if np.all(arr[start:, room] == species_index(room)):
            continue
        for space in available_stops:
            energy = least_energy_after_move(arr, (start, room), (0, space), prev_energy=best_energy)
            # print(f'Moving {arr[start, room]} from room {room} to space {space} gives energy of {energy}')
            if energy is not None and (best_energy is None or energy < best_energy):
                best_energy = energy
    memo[tuparr] = best_energy
    return best_energy


def print_array(arr):
    for line in arr:
        for num in line:
            if num == -1:
                c = '#'
            elif num == 0:
                c = '.'
            else:
                c = chr(num - 1 + ord('A'))
            print(c, end='')
        print()
    print()


class Day(Day2021):
    @property
    def num(self) -> int:
        return 23

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            row = []
            for c in line:
                num = -1
                if c == '.':
                    num = 0
                elif c in 'ABCD':
                    num = ord(c) - ord('A') + 1
                row.append(num)
            data.append(row)
        return np.array(data)[1:-1, 1:-1]

    def puzzle1(self):
        arr = self.get_data()
        arr = np.concatenate((arr[:2, :], arr[-1:, :]))
        print_array(arr)
        print(least_energy(arr))

    def puzzle2(self):
        arr = self.get_data()
        print_array(arr)
        print(least_energy(arr))
