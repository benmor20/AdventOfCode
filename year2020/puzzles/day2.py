from year2020.day2020 import Day2020_3


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example: bool = False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            split = line.split(' ')
            nums = split[0].split('-')
            data.append(((int(nums[0]), int(nums[1])), split[1][0], split[2]))
        return data

    def puzzle(self, num=1):
        count = 0
        for pwdinfo in self.get_data():
            nums, lett, pwd = pwdinfo
            if num == 1 and nums[0] <= pwd.count(lett) <= nums[1]:
                count += 1
            if num == 2 and (pwd[nums[0] - 1] == lett) ^ (pwd[nums[1] - 1] == lett):
                count += 1
        print(count)
