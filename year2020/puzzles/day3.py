from year2020.day2020 import Day2020_3


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 3

    def get_data(self, example: bool = False):
        lines = super().get_data(example)
        trees = []
        for line in lines:
            trees.append([c == '#' for c in line if c != '\n'])
        return trees

    def count_trees(self, trees, xchange, ychange):
        xpos, ypos = 0, 0
        trees_hit = 0
        while ypos < len(trees):
            if trees[ypos][xpos]:
                trees_hit += 1
            xpos += xchange
            xpos %= len(trees[0])
            ypos += ychange
        return trees_hit

    def puzzle(self, num=1):
        trees = self.get_data()
        if num == 1:
            print(self.count_trees(trees, 3, 1))
        if num == 2:
            slopes = [(x, 1) for x in range(1, 8, 2)] + [(1, 2)]
            prod = 1
            for slope in slopes:
                prod *= self.count_trees(trees, slope[0], slope[1])
            print(prod)
