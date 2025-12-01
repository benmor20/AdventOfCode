from year2025.day2025 import Day2025


class Day(Day2025):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [(line[0] == 'L', int(line[1:])) for line in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        dial = 50
        for left, amt in data:
            if left:
                dial -= amt
            else:
                dial += amt
            dial %= 100
            if dial == 0:
                total += 1
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        dial = 50
        prev_left = False
        for left, og_amt in data:
            og_dial = dial
            div, amt = divmod(og_amt, 100)
            total += div
            if left:
                dial -= amt
            else:
                dial += amt
            added = False
            if (dial <= 0 or dial >= 100) and og_dial != 0: # and not (og_dial == 0 and left != prev_left):
                total += 1
                added = True
            dial %= 100
            prev_left = left
            print(f"Started at {og_dial}. After moving {'L' if left else 'R'}{og_amt}, did full rev {div} times leaving {amt} left over, ending on {dial}, {added=} leaving total at {total}")
        print(total)


def one_line():
    pass
