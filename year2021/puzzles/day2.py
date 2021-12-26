from year2021.day2021 import Day2021


class Day(Day2021):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        data = []
        for line in super().get_data():
            split = line.split(' ')
            data.append((split[0], int(split[1])))
        return data

    def puzzle1(self):
        data = self.get_data()
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

    def puzzle2(self):
        data = self.get_data()
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
