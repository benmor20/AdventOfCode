from abc import ABC, abstractmethod


class DayBase(ABC):
    @property
    @abstractmethod
    def num(self) -> int:
        pass

    @property
    @abstractmethod
    def year(self) -> int:
        pass

    def puzzles(self):
        pass

    def get_data(self, example=False):
        ex_str = ''
        if example:
            ex_str = 'ex'
            if not isinstance(example, bool):
                ex_str += str(example)
        with open(f'year{self.year}/data/day{self.num}{ex_str}data.txt', 'r') as file:
            return [l.replace('\n', '') for l in file.readlines()]


class DayBase2(DayBase, ABC):
    @abstractmethod
    def puzzle1(self):
        pass

    @abstractmethod
    def puzzle2(self):
        pass

    def puzzles(self):
        self.puzzle1()
        self.puzzle2()


class DayBase3(DayBase, ABC):
    @abstractmethod
    def puzzle(self, puzzle_num=1):
        pass

    def puzzles(self):
        self.puzzle(1)
        self.puzzle(2)
