from year2022.day2022 import Day2022
from typing import *
import numpy as np


MOST_GEODES = 0


def time_until_can_make(recipes: List[np.ndarray], materials: np.ndarray, robots: np.ndarray, robot_type) -> int:
    needed = recipes[robot_type] - materials
    needed[needed < 0] = 0
    adj_robots = robots.copy()
    adj_robots[adj_robots == 0] = -1
    return int(np.max(np.ceil(needed / adj_robots))) + 1


def estimate_geode_count(recipes: List[np.ndarray], materials: np.ndarray, robots: np.ndarray, time_left: int) -> int:
    # Must be at least the actual final geode count, but ideally as close as possible
    est_time_with_geode = time_left - int(np.sum(robots == 0))
    return est_time_with_geode * (est_time_with_geode + 1) // 2


def max_geodes(recipes: List[np.ndarray], materials: np.ndarray, robots: np.ndarray, time_left: int) -> None:
    global MOST_GEODES
    if time_left == 0:
        geodes = materials[3]
        if geodes > MOST_GEODES:
            print(f'Reached 24 - New max for {recipes} is {geodes} with {materials}, {robots}')
            MOST_GEODES = geodes
        return
    recursed = False
    # print(recipes, materials, robots, time_left)
    for robot_type in range(3, -1, -1):
        if robot_type in (2, 3) and robots[robot_type - 1] == 0:
            continue
        time_to_make = time_until_can_make(recipes, materials, robots, robot_type)
        new_time_left = time_left - time_to_make
        if new_time_left < 0:
            continue
        if robot_type < 3 and new_time_left < 2:
            continue
        if robot_type == 0 and recipes[0][0] > new_time_left:
            # Don't produce ore bot if it won't make up for itself
            continue
        new_mats = materials + robots * time_to_make - recipes[robot_type]
        new_robs = robots.copy()
        new_robs[robot_type] += 1
        if estimate_geode_count(recipes, new_mats, new_robs, new_time_left) < MOST_GEODES:
            continue
        max_geodes(recipes, new_mats, new_robs, new_time_left)
        recursed = True
    if not recursed:
        geodes = materials[3] + robots[3] * time_left
        if geodes > MOST_GEODES:
            print(f'No new robots - New max for {recipes} is {geodes} with {materials + robots * time_left}, {robots}')
            MOST_GEODES = geodes


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
        start_mat = np.zeros((4, ), dtype=int)
        start_rob = np.array([1, 0, 0, 0], dtype=int)
        for i, recipes in enumerate(data):
            global MOST_GEODES
            MOST_GEODES = 0
            max_geodes(recipes, start_mat.copy(), start_rob.copy(), 24)
            print(f'{recipes} can produce {MOST_GEODES} geodes')
            total += (i + 1) * MOST_GEODES
        print(total)

    def puzzle2(self):
        data = self.get_data(True)
