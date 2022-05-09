from typing import *
from year2019.day2019 import Day2019
import collections


class Counter(collections.Counter):
    def __add__(self, other):
        keys = set(self.keys()).union(set(other.keys()))
        res = Counter()
        for key in keys:
            new_val = self[key] + other[key]
            if new_val != 0:
                res[key] = new_val
        return res

    def __sub__(self, other):
        keys = set(self.keys()).union(set(other.keys()))
        res = Counter()
        for key in keys:
            new_val = self[key] - other[key]
            if new_val != 0:
                res[key] = new_val
        return res

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            res = Counter()
            for key, amt in self.items():
                new_val = amt * other
                if new_val != 0:
                    res[key] = new_val
            return res
        else:
            keys = set(self.keys()).union(set(other.keys()))
            res = Counter()
            for key in keys:
                new_val = self[key] * other[key]
                if new_val != 0:
                    res[key] = new_val
            return res

    def __repr__(self):
        string = super().__repr__()[8:-1]
        return '{}' if len(string) == 0 else string


def done(cntr, eqns):
    for chem in eqns:
        if chem == 'ORE':
            continue
        if cntr[chem] >= eqns[chem][0]:
            return False
    return True


def step(cntr, eqns, int_only=True):
    for chem, amt in cntr.copy().items():
        if chem == 'ORE':
            continue
        needed_amt, components = eqns[chem]
        if int_only:
            d, m = divmod(cntr[chem], needed_amt)
            if m > 0:
                d += 1
        else:
            d = cntr[chem] / needed_amt
        # print(f'Removing {d*needed_amt} of {chem} from {cntr}')
        cntr = cntr - Counter({chem: d * needed_amt})
        # print(f'Counter is now {cntr}')

        adtn = components * d
        # print(f'Adding {adtn}')
        cntr = cntr + adtn

        # print(f'Counter is now {cntr}')
    return cntr


class Day(Day2019):
    @property
    def num(self) -> int:
        return 14

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = {}
        for line in lines:
            inp, out = tuple(line.split(' => '))
            terms = inp.split(', ')
            cntr = Counter()
            for term in terms:
                amt, chem = tuple(term.split(' '))
                cntr[chem] = int(amt)
            amt, chem = tuple(out.split(' '))
            data[chem] = int(amt), cntr
        return data

    def puzzles(self):
        eqns = self.get_data()
        # for chem, (amt, eqn) in eqns.items():
        #     print(f'{amt} {chem}: {eqn}')

        cntr = Counter({'FUEL': 1})
        while not done(cntr, eqns):
            cntr = step(cntr, eqns, True)
        print(cntr)
        print(f'You need {cntr["ORE"]} ORE to produce one FUEL')

        cntr = Counter({'FUEL': 1})
        while not done(cntr, eqns):
            cntr = step(cntr, eqns, False)
        num_fuel = 1e12 // cntr['ORE']
        print(f'With 1 trillion ORE you can produce {num_fuel} FUEL')
