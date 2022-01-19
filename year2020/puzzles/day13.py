import itertools

from year2020.day2020 import Day2020


def update(seq, new_constraint):
    res_step = seq[1] * new_constraint[0]
    # print(f'Updating {seq} to match {new_constraint}')
    for i in itertools.count(*seq):
        # print(f'{i} is {i % new_constraint[0]} more than a multiple of {new_constraint[0]}')
        if i % new_constraint[0] == new_constraint[1]:
            # print(f'Match! Returning {i, res_step}')
            return i, res_step


class Day(Day2020):
    @property
    def num(self) -> int:
        return 13

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [-1 if s == 'x' else int(s) for s in lines[1].split(',')]
        return int(lines[0]), data

    def puzzles(self):
        min_time, ids = self.get_data()
        # Puzzle 1
        time_to_wait, best_id = -1, 0
        for id in ids:
            if id == -1:
                continue
            wait = id - (min_time % id)
            if time_to_wait == -1 or wait < time_to_wait:
                time_to_wait, best_id = wait, id
        print(f'Need to wait {time_to_wait} units for bus {best_id}, answer is {time_to_wait * best_id}')

        # Puzzle 2
        id_map = {id: (id - (i % id)) % id for i, id in enumerate(ids) if id != -1}  # for k, v in items: ans is v more than a multiple of k
        seq = 0, list(id_map)[0]  # params for arithmetic sequence that meets constraint
        for i, (id, offset) in enumerate(id_map.items()):
            if i == 0:
                continue
            seq = update(seq, (id, offset))
        print(f'First timestamp is {seq[0]} (repeats every {seq[1]})')
