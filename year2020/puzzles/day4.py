from year2020.day2020 import Day2020_3


is_valid = {'byr': lambda i: 1920 <= int(i) <= 2002,
            'iyr': lambda i: 2010 <= int(i) <= 2020,
            'eyr': lambda i: 2020 <= int(i) <= 2030,
            'hgt': lambda h: (h[-2:] == 'cm' and 150 <= int(h[:-2]) <= 193)
            or (h[-2:] == 'in' and 59 <= int(h[:-2]) <= 76),
            'hcl': lambda h: len(h) == 7 and h[0] == '#' and set(h[1:]) <= set('0123456789abcdef'),
            'ecl': lambda e: e in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
            'pid': lambda p: len(p) == 9 and set(p) <= set('0123456789'),
            'cid': lambda c: True}


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 4

    def get_data(self, example: bool = False):
        lines = super().get_data(example)
        passports = []
        passport = {}
        for line in lines:
            if line == '\n':
                passports.append(passport)
                passport = {}
                continue
            for info in line.split(' '):
                splt = info.split(':')
                passport[splt[0]] = splt[1]
                if splt[1][-1] == '\n':
                    passport[splt[0]] = passport[splt[0]][:-1]
        return passports

    def puzzle(self, num=1):
        passports = self.get_data()
        cats = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
        num_valid = 0
        for passport in passports:
            if set(passport) >= set(cats):
                if num == 1 or (num == 2 and all([is_valid[k](v) for k, v in passport.items()])):
                    num_valid += 1
        print(num_valid)