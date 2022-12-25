from year2022.day2022 import Day2022
from typing import *
import numpy as np
from utils.optimization_tree import OptimizationTree


MATERIALS = ['ore', 'clay', 'obsidian', 'geode']


class Factory:
    def __init__(self, recipes: List[np.ndarray]):
        self.recipes = recipes
        self.robots = np.array([1, 0, 0, 0])
        self.amounts = np.zeros((4,))
        self.robot_to_build = -1

    @staticmethod
    def _time_until(amounts: np.ndarray, robots: np.ndarray, recipes: List[np.ndarray], robot_type: int):
        amt_needed = recipes[robot_type] - amounts
        amt_needed *= amt_needed > 0
        new_robots = robots - (robots == 0)
        return int(np.max(np.ceil(amt_needed / new_robots))) + 1

    def time_until(self, *robot_types):
        robots = self.robots.copy()
        amts = self.amounts.copy()
        total = 0
        for robot_type in robot_types:
            time = Factory._time_until(amts, robots, self.recipes, robot_type)
            amts += robots * time
            amts -= self.recipes[robot_type]
            robots = robots + np.eye(4)[robot_type]
            total += time
        return total

    def strategy(self):
        for i in range(3, 0, -1):
            if self.robots[i - 1] > 0:
                if np.all(self.amounts >= self.recipes[i]):
                    self.build(i)
                    return
                break
        type_to_make = 3 if np.all(self.robots > 0) else np.where(self.robots == 0)[0][0]
        nxt_mat = MATERIALS[type_to_make]
        cur_mat = MATERIALS[type_to_make - 1]
        prv_mat = MATERIALS[type_to_make - 2]
        if np.any(self.amounts < self.recipes[type_to_make - 1])\
                and (type_to_make < 2 or np.any(self.amounts < self.recipes[type_to_make - 2]))\
                and (type_to_make < 3 or np.any(self.amounts < self.recipes[0])):
            return
        time_if_nxt = self.time_until(type_to_make)
        time_if_cur = self.time_until(type_to_make - 1, type_to_make)
        if type_to_make >= 2:
            time_if_prv = self.time_until(type_to_make - 2, type_to_make - 1, type_to_make)
        else:
            time_if_prv = 1000
        if type_to_make == 3:
            time_if_ore = self.time_until(0, 1, 2, 3)
        else:
            time_if_ore = 1000

        print(f'{time_if_nxt} turns to make {nxt_mat}, or {time_if_cur} turns to make {cur_mat} then {nxt_mat}', end='')
        if type_to_make > 1:
            print(f', or {time_if_prv} if {prv_mat} then {cur_mat} then {nxt_mat}', end='')
            if type_to_make == 3:
                print(f', or {time_if_ore} if ore then clay then obsidian then geode', end='')
        print()
        if type_to_make == 3:
            time_if_nxt -= 0.5
        if time_if_ore <= time_if_nxt and time_if_ore <= time_if_cur and time_if_ore <= time_if_prv:
            self.build(0)
        elif time_if_prv <= time_if_nxt and time_if_prv <= time_if_cur:
            self.build(type_to_make - 2)
        elif time_if_cur <= time_if_nxt:
            self.build(type_to_make - 1)

    def step(self):
        self.amounts += self.robots
        if self.robot_to_build > -1:
            self.robots[self.robot_to_build] += 1
            self.robot_to_build = -1

    def build(self, robot_type: int) -> bool:
        if self.robot_to_build > -1:
            return False
        if np.any(self.recipes[robot_type] > self.amounts):
            return False
        print(f'Making {MATERIALS[robot_type]} robot')
        self.amounts -= self.recipes[robot_type]
        self.robot_to_build = robot_type
        return True

    def run(self) -> int:
        print(self.recipes)
        for i in range(24):
            print(f'Minute {i+1}')
            print(f'Start with {self.amounts} materials and {self.robots} robots')
            self.strategy()
            self.step()
            print(f'Now have {self.amounts} materials and {self.robots} robots')
            print()
        print()
        return int(self.amounts[3])


def time_until(robot_type: int, recipes: List[np.ndarray], state: np.ndarray) -> int:
    if np.any((recipes[robot_type] > 0) & (state[4:] == 0)):
        return -1
    amt_needed = recipes[robot_type] - state[:4]
    amt_needed *= amt_needed > 0
    robots = state[4:].copy()
    robots -= robots == 0
    return int(np.max(np.ceil(amt_needed / robots))) + 1


def optimize(recipes: List[np.ndarray], time_elapsed: int = 0, state: Optional[np.ndarray] = None) -> int:
    if state is None:
        state = np.array([0, 0, 0, 0, 1, 0, 0, 0], dtype=int)
        print(f'Start processing {recipes}')
    if time_elapsed > 24:
        assert False
    if time_elapsed == 24:
        return state[3]
    possibilities = []
    for robot_type in range(3, -1, -1):
        time = time_until(robot_type, recipes, state)
        if time == -1 or time_elapsed + time > 24:
            continue
        robot_addition = np.zeros((4,), dtype=int)
        robot_addition[robot_type] = 1
        addition = np.concatenate((state[4:] * time - recipes[robot_type], robot_addition))
        new_state = state + addition
        # print(f'Making {MATERIALS[robot_type]} takes us from {state} to {new_state} in {time} mins ({time+time_elapsed} total mins)')
        possibilities.append(optimize(recipes, time_elapsed + time, new_state))
    if len(possibilities) == 0:  # No more robots can be produced in time
        return state[3] + state[7] * (24 - time_elapsed)
    return max(possibilities)


def calculate_geodes(state: Tuple[int, ...]) -> Tuple[int, int]:
    pass


class GeodeTree(OptimizationTree[np.ndarray]):
    def __init__(self, recipes: List[np.ndarray]):
        super().__init__((0, 0, 0, 0, 0, 1, 0, 0, 0))
        self.recipes = recipes
        self.poss_geodes: Dict[Tuple[int, ...], Tuple[int, int]] = {}

    def find_children(self, parent: Tuple[int, ...], layer: int) -> List[Tuple[int, ...]]:
        children = []
        time_left = 24 - parent[0]
        parent_arr = np.array(parent)

        do_nothing = parent_arr.copy()
        do_nothing[0] = 24
        do_nothing[1:5] += parent_arr[5:] * time_left
        children.append(tuple(do_nothing))

        for robot_type in range(3, -1, -1):
            time = time_until(robot_type, self.recipes, parent_arr[1:])
            if time == -1 or time_left < time:
                continue
            if robot_type == 0 and self.recipes[0][0] > time_left:  # cost to produce > what it will make
                continue
            new_robot = np.eye(4, dtype=int)[robot_type]
            new_material = parent_arr[5:] * time
            new_material -= self.recipes[robot_type]
            new_time = np.array([time])
            to_add = np.concatenate([new_time, new_material, new_robot])
            new_state = parent_arr + to_add
            new_tup = tuple(new_state)
            self.poss_geodes[new_tup] = calculate_geodes(new_state)
            children.append(tuple(new_state))
        return children

    def trim_leaf(self, leaf: Tuple[int, ...], layers: List[Set[Tuple[int, ...]]], leaf_layer: int) -> bool:
        if leaf[0] == 24:
            return True
        if leaf[0] == 23 and leaf[-1] == 0:
            return True
        return False
        # return any(s[0] > max_geode for s in self._scores.values())

    def evaluate(self, state: Tuple[int, ...], layer: int) -> int:
        return state[4]


class Day(Day2022):
    @property
    def num(self) -> int:
        return 19

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            line = line.split(': ')[1]
            recipe_strs = line.split('.')
            recipes = []
            for recipestr in recipe_strs:
                words = recipestr.split(' ')
                if words[0] == '':
                    words = words[1:]
                if len(words) == 0:
                    continue
                robot_type = words[1]
                ingredient_strs = words[4:]
                amts = np.array([int(ingredient_strs[0]), 0, 0, 0], dtype=int)
                if len(ingredient_strs) == 2:
                    recipes.append(amts)
                    continue
                if words[-1] == 'clay':
                    amts[1] = int(ingredient_strs[-2])
                elif words[-1] == 'obsidian':
                    amts[2] = int(ingredient_strs[-2])
                recipes.append(amts)
            data.append(recipes)
        return data

    def puzzle1(self):
        data = self.get_data(True)
        total = 0
        for i, recipes in enumerate(data):
            tree = GeodeTree(recipes)
            tree.run(24)
            best_state, _ = tree.best_result()
            print(f'{recipes} gave best state of {best_state}')
            total += (i + 1) * best_state[4]
        print(total)

    def puzzle2(self):
        data = self.get_data(True)
