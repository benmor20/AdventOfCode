from year2024.day2024 import Day2024
from typing import *


def find_invalid_indexes(rules, update):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if (update[j], update[i]) in rules:
                return i, j
    return None


class Day(Day2024):
    @property
    def num(self) -> int:
        return 5

    def get_data(self, example=False):
        lines = super().get_data(example)
        rules = []
        updates = []
        on_rules = True
        for line in lines:
            if on_rules:
                if len(line) == 0:
                    on_rules = False
                    continue
                rules.append(tuple(int(i) for i in line.split('|')))
            else:
                updates.append([int(i) for i in line.split(',')])
        return rules, updates

    def puzzle1(self):
        list_rules, updates = self.get_data()
        rules = set(list_rules)
        total = 0
        for update in updates:
            works = True
            for i in range(len(update) - 1):
                for j in range(i + 1, len(update)):
                    if (update[j], update[i]) in rules:
                        # print(f'Update {update} does not work')
                        works = False
                        break
                if not works:
                    break
            if works:
                # print(f'Update {update} works')
                total += update[len(update) // 2]
        print(total)

    def puzzle2(self):
        list_rules, updates = self.get_data()
        rules = set(list_rules)
        total = 0
        for update in updates:
            swaps = 0
            while (idxs := find_invalid_indexes(rules, update)) is not None:
                swaps += 1
                i, j = idxs
                update[i], update[j] = update[j], update[i]
            if swaps > 0:
                total += update[len(update) // 2]
        print(total)


from functools import cmp_to_key


def one_line():
    return '\n'.join([data_sections := open('year2024/data/day5data.txt', 'r').read().split('\n\n'), rules := {tuple(int(i) for i in line.split('|')) for line in data_sections[0].split('\n')}, updates := [[int(i) for i in line.split(',')] for line in data_sections[1].split('\n')], key := cmp_to_key(lambda a, b: -1 if (a, b) in rules else 1), str(sum(update[len(update) // 2] for update in updates if update == sorted(update, key=key))), str(sum(sorted_update[len(update) // 2] for update in updates if (sorted_update := sorted(update, key=key)) != update))][-2:])
