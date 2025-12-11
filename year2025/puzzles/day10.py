import itertools
import re
from collections import deque, Counter

import numpy as np
from scipy.optimize import LinearConstraint, milp, Bounds

from utils.utils import add_tuples, scale_tuple, tuple_diff
from year2025.day2025 import Day2025


class Machine:
    def __init__(self, input_str: str):
        match = re.fullmatch(r"\[([.#]+)] ([ ,\d()]+) \{([\d,]+)}", input_str)
        assert match is not None
        lights = match.group(1)
        buttons = match.group(2)
        joltage = match.group(3)
        self.joltage = tuple(int(j) for j in joltage.split(","))
        self.nlights = len(lights)
        self.lights_on = frozenset(idx for idx, light in enumerate(lights) if light == '#')
        self.buttons = []
        self.button_tups = []
        for button_str in buttons.split(" "):
            self.buttons.append({int(b) for b in button_str.strip("()").split(",")})
            self.button_tups.append(tuple(1 if idx in self.buttons[-1] else 0 for idx in range(self.nlights)))

    @property
    def nbuttons(self) -> int:
        return len(self.buttons)


def press_button_p1(originally_on: frozenset[int], to_switch: set[int]) -> frozenset[int]:
    res = set(originally_on)
    for val in to_switch:
        if val in res:
            res.remove(val)
        else:
            res.add(val)
    return frozenset(res)


def press_button_p2(original_joltage: tuple[int, ...], to_add: tuple[int, ...]) -> tuple[int, ...]:
    return add_tuples(original_joltage, to_add)


class Day(Day2025):
    @property
    def num(self) -> int:
        return 10

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [Machine(line) for line in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for machine in data:
            queue = deque[frozenset[int]]()
            dists = {frozenset(): 0}
            queue.append(frozenset())
            while len(queue) > 0:
                node = queue.popleft()
                if node == machine.lights_on:
                    break
                for button in machine.buttons:
                    next_lights = press_button_p1(node, button)
                    if next_lights in dists:
                        continue
                    queue.append(next_lights)
                    dists[next_lights] = dists[node] + 1
            total += dists[machine.lights_on]
        print(total)


    def puzzle2(self):
        data = self.get_data()
        total = 0
        for midx, machine in enumerate(data):
            cost = np.ones(machine.nbuttons)
            integrality = np.ones(machine.nbuttons)
            bounds = Bounds(0)
            A = np.zeros((machine.nlights, machine.nbuttons))
            for idx, btn in enumerate(machine.button_tups):
                A[:, idx] = np.array(btn)
            constraint_bound = np.array(machine.joltage)
            constraint = LinearConstraint(A, constraint_bound, constraint_bound)
            soln = milp(cost, integrality=integrality, bounds=bounds, constraints=[constraint])
            assert np.allclose(A @ soln.x, constraint_bound)
            joltage = tuple(0 for _ in range(machine.nlights))
            for btn, amt in zip(machine.button_tups, soln.x):
                for _ in range(int(np.round(amt))):
                    joltage = press_button_p2(joltage, btn)
            assert list(joltage) == list(machine.joltage)
            print(f"Finished {midx}")
            total += sum(int(np.round(val)) for val in soln.x)
        print(total)


def one_line():
    pass
