from year2020.day2020 import Day2020_3
import numpy as np
from scipy.signal import correlate2d
import itertools
from utils.utils import *


kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def num_occupied(seats, seen, num):
    if num == 1:
        return correlate2d(seats == 2, kernel, mode='same')
    occ = np.zeros(seats.shape)
    for i in range(occ.shape[0]):
        for j in range(occ.shape[1]):
            if seats[i, j] == 0:
                occ[i, j] = 0
                continue
            occ[i, j] = sum([1 for s in seen[i, j].values() if s is not None and seats[s] == 2])
    return occ


def calculate_seen_seats(seats):
    res = {}
    for seat in itertools.product(range(seats.shape[0]), range(seats.shape[1])):
        if seats[seat] == 0:
            continue
        dct = {}
        for direc in itertools.product((-1,0,1), repeat=2):
            if direc == (0,0):
                continue
            dct[direc] = first_seat_in_dir(seats, seat, direc)
        res[seat] = dct
    return res


def first_seat_in_dir(seats, pos, direc, start=True):
    if start:
        return first_seat_in_dir(seats, add_tuples(pos, direc), direc, False)
    if not in_range(pos, seats.shape):
        return None
    if seats[pos] > 0:
        return pos
    return first_seat_in_dir(seats, add_tuples(pos, direc), direc, False)


def in_range(coords, shape):
    return 0 <= coords[0] < shape[0] and 0 <= coords[1] < shape[1]


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example: bool = False):
        return np.array([[1 if c == 'L' else 0 for c in row] for row in super().get_data(example)])

    def puzzle(self, num=1):
        prev = None
        seats = self.get_data()
        seen = calculate_seen_seats(seats) if num == 2 else None
        for i in itertools.count(1):
            empty = seats == 1
            occupied = seats == 2
            count_occ = num_occupied(seats, seen, num)
            seats[empty & (count_occ == 0)] = 2
            seats[occupied & (count_occ >= (4 if num == 1 else 5))] = 1
            if prev is not None and (prev == seats).all():
                print(np.sum(seats == 2))
                return
            prev = seats.copy()
