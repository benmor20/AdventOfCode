from puzzles.daybase import DayBase


class Day(DayBase):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            input, output = tuple(line.split(' | '))
            data.append((input.split(' '), output.split(' ')))
        return data

    def puzzle1(self):
        data = self.get_data()
        count = 0
        for i, (input, output) in enumerate(data):
            for seg in output:
                if len(seg) in (2, 3, 4, 7):
                    count += 1
                    # print(i, seg)
        print(count)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        len_key = {2: 1, 3: 7, 4: 4, 7: 8}
        for input, output in data:
            key = {}
            lens = {}
            for seg in input:
                string = ''.join(sorted(seg))
                if len(string) in len_key:
                    key[string] = len_key[len(string)]
                    lens[len(string)] = set(seg)
            for seg in input:
                string = ''.join(sorted(seg))
                s = set(seg)
                if len(string) not in len_key:
                    if len(string) == 6:
                        if lens[2] < s:
                            key[string] = 9 if lens[4] < s else 0
                        else:
                            key[string] = 6
                    else:  # length is 7
                        if lens[2] < s:
                            key[string] = 3
                        else:
                            key[string] = 5 if len(lens[4] - s) == 1 else 2
            num = 0
            for seg in output:
                s = ''.join(sorted(seg))
                print(key[s], end='')
                num *= 10
                num += key[s]
            total += num
            print()
        print(total)
